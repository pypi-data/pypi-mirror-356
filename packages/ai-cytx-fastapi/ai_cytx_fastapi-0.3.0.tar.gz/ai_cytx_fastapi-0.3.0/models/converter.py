from typing import List, Optional
from dataclasses import asdict

from models.get_model import GetPlanDataResponse, AssetItem, FinanceInfo, PlanInfo as GetPlanInfo
from models.save_model import SaveModel, AssetsTypeAmountList, AssetsList, FinanceInfoList, PlanInfo


def convert_asset_item(asset: AssetItem) -> AssetsList:
    return AssetsList(
        amount=asset.amount,
        category=asset.category,
        desp=asset.name,
        end_age=asset.end_age,
        growth_rate=asset.growth_rate,
        has_must=asset.is_required,
        item_name=asset.type_code,
        owner_type=asset.owner_type,
        start_age=asset.start_age,
        vibration_rate=asset.volatility
    )


def convert_finance_info(finance: FinanceInfo) -> FinanceInfoList:
    return FinanceInfoList(
        amount=finance.amount,
        desp=finance.description,
        end_age=finance.end_age,
        growth_rate=finance.growth_rate,
        item_name=finance.item_type,
        owner_type=finance.owner_type,
        start_age=finance.start_age,
        has_must=finance.is_essential
    )


def convert_plan_info(plan_info: GetPlanInfo) -> PlanInfo:
    return PlanInfo(
        birth_date=plan_info.birth_date,
        child_num=plan_info.child_count,
        current_age=plan_info.age,
        edu_level=plan_info.education_level,
        industry_type=plan_info.industry,
        is_spouse=plan_info.include_spouse,
        location_social_security=plan_info.social_security_location,
        plan_name=plan_info.plan_name,
        sex=plan_info.gender,
        trend_type=plan_info.trend_type,
        work_hour=plan_info.work_hours,
        contribution_years=plan_info.contribution_years,
        first_pension_amt=plan_info.pension_amount,
        marital_status=plan_info.marital_status,
        mate_birth_date=plan_info.mate_birth_date,
        mate_child_num=plan_info.mate_child_count,
        mate_contribution_years=plan_info.mate_contribution_years,
        mate_edu_level=plan_info.mate_education_level,
        mate_first_pension_amt=plan_info.mate_pension_amount,
        mate_industry_type=plan_info.mate_industry_type,
        mate_location_social_security=plan_info.mate_social_security_location,
        mate_marital_status=plan_info.mate_marital_status,
        mate_pension_acc_amt=plan_info.mate_pension_balance,
        mate_sex=plan_info.mate_gender,
        mate_social_security_type=plan_info.mate_social_security_type,
        mate_target_city_name=plan_info.mate_retirement_city,
        mate_work_hour=plan_info.mate_work_hours,
        pension_acc_amt=plan_info.pension_balance,
        risk_level=plan_info.risk_profile,
        social_security_type=plan_info.social_security_type,
        target_city_name=plan_info.retirement_city
    )


def convert_get_to_save(get_data: GetPlanDataResponse) -> SaveModel:
    assets_type_amount_list = [
        AssetsTypeAmountList(
            assets_list=[convert_asset_item(asset) for asset in asset_group.items]
        )
        for asset_group in get_data.assets
    ] if get_data.assets else []

    finance_info_list = [convert_finance_info(finance) for finance in get_data.finances] if get_data.finances else []

    plan_info = convert_plan_info(get_data.plan_info) if get_data.plan_info else None

    return SaveModel(
        assets_type_amount_list=assets_type_amount_list,
        finance_info_list=finance_info_list,
        plan_info=plan_info
    )