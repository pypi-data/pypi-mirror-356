# 对接所有cytx的接口

import json
import logging

import requests

from config.settings import cytx_api_getPlanData_url, cytx_api_getAgedInsurance_url, cytx_api_getTargetList_url, \
    cytx_api_getSolution_url, cytx_api_saveBasicInfo_url, cytx_api_saveAgeInsurance_url, cytx_api_saveTargetList_url, \
    cytx_api_saveSolution_url,cytx_api_select_report_url,cytx_api_calc_target_list_url,cytx_api_get_plan_report_url

logger = logging.getLogger(__name__)

def requests_get_insurance(cytxToken: str, planId: str) -> dict:
    """
    获取保险数据。

    该函数通过发送POST请求，获取指定计划下的保险数据。

    参数:
    - cytxToken: 用户令牌，用于身份验证。
    - planId: 计划ID，用于指定需要获取保险数据的计划。

    返回:
    - 一个字典，包含保险数据。
    """
    try:
        logger.info("into requests_get_insurance")
        logger.info("cytxToken: %s, planId: %s", cytxToken, planId)
        
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        
        # 初始化请求体，至少包含planId
        body = {
            "planId": planId
        }
        
        logger.info("requests_get_insurance body:\n%s", json.dumps(body))
        
        # 发送POST请求到指定URL
        response = requests.post(cytx_api_getAgedInsurance_url, headers=headers, json=body)
        
        # 检查响应状态码是否为200，否则抛出异常
        if response.status_code != 200:
            logger.error("Failed to requests_get_insurance: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
            logger.info("requests_get_insurance response:\n%s", json.dumps(respJson))
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        # 提取响应数据中的data部分
        retData = respJson.get("data")
        # 记录处理后的响应数据日志
        logger.info("requests_get_insurance response:\n%s", json.dumps(retData))
        # 返回处理后的数据
        return retData
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)
    
def requests_get_solution(cytxToken: str, planId: str) -> dict:
    """
    获取解决方案数据。

    该函数通过发送POST请求，获取指定计划下的解决方案数据。

    参数:
    - cytxToken: 用户令牌，用于身份验证。
    - planId: 计划ID，用于指定需要获取解决方案数据的计划。

    返回:
    - 一个字典，包含解决方案数据。
    """
    try:
        logger.info("into requests_get_solution")
        logger.info("cytxToken: %s, planId: %s", cytxToken, planId)
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        # 初始化请求体，至少包含planId
        body = {
            "planId": planId
        }
        
        logger.info("requests_get_solution request:\n%s", json.dumps(body))
        
        # 发送POST请求到指定URL
        response = requests.post(cytx_api_getSolution_url, headers=headers, json=body)
        # 检查响应状态码是否为200，否则抛出异常
        if response.status_code != 200:
            logger.error("Failed to requests_get_solution: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
            logger.info("requests_get_solution response:\n%s", json.dumps(respJson))
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        # 提取响应数据中的data部分
        retData = respJson.get("data")
        # 记录处理后的响应数据日志
        logger.info("requests_get_solution response:\n%s", json.dumps(retData))
        # 返回处理后的数据
        return retData
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)

def requests_get_plan_data(cytxToken: str, planId: str, **kwargs) -> dict:
    """
    封装对接cytx接口，请求养老规划基本信息
    """
    try:
        logger.info("into requests_get_plan_data")
        logger.info("cytxToken: %s, planId: %s", cytxToken, planId)
        
        logger.info("kwargs: %s", kwargs)
        need_filter = kwargs.get("need_filter",True)
        
        
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        body = {
            "planId": planId,
            "channel": 1,
            "version": 1
        }
        
        logger.info("Request Body:\n%s", json.dumps(body))
        
        response = requests.post(cytx_api_getPlanData_url, headers=headers, json=body)
        if response.status_code != 200:
            logger.error("Failed to get plan data: %s", response.text)
            raise ValueError("response error")
        # logger.info("Plan Data:%s", json.dumps(response.json()))
        # 把返回数据中的data下的region字段
        try:
            respJson = response.json()
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %s", e)
            # return {"error": "Invalid JSON response"}
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        retData = respJson.get("data")
        retData.pop("region", None)
        
        # 2025-06-06 新增方法，遍历assetsList，把trendDTO和trendJson字段删除；遍历financeInfoList，把trendDTO和trendJson字段删除
        
        for assetsTypeAmount in retData.get("assetsTypeAmountList", []):
            for assets in assetsTypeAmount.get("assetsList", []):
                assets.pop("trendDTO", None)
                assets.pop("trendJson", None)


        if need_filter:
            for financeInfo in retData.get("financeInfoList", []):
                financeInfo.pop("trendDTO", None)
                financeInfo.pop("trendJson", None)
        
        logger.info("Plan Data:%s", json.dumps(retData))
        return retData
    except Exception as e:
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)
    
def requests_get_target_list(cytxToken: str, planId: str, self_cost_type: str, mate_cost_type: str) -> dict:
    """
    获取目标列表数据。

    该函数通过发送POST请求，获取指定计划下的目标列表数据，并根据自费类型和他费类型对数据进行处理。

    参数:
    - cytxToken: 用户令牌，用于身份验证。
    - planId: 计划ID，用于指定需要获取目标列表的计划。
    - self_cost_type: 自费类型，用于过滤目标列表。
    - mate_cost_type: 他费类型，用于过滤目标列表。

    返回:
    - 一个字典，包含处理后的目标列表数据。
    """
    try:
        logger.info("into requests_get_target_list")
        # 打印所有参数
        logger.info("cytxToken: %s, planId: %s, self_cost_type: %s, mate_cost_type: %s", cytxToken, planId,
                    self_cost_type, mate_cost_type)
        
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        
        # 初始化请求体，至少包含planId
        body = {
            "planId": planId
        }
        
        # 根据self_cost_type参数决定是否添加selfCostType到请求体
        if self_cost_type is not None:
            body["selfCostType"] = self_cost_type
        
        # 根据mate_cost_type参数决定是否添加mateCostType到请求体
        if mate_cost_type is not None:
            body["mateCostType"] = mate_cost_type
        
        logger.info("requests_get_target_list body:%s", json.dumps(body))
        
        # 发送POST请求到指定URL
        response = requests.post(cytx_api_getTargetList_url, headers=headers, json=body)
        
        # 检查响应状态码是否为200，否则抛出异常
        if response.status_code != 200:
            logger.error("Failed to get target list: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
            # logger.info("requests_get_target_list response:%s", json.dumps(respJson))
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        # 提取响应数据中的data部分
        retData = respJson.get("data")
        
        # 遍历selfTargetList下的subTargetList，删除trendDTO和trendJson字段
        for selfTarget in retData.get("selfTargetList", []):
            for subTarget in selfTarget.get("subTargetList", []):
                subTarget.pop("trendDTO", None)
                subTarget.pop("trendJson", None)
        
        # 遍历mateTargetList下的subTargetList，删除trendDTO和trendJson字段
        for mateTarget in retData.get("mateTargetList", []):
            for subTarget in mateTarget.get("subTargetList", []):
                subTarget.pop("trendDTO", None)
                subTarget.pop("trendJson", None)
        
        # 记录处理后的响应数据日志
        logger.info("requests_get_target_list response:%s", json.dumps(retData))
        
        # 返回处理后的数据
        return retData
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)

def requests_update_base_list(cytxToken, planId, planData):
    try:
        logger.info("into requests_update_base_list")
        # 打印所有参数
        logger.info("cytxToken: %s, planId: %s, planData: %s", cytxToken, planId, planData)
        
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        
        # 初始化请求体，至少包含planId
        body = planData
        
        logger.info("requests_update_base_list body:%s", json.dumps(body))
        
        # 发送POST请求到指定URL
        response = requests.post(cytx_api_saveBasicInfo_url, headers=headers, json=body)
        
        # 检查响应状态码是否为200，否则抛出异常
        if response.status_code != 200:
            logger.error("Failed to get target list: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
            # logger.info("requests_update_base_list response:%s", json.dumps(respJson))
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        logger.info("requests_update_base_list response:%s", json.dumps(respJson))
        
        # 返回处理后的数据
        return json.dumps({"status": "success"})
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)

def requests_update_insurance_list(cytxToken, planId, insurance_list_data):
    try:
        logger.info("into requests_update_insurance_list")
        # 打印所有参数
        logger.info("cytxToken: %s, planId: %s, insurance_list_data: %s", cytxToken, planId, insurance_list_data)
        
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        
        # 初始化请求体，至少包含planId
        body = {
            "agedReqList": insurance_list_data
        }
        
        logger.info("requests_update_insurance_list body:%s", json.dumps(body))
        
        # 根据self_cost_type参数决定是否添加selfCostType到请求体
        # if self_cost_type is not None:
        #     body["selfCostType"] = self_cost_type
        
        # 根据mate_cost_type参数决定是否添加mateCostType到请求体
        # if mate_cost_type is not None:
        #     body["mateCostType"] = mate_cost_type
        
        # 发送POST请求到指定URL
        response = requests.post(cytx_api_saveAgeInsurance_url, headers=headers, json=body)
        
        # 检查响应状态码是否为200，否则抛出异常
        if response.status_code != 200:
            logger.error("Failed to get target list: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        logger.info("requests_get_target_list response:%s", json.dumps(respJson))
        
        # 返回处理后的数据
        return json.dumps({"status": "success"})
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)

def requests_update_solutions_list(cytxToken, planId, solutions_list_data):
    try:
        logger.info("into requests_update_insurance_list")
        # 打印所有参数
        logger.info("cytxToken: %s, planId: %s, insurance_list_data: %s", cytxToken, planId, solutions_list_data)
        
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        
        # 初始化请求体，至少包含planId
        body = solutions_list_data
        
        body["planId"] = planId
        
        logger.info("requests_update_insurance_list body:%s", json.dumps(body))
        
        # 发送POST请求到指定URL
        response = requests.post(cytx_api_saveSolution_url, headers=headers, json=body)
        
        # 检查响应状态码是否为200，否则抛出异常
        if response.status_code != 200:
            logger.error("Failed to get target list: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        logger.info("requests_get_target_list response:%s", json.dumps(respJson))

        # 返回处理后的数据
        return json.dumps({"status": "success"})
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)

def requests_update_target_list(cytxToken, planId, target_list_data):
    try:
        logger.info("into requests_update_target_list")
        # 打印所有参数
        logger.info("cytxToken: %s, planId: %s, target_list_data: %s", cytxToken, planId, target_list_data)
        
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        
        # 初始化请求体，至少包含planId
        body = {
            "planId": planId,
            "selfCostType": target_list_data.get("selfCostType", None),
            "selfTargetList": target_list_data.get("selfTargetList", []),
            "mateTargetList": target_list_data.get("mateTargetList", [])
        }
        
        # 根据self_cost_type参数决定是否添加selfCostType到请求体
        # if self_cost_type is not None:
        #     body["selfCostType"] = self_cost_type
        
        # 根据mate_cost_type参数决定是否添加mateCostType到请求体
        # if mate_cost_type is not None:
        #     body["mateCostType"] = mate_cost_type
        
        logger.info("requests_update_target_list body:%s", json.dumps(body))
        
        # 发送POST请求到指定URL
        response = requests.post(cytx_api_saveTargetList_url, headers=headers, json=body)
        
        # 检查响应状态码是否为200，否则抛出异常
        if response.status_code != 200:
            logger.error("Failed to get target list: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        logger.info("requests_get_target_list response:%s", json.dumps(respJson))

        # 返回处理后的数据
        return json.dumps({"status": "success"})
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)


def requests_select_report(cytxToken, planId):
    try:
        logger.info("into requests_select_report")
        # 打印所有参数
        logger.info("cytxToken: %s, planId: %s", cytxToken, planId)
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        
        # 初始化请求体，至少包含planId
        body = {
            "planId": planId,
            "channel": 1,
            "version": 1
        }
        logger.info("requests_select_report body:%s", json.dumps(body))
        response = requests.post(cytx_api_select_report_url, headers=headers, json=body)
    
        if response.status_code != 200:
            logger.error("Failed to get target list: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        retData = respJson.get("data")
        logger.info("requests_select_report response:%s", json.dumps(retData))
        return retData
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)


def requests_calc_target_list(cytxToken, planId, target_list_data):
    try:
        logger.info("into requests_calc_target_list")
        # 打印所有参数
        logger.info("cytxToken: %s, planId: %s, target_list_data: %s", cytxToken, planId, target_list_data)
        
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        
        # 初始化请求体，至少包含planId
        body = {
            "planId": planId,
            "selfTargetList": target_list_data.get("selfTargetList", []),
            "mateTargetList": target_list_data.get("mateTargetList", [])
        }
        
        # 根据self_cost_type参数决定是否添加selfCostType到请求体
        # if self_cost_type is not None:
        #     body["selfCostType"] = self_cost_type
        
        # 根据mate_cost_type参数决定是否添加mateCostType到请求体
        # if mate_cost_type is not None:
        #     body["mateCostType"] = mate_cost_type
        
        logger.info("requests_calc_target_list body:%s", json.dumps(body))
        
        # 发送POST请求到指定URL
        response = requests.post(cytx_api_calc_target_list_url, headers=headers, json=body)
        
        # 检查响应状态码是否为200，否则抛出异常
        if response.status_code != 200:
            logger.error("Failed to get target list: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        retData = respJson.get("data")
        logger.info("requests_calc_target_list response:%s", json.dumps(retData))
        
        # 返回处理后的数据
        return retData
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)


def requests_get_plan_report(cytxToken, planId,finIncome):
    try:
        logger.info("into requests_get_plan_report")
        # 打印所有参数
        logger.info("cytxToken: %s, planId: %s,finIncome:%s", cytxToken, planId, finIncome)
        # 设置请求头，包括内容类型和身份验证信息
        headers = {
            "Content-Type": "application/json",
            "cytx-plan-app-token": cytxToken,
            "Authorization": "Bearer " + cytxToken
        }
        
        # 初始化请求体，至少包含planId
        body = {
            "planId": planId,
            "finIncome": finIncome
        }
        logger.info("requests_get_plan_report body:%s", json.dumps(body))
        response = requests.post(cytx_api_get_plan_report_url, headers=headers, json=body)
        
        if response.status_code != 200:
            logger.error("Failed to get target list: %s", response.text)
            raise ValueError("response error")
        try:
            # 尝试解析响应内容为JSON格式
            respJson = response.json()
        except json.JSONDecodeError as e:
            # 如果解析失败，记录错误日志并抛出异常
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000，否则抛出异常
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        retData = respJson.get("data")
        logger.info("requests_select_report response:%s", json.dumps(retData))
        return retData
    
    except Exception as e:
        # 捕获并记录任何异常，然后抛出ValueError异常
        logger.error("Error: %s", e)
        raise ValueError("Error: %s", e)
        
        
