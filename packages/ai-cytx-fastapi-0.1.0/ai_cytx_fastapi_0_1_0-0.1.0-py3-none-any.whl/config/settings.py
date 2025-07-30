import os
from dotenv import load_dotenv
load_dotenv()

# 把.env中的环境变量都加载进来
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
bailian_app_id = os.getenv("BAILIAN_APP_ID")
bailian_app_id_report = os.getenv("BAILIAN_APP_ID_REPORT")
user_api_keyid = os.getenv("USER_API_KEYID")
secret_key = os.getenv("SECRET_KEY")
mcp_secret_key = os.getenv("MCP_SECRET_KEY")
api_base_url = os.getenv("API_BASE_URL")

mcp_name =os.getenv("MCP_NAME")
mcp_server_host = os.getenv("MCP_SERVER_HOST")
mcp_server_port = os.getenv("MCP_SERVER_PORT")
mcp_log_name = os.getenv("MCP_LOG_NAME")

report_mcp_name = os.getenv("REPORT_MCP_NAME")
report_mcp_server_host = os.getenv("REPORT_MCP_SERVER_HOST")
report_mcp_server_port = os.getenv("REPORT_MCP_SERVER_PORT")
report_mcp_log_name = os.getenv("REPORT_MCP_LOG_NAME")

upload_folder = os.getenv("UPLOAD_FOLDER")
alibaba_cloud_access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
alibaba_cloud_access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
alibaba_cloud_categoryid = os.getenv("ALIBABA_CLOUD_CATEGORYID")
alibaba_cloud_workspaceid = os.getenv("ALIBABA_CLOUD_WORKSPACEID")
alibaba_cloud_categorytype = os.getenv("ALIBABA_CLOUD_CATEGORYTYPE")

web_server_host = os.getenv("WEB_SERVER_HOST")
web_server_port = os.getenv("WEB_SERVER_PORT")
web_log_name = os.getenv("WEB_LOG_NAME")

cytx_api_url = os.getenv("CYTX_API_URL")
cytx_api_getPlanData_url = cytx_api_url + "/api/aged/getPlanData"
cytx_api_getAgedInsurance_url = cytx_api_url + "/api/aged/getAgedInsurance"
cytx_api_getTargetList_url = cytx_api_url + "/api/aged/getTargetList"
cytx_api_getSolution_url = cytx_api_url + "/api/aged/getSolution"
cytx_api_saveBasicInfo_url = cytx_api_url + "/api/aged/saveBasicInfo"
cytx_api_saveAgeInsurance_url = cytx_api_url + "/api/aged/saveAgeInsurance"
cytx_api_saveTargetList_url = cytx_api_url + "/api/aged/saveTargetList"
cytx_api_saveSolution_url = cytx_api_url + "/api/aged/saveSolution"

cytx_api_select_report_url = cytx_api_url + "/api/pub/selectReportJson"
cytx_api_calc_target_list_url = cytx_api_url + "/api/whole/planCalc/calcTargetList"
cytx_api_get_plan_report_url = cytx_api_url + "/api/aged/getPlanReport"

type_code_list = [
  {
    "name": "个人信息",
    "code": "0-0-0"
  },
  {
    "name": "资产",
    "code": "1-0-0"
  },
  {
    "name": "资产-现金类资产",
    "code": "1-1-0"
  },
  {
    "name": "资产-现金类资产-活期存款",
    "code": "1-1-6"
  },
  {
    "name": "资产-现金类资产-货币基金",
    "code": "1-1-8"
  },
  {
    "name": "资产-固收类资产",
    "code": "1-2-0"
  },
  {
    "name": "资产-固收类资产-定期存款",
    "code": "1-2-7"
  },
  {
    "name": "资产-固收类资产-债券",
    "code": "1-2-11"
  },
  {
    "name": "资产-固收类资产-债券类基金",
    "code": "1-2-23"
  },
  {
    "name": "资产-固收类资产-理财产品",
    "code": "1-2-24"
  },
  {
    "name": "资产-权益类资产",
    "code": "1-3-0"
  },
  {
    "name": "资产-权益类资产-股票",
    "code": "1-3-9"
  },
  {
    "name": "资产-权益类资产-股票类基金",
    "code": "1-3-10"
  },
  {
    "name": "资产-权益类资产-私募基金",
    "code": "1-3-31"
  },
  {
    "name": "资产-房产类资产-房产",
    "code": "1-5-14"
  },
  {
    "name": "资产-个人养老金",
    "code": "1-46-46"
  },
  {
    "name": "资产-公积金账户",
    "code": "1-47-47"
  },
  {
    "name": "资产-社保养老账户",
    "code": "1-17-17"
  },
  {
    "name": "资产-企业年金",
    "code": "1-48-48"
  },
  {
    "name": "资产-其他资产-其他资产",
    "code": "1-4-12"
  },
  {
    "name": "资产-其他资产-贵金属",
    "code": "1-4-41"
  },
  {
    "name": "财务-收入-工作收入",
    "code": "2-1-1"
  },
  {
    "name": "财务-收入-经营性收入",
    "code": "2-1-2"
  },
  {
    "name": "财务-收入-其他长期收入(主动收入)",
    "code": "2-1-3"
  },
  {
    "name": "财务-收入-其他长期收入(被动收入)",
    "code": "2-1-4"
  },
  {
    "name": "财务-支出-生活支出",
    "code": "2-4-1"
  },
  {
    "name": "财务-支出-子女教育",
    "code": "2-4-2"
  },
  {
    "name": "财务-支出-赡养父母支出",
    "code": "2-4-3"
  },
  {
    "name": "财务-支出-旅游支出",
    "code": "2-4-4"
  },
  {
    "name": "财务-支出-娱乐支出",
    "code": "2-4-5"
  },
  {
    "name": "财务-支出-其他支出",
    "code": "2-4-6"
  },
  {
    "name": "养老目标",
    "code": "3-0-0"
  },
  {
    "name": "养老目标-医疗",
    "code": "3-1-0"
  },
  {
    "name": "养老目标-医疗-医保",
    "code": "3-1-1"
  },
  {
    "name": "养老目标-医疗-普通保障",
    "code": "3-1-2"
  },
  {
    "name": "养老目标-医疗-高端医疗保障",
    "code": "3-1-3"
  },
  {
    "name": "养老目标-医疗-慢病医疗",
    "code": "3-1-5"
  },
  {
    "name": "养老目标-医疗-重疾医疗",
    "code": "3-1-6"
  },
  {
    "name": "养老目标-居住",
    "code": "3-2-0"
  },
  {
    "name": "养老目标-居住-居住",
    "code": "3-2-1"
  },
  {
    "name": "养老目标-居住-养老院",
    "code": "3-2-2"
  },
  {
    "name": "养老目标-居住-养老社区",
    "code": "3-2-5"
  },
  {
    "name": "养老目标-护理",
    "code": "3-3-0"
  },
  {
    "name": "养老目标-护理-家人照顾",
    "code": "3-3-1"
  },
  {
    "name": "养老目标-护理-保姆照顾",
    "code": "3-3-2"
  },
  {
    "name": "养老目标-护理-护工照顾",
    "code": "3-3-1"
  },
  {
    "name": "养老目标-生活-无分类",
    "code": "3-6-0"
  },
  {
    "name": "养老目标-爱好-无分类",
    "code": "3-7-0"
  },
  {
    "name": "养老目标-自定义-无分类",
    "code": "3-9-0"
  },
  {
    "name": "保险-医疗险-无分类",
    "code": "4-1-0"
  },
  {
    "name": "保险-意外险-无分类",
    "code": "4-2-0"
  },
  {
    "name": "保险-重疾险-无分类",
    "code": "4-3-0"
  },
  {
    "name": "保险-养老年金险-无分类",
    "code": "4-4-0"
  },
  {
    "name": "保险-寿险-无分类",
    "code": "4-5-0"
  },
  {
    "name": "满意度",
    "code": "5-0-0"
  }
,
  {
    "name": "保险",
    "code": "4-0-0"
  }
]
