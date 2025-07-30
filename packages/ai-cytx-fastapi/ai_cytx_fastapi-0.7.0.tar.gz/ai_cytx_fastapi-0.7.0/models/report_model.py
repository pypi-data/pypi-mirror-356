from pydantic import BaseModel
from typing import List, Optional
from services.common_utils import percent_to_float

class AgedTarget(BaseModel):
    endAge: int
    name: str
    startAge: int
    targetCost: float

class FinancialAssetCashFlow(BaseModel):
    amount: float
    year: int
    age: int | None
    spouseAge: int | None

class CashFlowItem(BaseModel):
    amount: float
    year: int
    age: int | None
    spouseAge: int | None

class FinancialDetailsItem(BaseModel):
    cashFlowList: List[CashFlowItem]
    cashFlowName: str

class AssetsTypeAmountItem(BaseModel):
    amount: float
    typeName: str
    percent: Optional[str] = None

class AstCfgPropItem(BaseModel):
    actCfgRt: float
    astCtgCode: str
    diffAmt: float
    rcmdCfgRt: float

class InsCalcDataItem(BaseModel):
    insuredAmount: float
    needAmount: float
    typeName: str

class SubIndicatorItem(BaseModel):
    name: str
    ratio: float
    reasonableRange: str
    score: float

class DiagnosisDataItem(BaseModel):
    indicator: float
    name: str
    subIndicators: List[SubIndicatorItem]
    warningInfo: str

class ReportModel(BaseModel):
    num:  Optional[int] = None
    agedTarget: List[AgedTarget] = None
    financialAssetCashFlowList: List[FinancialAssetCashFlow] = None
    financialDetailsList: List[FinancialDetailsItem] = None
    assetsTypeAmountList: List[AssetsTypeAmountItem] = None
    incomeAmount: float = None
    existAssetAmt: float = None
    pensionSocialAmount: float = None
    totalPostRetirementExpenses: float = None
    satisfaction: float = None
    financialAssetOnRetireYear: float = None
    totalFinancialGapSinceRetireYear: float = None
    payAmount: float = None
    amount: float = None
    gapAmount: float = None
    agedTotalCost: float = None
    initialAssetsSolution: float = None
    periodInvestSolution: float = None
    beforeRetireRate: float = None
    afterRetireRate: float = None
    astCfgProp: List[AstCfgPropItem] = None
    selfInsCalcData: List[InsCalcDataItem] = None
    mateInsCalcData: List[InsCalcDataItem] = None
    diagnosisData: List[DiagnosisDataItem] = None


def json_to_model(json_data: dict) -> ReportModel:
    """
    将原始 JSON 数据转换为 ReportModel 实例。

    :param json_data: 输入的原始 JSON 字典
    :return: ReportModel 实例
    """
    # 手动处理可能为字符串的数值字段
    for item in json_data.get("agedTarget", []):
        if isinstance(item.get("targetCost"), str):
            item["targetCost"] = float(item["targetCost"])
    
    if isinstance(json_data.get("agedTotalCost"), str):
        json_data["agedTotalCost"] = float(json_data["agedTotalCost"])
    if isinstance(json_data.get("amount"), str):
        json_data["amount"] = float(json_data["amount"])
    if isinstance(json_data.get("gapAmount"), str):
        json_data["gapAmount"] = float(json_data["gapAmount"])
    if isinstance(json_data.get("payAmount"), str):
        json_data["payAmount"] = float(json_data["payAmount"])
    if isinstance(json_data.get("satisfaction"), str):
        json_data["satisfaction"] = percent_to_float(json_data.get("satisfaction"))
    
    # 使用 model_validate 自动匹配字段并构建模型
    return ReportModel.model_validate(json_data)
