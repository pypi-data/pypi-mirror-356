import functools
import logging
import os
from datetime import datetime
from http import HTTPStatus
from dashscope import Application
from flask import Response, stream_with_context,jsonify
from dotenv import load_dotenv
import json
from . import file_utils
from services.aliyun_service import AliyunApiService


# 加载 .env 文件中的环境变量
load_dotenv()

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('api', __name__, url_prefix='/api')

dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
bailian_app_id = os.getenv("BAILIAN_APP_ID")
user_api_keyid = os.getenv("USER_API_KEYID")
mcp_secret_key = os.getenv("MCP_SECRET_KEY")

logging.basicConfig(level=logging.INFO)
logging.info("DASHSCOPE_API_KEY: %s", dashscope_api_key)
logging.info("BAILIAN_APP_ID: %s", bailian_app_id)
logging.info("USER_API_KEYID: %s", user_api_keyid)
logging.info("MCP_SECRET_KEY: %s", mcp_secret_key)

bailian_open_words = '### 开场词：\n```\n欢迎回来！我是您专属的养老顾问小瑞，很高兴再次为您服务。我注意到您之前已经填写过养老规划报\n告所需的部分信息，为了更好地协助您，请问您本次是希望：\n1. 调整原有报告（更新信息或修改目标）\n2. 完善更多信息（补充数据）\n3. 其他问题咨询\n请直接告诉我您的需求，我会立刻为您安排！\n```'




@bp.route('/chat', methods=['POST'])
def chat():

    """
        请求：
            {
                "planId": "202505151734531020000041",
                "messages": "这里是提问信息",
                "sessionId": "sessionId",
                "file": [
                    "https://example.com/images/example.jpg",
                    "https://example.com/images/example2.jpg"
                ],
                "mode": 0
            }
        响应：
            {
                "planId": "planId",
                "sessionId": "sessionId",
                "text": "这里是生成的回复内容",
                "code": 1,
                "message": "success",
                "requestId": "1d14958f-0498-91a3-9e15-be477971967b"
            }
    """


    logging.debug("chat index")

    #获取请求头和json请求体
    headers = request.headers
    reqJson = request.json
    logging.info("Request Headers:\n%s", headers)
    logging.info("Request JSON:\n%s", json.dumps(reqJson))

    # 获取头信息中的keyId
    keyId = headers.get('keyId')
    if keyId != user_api_keyid:
        logging.error("Invalid Secret Key")
        return  jsonify({"code": 0, "message": "Invalid Secret Key"})

    logging.info("KeyId: %s", keyId)

    #获取头信息中的cytx-token
    cytxToken = headers.get('cytx-token')
    if cytxToken is None:
        logging.error("Invalid cytx-token")
        return  jsonify({"code": 0, "message": "Invalid cytx-token"})

    # 获取请求体中的planId
    planId = reqJson.get('planId')
    logging.info("planId: %s", planId)

    if planId is None:
        logging.error("Invalid planId")
        return  jsonify({"code": 0, "message": "Invalid planId"})

    # 获取请求体中的mode
    mode : Any = reqJson.get('mode')
    logging.info("mode: %s", mode)
    if mode is None:
       mode = 0

    #  获取请求体中的messages
    messages = reqJson.get('messages')
    logging.info("messages: %s", messages)

    if messages is None:
        logging.error("messages is None")
        return  jsonify({"code": 0, "message": "messages is None"})

    #判断messages是不是数组及数组长度
    if not isinstance(messages, list) or len(messages) == 0:
        logging.error("Invalid messages")
        return  jsonify({"code": 0, "message": "Invalid messages"})

    # 判断messages数组中，第一条数据的角色是不是system，如果不是system，把开场词添加到messages数组第一位
    if messages[0].get('role') != 'system':
        messages.insert(0, {"role": "system", "content": bailian_open_words})



    # 获取请求体中的 sessionId
    sessionId = reqJson.get('sessionId')
    logging.info("sessionId: %s", sessionId)

    #获取请求体中的 fileUrls
    fileIds = reqJson.get('fileIds')
    logging.info("fileIds: %s", fileIds)

    biz_params = {
        "sk": mcp_secret_key,
        "cytxToken": cytxToken,
        "planId": planId,
    }
    logging.info("biz_params: %s", biz_params)
    logging.info("mode: %s", mode)


    if mode == 0:
        responses = Application.call(
            api_key=dashscope_api_key,
            app_id=bailian_app_id,
            stream=True,
            incremental_output=True,
            biz_params=biz_params,
            messages=messages,
        )
        logging.info("responses: %s", responses)

        return Response(generate(responses,planId=planId), mimetype='application/json')

    elif mode == 1 or mode==2:

        logging.info("fileIds:%s",  fileIds)
        #判断fileUrls数组是否为空
        if fileIds is None or len(fileIds) == 0:
            return jsonify({"code": 0, "message": "Invalid fileIds"})

        responses = Application.call(
            api_key=dashscope_api_key,
            app_id=bailian_app_id,
            stream=True,
            incremental_output=True,
            biz_params=biz_params,
            rag_options={"session_file_ids": fileIds},
            messages=messages
        )
        logging.info("responses: %s", responses)

        return Response(generate(responses,planId=planId), mimetype='application/json')

    else:
        logging.error("Invalid mode")
        return jsonify({"code": 0, "message": "Invalid mode"})



# 文件上传接口
@bp.route('/fileUpload', methods=['POST'])
def fileUpload():

    """
    curl -X POST http://127.0.0.1:5000/api/fileUpload \
      -H "keyId: KAQML-HWNMU-KWPBZ-CFLZF-UCWKD" \
      -H "Content-Type: multipart/form-data" \
      -F "file=@./1.xlsx"

    """

    logging.info("into fileUpload")
    logging.info("Request Headers:\n%s", request.headers)
    logging.info("Request Files:\n%s", request.files)
    # 获取头信息中的keyId
    keyId = request.headers.get('keyId')
    if keyId != user_api_keyid:
        logging.error("Invalid Secret Key")
        return jsonify({"code": 0, "message": "Invalid Secret Key"})
    if 'file' not in request.files:
        return {"code": 0, "message": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"code": 0, "message": "No selected file"}, 400
    # 获取当前日期并格式化为 YYYYMMDD
    today = datetime.now().strftime("%Y%m%d")

    # 构建基础上传目录和当天的子目录
    base_upload_folder = os.getenv('UPLOAD_FOLDER', './uploads')
    date_folder = os.path.join(base_upload_folder, today)

    # 自动创建日期目录（如果不存在）
    os.makedirs(date_folder, exist_ok=True)

    file_path = os.path.join(date_folder, file.filename)
    # 保存文件到日期目录中
    file.save(file_path)
    file_size = os.path.getsize(file_path)
    logging.info("file_size: %s", file_size)
    file_md5 = file_utils.calculate_md5(file_path)
    logging.info("file_md5: %s", file_md5)

    file_id = AliyunApiService.do_upload_file_to_bailian(file_path,file.filename,file_md5,str(file_size))
    if file_id is None:
        return {"code": 0, "message": "File upload failed","file_id": None}

    return {"code": 1, "message": "success","file_id": file_id}


@stream_with_context
def generate(*args, **kwargs):
    responses = args[0]
    planId = kwargs.get('planId', '')
    for response in responses:
        if response.status_code != HTTPStatus.OK:
            print(f'request_id={response.request_id}')
            print(f'code={response.status_code}')
            print(f'message={response.message}')
            print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        else:
            print(f'usage={response.usage}')
            print(f'output={response.output}\n')
            print(f'status_code={response.status_code}\n')
            print(f'request_id={response.request_id}\n')
            print(f'session_id={response.output.session_id}\n')
            print(f'code={response.code}\n')
            print(f'message={response.message}\n')
            print(f'{response.output.text}\n')  # 处理只输出文本text
            yield json.dumps({
                "code": 1,
                "message": "success",
                "text": response.output.text,
                "sessionId": response.output.session_id,
                "planId":  planId,
                "request_id":response.request_id
            })





