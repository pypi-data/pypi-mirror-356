import json
import logging
import re
import time
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from typing import Dict, Any, Union, List, Optional

from mcp.server.fastmcp import FastMCP

from config.settings import mcp_secret_key, mcp_server_host, mcp_server_port, type_code_list, mcp_name, mcp_log_name
from models.command_model import CommandModel
from services.common_utils import is_empty
from services.mcp_service import MCPService
from services.requests_service import requests_get_solution, requests_get_insurance, requests_get_plan_data, \
    requests_get_target_list

# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        TimedRotatingFileHandler(mcp_log_name, when="D", backupCount=7),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logging.getLogger("mcp.server.sse").setLevel(logging.DEBUG)


dependencies=[
    "websockets"
]

mcp = FastMCP(mcp_name,port=int(mcp_server_port),host=mcp_server_host,dependencies=dependencies)


# @mcp.tool(name="getPlanData",description="获取养老规划基本信息")
def getPlanData(sk:str,cytxToken:str,planId:str) -> str:
    """
    获取养老规划的基本信息。
    
    参数:
    - sk: 秘钥，用于验证请求合法性。
    - cytxToken: 用户令牌，用于身份验证。
    - planId: 养老规划的唯一标识符。
    
    返回:
    - JSON格式的字符串，包含养老规划的基本信息。
    """
    logger.info("into getPlanData")
    # 记录方法执行时间
    start_time = time.time()
    # 打印接收到的参数
    logger.info("Received parameters: sk=%s, cytxToken=%s, planId=%s", sk, cytxToken, planId)
    
    # 校验请求参数是否合法
    validate_str = validate_request(sk,cytxToken, planId)
    if validate_str is not None:
        return validate_str
    
    try:
        # 调用服务层方法获取养老规划基本信息
        retData = requests_get_plan_data(cytxToken,planId)
    except Exception as e:
        # 记录异常信息
        logger.error("Error: %s", e)
        return json.dumps({"error": "requests_get_plan_data error"})
    
    # 记录方法执行时间
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info("Execution time: %.2f seconds", execution_time)
    return json.dumps(retData)


# @mcp.tool(name="getAgedInsurance",description="获取养老规划保险保障信息")
def getAgedInsurance(sk:str,cytxToken:str,planId:str) -> str:
    logger.info("into getAgedInsurance")
    start_time = time.time()
    # 打印接收到的参数
    logger.info("Received parameters: sk=%s, cytxToken=%s, planId=%s", sk, cytxToken, planId)
    validate_str = validate_request(sk, cytxToken, planId)
    if validate_str is not None:
        return validate_str
    try:
        retData = requests_get_insurance(cytxToken, planId)
    except Exception as e:
        logger.error("Error: %s", e)
        return json.dumps({"error": "requests_get_insurance error"})
    # 如何打印方法执行时间
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info("Execution time: %.2f seconds", execution_time)
    return json.dumps(retData)

# @mcp.tool(name="getTargetList",description="获取养老规划目标信息")
def getTargetList(sk:str,cytxToken:str,planId:str) -> str:
    logger.info("into getTargetList")
    # 如何打印方法执行时间
    start_time = time.time()
    # 打印接收到的参数
    logger.info("Received parameters: sk=%s, cytxToken=%s, planId=%s", sk, cytxToken, planId)
    validate_str = validate_request(sk, cytxToken, planId)
    if validate_str is not None:
        return validate_str
    try:
        retData = requests_get_target_list(cytxToken, planId)
    except Exception as e:
        logger.error("Error: %s", e)
        return json.dumps({"error": "requests_get_target_list error"})
    
    # 如何打印方法执行时间
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info("Execution time: %.2f seconds", execution_time)
    return json.dumps(retData)

# @mcp.tool(name="getSolution",description="获取养老规划解决方案")
def getSolution(sk:str,cytxToken:str,planId:str) -> str:
    logger.info("into getSolution")
    start_time = time.time()
    # 打印接收到的参数
    logger.info("Received parameters: sk=%s, cytxToken=%s, planId=%s", sk, cytxToken, planId)
    validate_str = validate_request(sk, cytxToken, planId)
    if validate_str is not None:
        return validate_str
    try:
        retData = requests_get_solution(cytxToken, planId)
    except Exception as e:
        logger.error("Error: %s", e)
        return json.dumps({"error": "requests_get_solution error"})
    
    # 如何打印方法执行时间
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info("Execution time: %.2f seconds", execution_time)
    return json.dumps(retData)

@mcp.tool(name="updateBasicInfo", description="更新")
def updateBasicInfo(sk: str, cytxToken: str, planId: str, reqStr: Union[Dict[str, Any], List[Dict[str, Any]], str, None]) -> str:
    """
    更新养老规划的相关信息。
    
    参数:
    - sk: 秘钥，用于验证请求合法性。
    - cytxToken: 用户令牌，用于身份验证。
    - planId: 养老规划的唯一标识符。
    - reqStr: 请求数据，可以是JSON字符串或字典列表。
    
    返回:
    - JSON格式的字符串，包含更新操作的结果。
    """
    logger.info("into updateBasicInfo")
    # 记录方法执行时间
    start_time = time.time()
    # 打印接收到的参数
    logger.info("Received parameters: sk=%s, cytxToken=%s, planId=%s, reqStr=%s", sk, cytxToken, planId, reqStr)
    
    # 校验请求参数是否合法
    validate_str = validate_request(sk, cytxToken, planId)
    if validate_str is not None:
        return validate_str
    
    try:
        # 将请求数据转换为JSON格式
        if isinstance(reqStr, str):
            reqJson = json.loads(reqStr)
        else:
            reqJson = reqStr
    except json.JSONDecodeError as e:
        # 记录无效JSON格式的错误
        logger.error("Invalid JSON input: %s", e)
        return "Invalid JSON format"

    # 打印请求参数
    logger.info("Request JSON:%s", json.dumps(reqJson))

    # 将 reqJson 转换为 CommandModel 对象
    try:
        command_models = [CommandModel(**item) for item in reqJson]
    except Exception as e:
        # 记录CommandModel解析失败的错误
        logger.error("Failed to parse CommandModel: %s", e)
        return "Invalid CommandModel format"

    # 初始化结果列表
    results = []
    # 设置变量，用来存储各个分类的数组
    base_lists =[]
    targets_lists = []
    insurance_lists = []
    solutions_lists = []
    
    # 遍历 CommandModel 数组，根据 command 类型分类处理
    for command_model in command_models:
        command_type = command_model.type
        #  根据command和command_type进行分组。 分组逻辑如下，command分为add、update、delete，command_type分为以0，1，2，3，4，5开头的
        try:
            logger.info("command_type: %s", command_type)
            if command_type.startswith("0") or command_type.startswith("1") or command_type.startswith("2") :
                if command_type == "0" or command_type =="0-0-0":
                    # 基本信息都按照更新逻辑走
                    command_model.type = "0-0-0"
                    command_model.command='update'
                base_lists.append(command_model)
            elif command_type.startswith("3") :
                targets_lists.append(command_model)
            elif command_type.startswith("4") :
                insurance_lists.append(command_model)
            elif command_type.startswith("5") :
                solutions_lists.append(command_model)
            else:
                results.append("Unsupported command_type")
        except Exception as e:
            # 捕获异常并记录错误信息
            logger.error(f"Error processing command '{command}': {e}")
            results.append(f"Error processing command '{command}': {str(e)}")
            
    # 处理基本信息
    if base_lists is not None and len(base_lists) > 0:
        try:
            retData = MCPService.update_base_list(base_lists, cytxToken, planId)
            results.append(retData)
        except Exception as e:
            logger.error("Error: %s", e)
            return json.dumps({"error": "update_base_list error"})
    
    # 处理目标信息
    if targets_lists is not None and len(targets_lists) > 0:
        try:
            retData = MCPService.update_target_list(targets_lists, cytxToken, planId)
            results.append(retData)
        except Exception as e:
            logger.error("Error: %s", e)
            return json.dumps({"error": "update_target_list error"})
    
    # 处理保险信息
    if insurance_lists is not None and len(insurance_lists) > 0:
        try:
            retData = MCPService.update_insurance_list(insurance_lists, cytxToken, planId)
            results.append(retData)
        except Exception as e:
            logger.error("Error: %s", e)
            return json.dumps({"error": "update_insurance_list error"})
    
    # 处理解决方案信息
    if solutions_lists is not None and len(solutions_lists) > 0:
        try:
            retData = MCPService.update_solutions_list(solutions_lists, cytxToken, planId)
            results.append(retData)
        except Exception as e:
            logger.error("Error: %s", e)
            return json.dumps({"error": "update_solutions_list error"})
    
    # 记录方法执行时间
    end_time = time.time()
    logger.info("Method execution time: %.2f seconds", end_time - start_time)
    logger.info("Update Results: %s", json.dumps(results))
    # 将所有结果整合成一个数组返回
    return json.dumps(results)

# @mcp.tool(name="mergeBaseInfo",description="合并养老规划基本信息")
def mergeBaseInfo(sk: str, cytxToken: str, planId: str, reqStr: Any) -> Any:
    logger.info("into mergeBaseInfo")
    #  如何打印方法执行时间
    start_time = time.time()
    
    # 打印接收到的参数
    logger.info("Received parameters: sk=%s, cytxToken=%s, planId=%s, reqStr=%s", sk, cytxToken, planId, reqStr)
    
    validate_str = validate_request(sk, cytxToken, planId)
    if validate_str is not None:
        return validate_str
    
    try:
        if isinstance(reqStr, str):
            reqJson = json.loads(reqStr)
        else:
            reqJson = reqStr
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON input: %s", e)
        return "Invalid JSON format"
        
    # 打印请求参数reqJson
    logger.info("Request JSON:%s", json.dumps(reqJson))
    
    try:
        MCPService.handle_merge_logic(reqJson, cytxToken, planId)
    except Exception as e:
        logger.error("merge fail: %s", e)
        return json.dumps({"error": "merge fail"})
    # 如何打印方法执行时间
    end_time = time.time()
    logger.info("Method execution time: %.2f seconds", end_time - start_time)
    return json.dumps({"status": "OK"})

@mcp.tool(name="queryInfo", description="查询")
def queryInfo(sk: str, cytxToken: str, planId: str, reqStr: Union[Dict[str, Any], List[Dict[str, Any]], str, None]) -> str:
    """
    查询养老规划的所有相关信息。
    
    参数:
    - sk: 秘钥，用于验证请求合法性。
    - cytxToken: 用户令牌，用于身份验证。
    - planId: 养老规划的唯一标识符。
    - reqStr: 请求数据，包含type和ownertype字段。
    
    返回:
    - JSON格式的字符串，包含所有查询到的信息。
    """
    logger.info("into queryInfo")
    # 记录方法执行时间
    start_time = time.time()
    # 打印接收到的参数
    logger.info("Received parameters: sk=%s, cytxToken=%s, planId=%s, reqStr=%s", sk, cytxToken, planId, reqStr)
    
    # 校验请求参数是否合法
    validate_str = validate_request(sk, cytxToken, planId)
    if validate_str is not None:
        return validate_str
    
    try:
        # 将请求数据转换为JSON格式
        if isinstance(reqStr, str):
            reqJson = json.loads(reqStr)
        else:
            reqJson = reqStr
    except json.JSONDecodeError as e:
        # 记录无效JSON格式的错误
        logger.error("Invalid JSON input: %s", e)
        return "Invalid JSON format"

    # 打印请求参数
    logger.info("Request JSON:%s", json.dumps(reqJson))
    
    # 判断下，如果reqJson是数组，只取第一个元素
    reqJson = reqJson[0] if isinstance(reqJson, list) else reqJson

    # 初始化结果字典
    results = {}

    # 根据type和ownertype字段调用不同的查询方法
    try:
        search_age = None
        if "searchAge" in reqJson:
            search_age = reqJson["searchAge"]
            
        
        if "type" in reqJson and "ownerType" in reqJson:
            type_value = reqJson["type"]
            ownertype_value = reqJson["ownerType"]
            
            if is_empty(ownertype_value):
                ownertype_value = "0"
                
            if is_empty(type_value):
                type_value = "0-0-0"
            
            # 进行格式校验
            if re.match(r'^\d+(-\d+)*$', type_value):
                pass
            elif re.match(r'^[\u4e00-\u9fa5]+(-[\u4e00-\u9fa5]+)*(-[\u4e00-\u9fa5]+)*$', type_value):
                type_value = get_type_code_by_name(type_value)
            else:
                return json.dumps({"error": "Invalid type format"})
            
            # 查询基础信息
            if type_value.startswith("0") :
                base_info = requests_get_plan_data(cytxToken, planId)
                find_result = MCPService.find_data_by_type_new(type_value, base_info, ownertype_value, None, None)
                
            elif type_value.startswith("1") :
                base_info = requests_get_plan_data(cytxToken, planId)
                find_result = MCPService.find_data_by_type_new(type_value, base_info, ownertype_value, None, None)
                
            elif type_value.startswith("2") :
                if search_age is not None and type_value == "2-1-1" :
                    base_info = requests_get_plan_data(cytxToken, planId,need_filter=False)
                    search_age = calculate_search_age(base_info,search_age, ownertype_value)
                    find_result = MCPService.find_data_by_type_new(type_value, base_info, ownertype_value, None, None)
                    find_result = filter_by_age(find_result, search_age)
                else:
                    base_info = requests_get_plan_data(cytxToken, planId)
                    find_result = MCPService.find_data_by_type_new(type_value, base_info, ownertype_value, None, None)

            # 查询目标信息
            elif type_value.startswith("3") :
                target_info = requests_get_target_list(cytxToken, planId,None, None)
                find_result = MCPService.find_data_by_type_new(type_value, target_info, ownertype_value, None, None)

            # 查询保险信息
            elif type_value.startswith("4"):
                insurance_info = requests_get_insurance(cytxToken, planId)
                find_result = MCPService.find_data_by_type_new(type_value, insurance_info, ownertype_value, None, None)

            # 查询解决方案信息
            elif type_value.startswith("5"):
                solution_info = requests_get_solution(cytxToken, planId)
                find_result = MCPService.find_data_by_type_new(type_value, solution_info, ownertype_value, None, None)
            # 如果ownertype为特定值，可以扩展其他逻辑
            else:
                pass
            
            if find_result:
                # 房产需要单独处理，因为房产id居然都是一致的
                result_items = [item[0] for item in find_result if item[0] is not None]
                if type_value == "1-5-14" :
                    result_items = filter_house_id(result_items)
            else:
                result_items = []
            
            results["data"] = result_items
        else:
            logger.error("Invalid request parameters")
            return json.dumps({"error": "Invalid request parameters"})

    except Exception as e:
        # 捕获异常并记录错误信息
        logger.error("Error querying information: %s", e)
        return json.dumps({"error": "Error querying information"})

    # 记录方法执行时间
    end_time = time.time()
    logger.info("Method execution time: %.2f seconds", end_time - start_time)
    logger.info("Query results: %s", json.dumps(results))
    # 返回所有查询结果
    return json.dumps(results)

# 写个方法，校验请求参数
def validate_request(sk: str, cytxToken: str, planId: str) -> str:
    if sk != mcp_secret_key:
        logger.error("Invalid Secret Key")
        return "Invalid Secret Key"
    
    if cytxToken is None:
        logger.error("cytxToken is None")
        return "cytxToken is None"
    
    if planId is None:
        logger.error("planId is None")
        return "planId is None"
    
    return None

def filter_house_id(house_list):
    """
    过滤掉房产id
    """
    for house in house_list:
        if house["id"]:
            house.pop('id')
    return house_list

def get_type_code_by_name(type_name: str) -> str:
    for type_code in type_code_list:
        if type_code["name"] == type_name:
            return type_code["code"]
    return ""

def filter_by_age(data_list: List[Dict[str, Any]], search_age: int) -> List[Dict[str, Any]]:
    """
    根据 search_age 过滤数据列表。

    Args:
        data_list (List[Dict[str, Any]]): 数据列表。
        search_age (int): 搜索年龄。

    Returns:
        List[Dict[str, Any]]: 过滤后的数据列表。
    """
    logger.info("into filter_by_age")
    logger.info("data_list: %s", data_list)
    logger.info("search_age: %s", search_age)
    for item in data_list:
        if item[0]["desp"] ==  "工作收入":
            am = get_optimal_amt_by_age(item[0].get("trendDTO", {}),  search_age)
            if am is not None:
                item[0]["amount"] = am
    
    # 过滤trendDTO
    for item in data_list:
        item[0].pop("trendDTO", None)
    
    return data_list
    
    
    
def calculate_search_age(data: Dict[str, Any],search_age: Optional[int],ownertype_value: str) -> int:
    """
   计算 search_age 的值。

   如果 search_age < 100，直接返回；
   如果 search_age >= 100，认为是年份，如2025年，计算当前年龄。

   Args:
       search_age (Optional[int]): 输入的 search_age 值。

   Returns:
       int: 计算后的年龄。
   """
    logger.info("into calculate_search_age")
    if search_age is None:
        return None
    if search_age < 100:
        return search_age
    if search_age >= 2000:
        if str(ownertype_value) == "0":
            current_age = data.get("planInfo").get("currentAge")
        else:
            current_age = data.get("planInfo").get("mateCurrentAge")
        
        # 根据当前年龄和当前年份，计算search_age时的年龄
        # 获取当前年份
        current_year = datetime.now().year
        return current_age + (search_age - current_year)
        
    else:
        return None


def get_optimal_amt_by_age(data: dict, age: int) -> Optional[float]:
    """
    根据传入的年龄，在 data['ageArr'] 中查找对应的索引，
    并返回 data['optimalAmtList'][index] 的值。

    Args:
        data (dict): 包含 ageArr 和 optimalAmtList 的数据字典。
        age (int): 要查询的年龄。

    Returns:
        Optional[float]: 查询结果，如果找不到则返回 None。
    """
    age_list = data.get("ageArr", [])
    optimal_amt_list = data.get("optimalAmtList", [])
    
    try:
        index = age_list.index(age)
        return optimal_amt_list[index]
    except ValueError:
        logger.warning(f"Age {age} not found in ageArr.")
        return None
    except IndexError:
        logger.error(f"Index error when accessing optimalAmtList for age {age}.")
        return None

def main():
    mcp.run(transport="sse")

if __name__ == "__main__":
    # Initialize and run the server
    main()
