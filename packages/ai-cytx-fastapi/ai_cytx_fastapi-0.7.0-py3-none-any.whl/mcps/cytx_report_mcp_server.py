import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

from mcp.server.fastmcp import FastMCP

from config.settings import report_mcp_server_host, report_mcp_server_port, report_mcp_name, report_mcp_log_name, \
    mcp_secret_key
from models.report_model import ReportModel, json_to_model
from services.common_utils import safe_json_loads, safe_get
from services.requests_service import requests_select_report, requests_get_plan_report, requests_calc_target_list, \
    requests_get_target_list

# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        TimedRotatingFileHandler(report_mcp_log_name, when="D", backupCount=7),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logging.getLogger("mcp.server.sse").setLevel(logging.DEBUG)

dependencies = [
    "websockets"
]

mcp = FastMCP(report_mcp_name, port=int(report_mcp_server_port), host=report_mcp_server_host, dependencies=dependencies)


@mcp.tool(name="getInfo", description="get")
def get_info(sk: str, cytxToken: str, planId: str) -> str:
    logger.info("into get_info")
    try:
        logger.info("Received parameters: sk=%s, cytxToken=%s, planId=%s", sk, cytxToken, planId)
        validate_str = validate_request(sk, cytxToken, planId)
        if validate_str is not None:
            return validate_str
        
        # 获取方案数据
        response_report_data = requests_select_report(cytxToken, planId)
        logger.info("response_report_data: %s", response_report_data)
        logger.info(type(response_report_data.get("jsonResult")))
        report_data_data = safe_json_loads(response_report_data.get("jsonResult"))
        logger.info(type(report_data_data))
        
        # 获取养老目标，计算养老目标，获取财务报告
        response_target_list = requests_get_target_list(cytxToken, planId, None, None)
        logger.info("response_target_list: %s", response_target_list)
        
        request_calc_target_list_str = {}
        request_calc_target_list_str["mateTargetList"] = response_target_list.get("mateTargetList", [])
        request_calc_target_list_str["selfTargetList"] = response_target_list.get("selfTargetList", [])
        request_calc_target_list_str["planId"] = planId
        
        logger.info("request_calc_target_list_str: %s", request_calc_target_list_str)
        
        response_calc_target_list = requests_calc_target_list(cytxToken, planId, request_calc_target_list_str)
        logger.info("calc_target_list: %s", response_calc_target_list)
        
        request_finIncome = safe_get(
            response_calc_target_list,
            path=["financialDetailsList", 0, "cashFlowList", 1, "amount"],
            default=0.0
        )
        logger.info("request_finIncome: %s", request_finIncome)
        response_plan_report = requests_get_plan_report(cytxToken, planId, request_finIncome)
        logger.info("response_plan_report: %s", response_plan_report)
        
        # 开始解析报告
        report_model = convert_report_to_model(report_data_data, target_list=response_target_list,
                                               calc_target_list=response_calc_target_list,
                                               plan_report=response_plan_report)
        
        logger.info("get_info return: %s", report_model.model_dump_json())
        return report_model.model_dump_json()
    
    except Exception as e:
        # 记录异常信息
        logger.error("Error: %s", e)
        return json.dumps({"error": "Internal server"})


def convert_report_to_model(report_data, *args, **kwargs) -> ReportModel:
    """
    将报告数据转换为模型
    """
    # 先匹配一遍，把完全相同的赋值一遍
    report_model = json_to_model(report_data)
    
    target_list = kwargs.get("target_list")
    calc_target_list = kwargs.get("calc_target_list")
    plan_report = kwargs.get("plan_report")
    
    # 然后手动处理有逻辑的
    report_model.num = get_report_num(report_data)
    report_model.gapAmount = calculate_gap_amount(report_model.payAmount, report_model.amount)
    
    current_age = target_list.get("currentAge")
    mate_current_age= target_list.get("mateCurrentAge",None)
    
    report_model.financialAssetCashFlowList = add_ages_to_cashflow(calc_target_list.get("financialAssetCashFlowList",[]), current_age,mate_current_age)
    report_model.financialDetailsList = add_age_to_nested_cashflow(calc_target_list.get("financialDetailsList",[]), current_age,mate_current_age)
    report_model.astCfgProp = plan_report.get("solutionData", []).get("astCfgProp", [])
    report_model.selfInsCalcData = plan_report.get("selfInsCalcData", [])
    report_model.mateInsCalcData = plan_report.get("mateInsCalcData", [])
    report_model.diagnosisData = plan_report.get("diagnosisData", [])
    
    # 计算百分比
    report_model.assetsTypeAmountList = calculate_assetstypeamountlist_percentages(report_model.assetsTypeAmountList)
    
    return report_model


@mcp.tool(name="getTemplate", description="template")
def get_template(sk: str) -> str:
    logger.info("into get_template")
    # 假设 cytx_report_mcp_server.py 所在目录下有一个 template 文件夹
    TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "template")
    
    # 校验 sk（根据你的需求保留）
    if sk != mcp_secret_key:
        logger.error("Invalid Secret Key")
        return "Invalid Secret Key"
    
    template_path = os.path.join(TEMPLATE_DIR, "template01.json")
    
    if not os.path.exists(template_path):
        logger.error("Template file not found: %s", template_path)
        return json.dumps({"error": "Template not found"})
    
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
        return template_content
    except Exception as e:
        logger.error("Error reading template file: %s", e)
        return json.dumps({"error": "Failed to read template"})

    


def get_report_num(report_data) -> int:
    """
    获取报告数字
    """
    curr_age = report_data.get("currAge")
    
    if curr_age >= 65:
        # 摔老期
        return 4
    elif curr_age >= 50:
        # 成熟期
        return 3
    elif curr_age >= 35:
        # 成长期
        return 2
    elif curr_age >= 25:
        # 形成期
        return 1
    elif curr_age >= 18:
        # 单身期
        return 0


def calculate_gap_amount(pay_amount: Optional[float], amount: Optional[float]) -> float:
    """
    计算金额差距
    """
    return (pay_amount or 0.0) - (amount or 0.0)


def calculate_assetstypeamountlist_percentages(items: list) -> list:
    """
    遍历列表，并在每个元素中添加 percent 字段，表示该元素 amount 占总量的百分比（字符串形式 + 百分号）。

    参数:
        items (list): 包含 "amount" 字段的字典列表

    返回:
        list: 修改后的列表，每个元素中包含新的 percent 字段（str 类型，带 %）
    """
    try:
        total = sum(float(item.amount) for item in items)
    except Exception as e:
        logger.warning("无法解析 amount 数据: %s", e)
        return items  # 返回原始数据，不添加 percent 字段

    if total == 0:
        return items  # 总金额为 0 时不计算百分比

    for item in items:
        amount = float(item.amount)
        percentage = round((amount / total) * 100, 2)
        item.percent = f"{percentage:.2f}%"  # 添加带百分号的字符串

    return items


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

def add_ages_to_cashflow(cash_flow_list, current_age, mate_current_age):
    """
    遍历现金流水列表，并根据初始年龄，为每一项添加 age 和（可选）mate_age 字段。

    :param cash_flow_list: 包含 year 字段的字典列表
    :param current_age: 用户当前年龄
    :param mate_current_age: 配偶当前年龄（可能为 None）
    :return: 增加了 age 和（可选）mate_age 字段的新列表
    """
    if not cash_flow_list or not isinstance(cash_flow_list, list):
        return []
    
    base_year = datetime.now().year  # 使用当前年份作为基准年
    result = []

    for item in cash_flow_list:
        year = int(item["year"])
        years_diff = year - base_year
        user_age = current_age + years_diff

        # 创建新字典并更新用户年龄
        new_item = item.copy()
        new_item["age"] = user_age

        # 判断是否添加配偶年龄
        if mate_current_age is not None:
            mate_age = mate_current_age + years_diff
            new_item["spouseAge"] = mate_age

        result.append(new_item)

    return result

from copy import deepcopy
from datetime import datetime


def add_age_to_nested_cashflow(nested_cashflow_list, current_age, mate_current_age=None):
    """
    遍历嵌套的现金流水列表，并根据初始年龄，为每个 cashFlowList 中的项添加 age 和（可选）spouseAge 字段。

    :param nested_cashflow_list: 包含多个 cashFlowList 的字典列表
    :param current_age: 用户当前年龄
    :param mate_current_age: 配偶当前年龄（可能为 None）
    :return: 增加了 age 和（可选）spouseAge 字段的新列表
    """
    if not nested_cashflow_list or not isinstance(nested_cashflow_list, list):
        return []

    result = []
    for item in nested_cashflow_list:
        # 深拷贝确保不影响原始数据
        item_copy = deepcopy(item)
        cash_flow_list = item_copy.get("cashFlowList", [])

        # 使用已有函数处理每个 cashFlowList
        updated_cash_flow = add_ages_to_cashflow(cash_flow_list, current_age, mate_current_age)

        # 替换为更新后的 cashFlowList
        item_copy["cashFlowList"] = updated_cash_flow
        result.append(item_copy)

    return result

def main():
    mcp.run()

if __name__ == "__main__":
    # Initialize and run the server
    main()
