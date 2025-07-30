import copy
import json
import logging
from typing import Dict, Any, List

import requests
from deepmerge import Merger, always_merger

from config.settings import cytx_api_url
from models.command_model import CommandModel
from services.requests_service import requests_get_solution, requests_get_insurance, requests_get_plan_data, \
    requests_update_target_list, requests_update_base_list, requests_update_insurance_list, \
    requests_update_solutions_list, requests_get_target_list

cytx_api_getPlanData_url = cytx_api_url + "/api/aged/getPlanData"
cytx_api_getAgedInsurance_url = cytx_api_url + "/api/aged/getAgedInsurance"
cytx_api_getTargetList_url = cytx_api_url + "/api/aged/getTargetList"
cytx_api_getSolution_url = cytx_api_url + "/api/aged/getSolution"
cytx_api_saveBasicInfo_url = cytx_api_url + "/api/aged/saveBasicInfo"
cytx_api_saveAgeInsurance_url = cytx_api_url + "/api/aged/saveAgeInsurance"
cytx_api_saveTargetList_url = cytx_api_url + "/api/aged/saveTargetList"
cytx_api_saveSolution_url = cytx_api_url + "/api/aged/saveSolution"

logger = logging.getLogger(__name__)

class MCPService:
    
    def __init__(self):
        pass
    
    @staticmethod
    def find_data_by_type_new(data_type: str, data: dict, owner_type: str, data_id: str | None,
                          work_type: str | None) :
        """
        根据资产代码查找资产信息
        :param data_type: 资产代码，格式为 "1-1-6"
        :param data: 包含资产信息的 JSON 数据
        :return: 找到的资产信息，如果没有找到则返回 None
        """
        if data_type == '0':
            data_type = "0-0-0"
        # 解析资产代码
        category, type_code, item_name = map(int, data_type.split('-'))
        # 查找对应的资产类型
        if category == 1:
            logger.info("find_data_by_type_new: category == 1")
            returnList = []
            parent = None
            # 如果 type_code == 0 且 item_name == 0，表示返回所有资产类型下的资产列表
            if type_code == 0 and item_name == 0:
                for asset_type in data.get('assetsTypeAmountList', []):
                    parent = asset_type.get('assetsList', [])
                    for idx, asset in enumerate(parent):
                        if str(asset.get('ownerType')) == str(owner_type):
                            returnList.append([asset, parent, idx])
                if not returnList:
                    return [[None, parent, None]]
                return returnList
            
            # 遍历资产类型列表，查找匹配 type_code 的项
            for asset_type in data.get('assetsTypeAmountList', []):
                asset_type_code = asset_type.get('type')
                if asset_type_code != type_code:
                    continue
                parent = asset_type.get('assetsList', [])
                # 如果 item_name == 0，则返回该类型下所有资产
                if item_name == 0:
                    for idx, asset in enumerate(parent):
                        if str(asset.get('ownerType')) == str(owner_type):
                            returnList.append([asset, parent, idx])
                    break  # 找到对应 type_code 后无需继续遍历
                else:
                    # 否则按 itemName 和 ownerType 匹配具体资产
                    for idx, asset in enumerate(parent):
                        if asset.get('itemName') != item_name or str(asset.get('ownerType')) != str(owner_type):
                            continue
                        
                        if data_id is not None:
                            if str(asset.get('id')) == str(data_id):
                                logger.info(f"Found asset: {json.dumps(asset)}")
                                returnList.append([asset, parent, idx])
                            elif asset.get('houseAssetsList') and work_type == 'update':
                                for house_asset in asset.get('houseAssetsList', []):
                                    if str(house_asset.get('id')) == str(data_id):
                                        logger.info(f"Found house asset: {json.dumps(house_asset)}")
                                        returnList.append([asset, parent, idx])
                        elif data_id is None:
                            logger.info(f"Found asset: {json.dumps(asset)}")
                            returnList.append([asset, parent, idx])
            
            if not returnList:
                return [[None, parent, None]]
            return returnList
        elif category == 2:
            logger.info("find_data_by_type_new:category == 2")
            parent = data.get('financeInfoList')
            returnList = []
            for idx,finance in enumerate(parent):
                if finance.get('itemName') == type_code and str(finance.get('ownerType')) == str(owner_type):
                    # 转换为字符串并打印
                    logger.info(f"Found finance info: {json.dumps(finance)}")
                    returnList.append([finance,parent,idx])
            if len(returnList) == 0:
                logger.error("Error: No matching finance info found")
                returnList.append([None, parent, None])
            return returnList
        
        elif category == 0:
            logger.info("find_data_by_type_new:category == 0")
            # 返回planInfo
            return [[data.get('planInfo'),None,None]]
        elif category == 3:
            logger.info("find_data_by_type_new: category == 3")
            # 根据 owner_type 获取对应的目标列表
            if int(owner_type) == 0:
                targets_lists = data.get('selfTargetList', [])
            elif int(owner_type) == 1:
                targets_lists = data.get('mateTargetList', [])
            else:
                targets_lists = []
            returnList = []
            parent = None
            
            for targets in targets_lists:
                # 全匹配：type_code 和 item_name 都为 0 时返回所有子目标
                if type_code == 0 and item_name == 0:
                    parent = targets.get('subTargetList', [])
                    for idx, subTarget in enumerate(parent):
                        returnList.append([subTarget, parent, idx])
                # 匹配 targetType 相同的项
                elif targets.get('targetType') == type_code:
                    parent = targets.get('subTargetList', [])
                    for idx, subTarget in enumerate(parent):
                        if subTarget.get('targetType') != type_code:
                            continue
                        # 不需要 item_name 匹配的情况
                        if item_name == 0:
                            if data_id is None or str(subTarget.get('id')) == str(data_id):
                                returnList.append([subTarget, parent, idx])
                        # 需要 item_name 匹配的情况
                        elif str(subTarget.get('targetMinType')) == str(item_name):
                            if data_id is None or str(subTarget.get('id')) == str(data_id):
                                returnList.append([subTarget, parent, idx])
            
            # 如果没有找到任何匹配项，返回 [None, parent, None]
            if not returnList:
                return [[None, parent, None]]
            return returnList
        elif category == 4:
            logger.info("find_data_by_type_new: category == 4")
            returnList = []
            parent = None
            # 遍历所有保险数据
            for insurance_lists in data:
                # 匹配 ownerType
                if str(insurance_lists.get('ownerType')) != str(owner_type):
                    continue
                # 获取保险类型列表
                for insurance_list in insurance_lists.get('insuranceTypeList', []):
                    insurance_type = insurance_list.get('type')
                    # 如果 type_code == 0 且 item_name == 0，则返回该类型下所有保险
                    if type_code == 0 and item_name == 0:
                        parent = insurance_list.get('insuranceList', [])
                        for idx, insurance in enumerate(parent):
                            returnList.append([insurance, parent, idx])
                        continue  # 跳过下面的 type_code 判断
                    
                    if str(insurance_type) != str(type_code):
                        continue
                    parent = insurance_list.get('insuranceList', [])
                    # 遍历保险列表进行匹配
                    for idx, insurance in enumerate(parent):
                        if insurance.get('type') != type_code:
                            continue
                        # 根据 data_id 匹配
                        if data_id is not None and str(insurance.get('id')) != str(data_id):
                            continue
                        # 添加匹配结果
                        returnList.append([insurance, parent, idx])
            
            # 如果没有找到任何匹配项，返回 [None, None, None]
            if not returnList:
                return [[None, parent, None]]
            return returnList
        elif category == 5:
            logger.info("find_data_by_type_new:category == 5")
            # 返回planInfo
            return [[data,None,None]]
    
    @staticmethod
    def handle_add_logic(command_model: CommandModel, planData: List[Dict[str, Any]]):
        """
        处理添加逻辑

        根据command_model中的数据更新planData列表中的字典数据
        如果command_model.data为空，则抛出ValueError异常

        参数:
        - command_model: CommandModel实例，包含命令信息
        - planData: 包含计划数据的列表，每个元素是一个字典

        返回:
        - 更新后的planData列表
        """
        # 记录处理添加逻辑的开始
        logger.info(f"Handling add logic for command: {command_model.command}")
        
        # 检查command_model.data是否为空
        if command_model.data is None:
            logger.error("Error: command_model.data is None")
            # 抛出异常
            raise ValueError("Error: command_model.data is None")
        
        # 根据类型查找需要更新的数据
        find_result = MCPService.find_data_by_type_new(command_model.type, planData,
                                                                           command_model.ownerType, command_model.id,
                                                                           'add')
        to_update_data, parentList, idx = find_result[0]
        
        # 根据类型和条件决定是合并数据还是直接添加
        if command_model.type == "2-1-1" and to_update_data is not None and command_model.data.get(
                "desp") == "工作收入":
            # 工作收入单独处理 金额相加
            to_update_data["amount"] = to_update_data["amount"] + command_model.data["amount"]
            parentList[idx] = to_update_data
            
        elif parentList is not None:
            parentList.append(command_model.data)
        
        # 记录合并后的数据
        logger.info("Merged Data:\n%s", json.dumps(parentList))
        
        # 记录更新后的planData
        logger.info("planData Data:\n%s", json.dumps(planData))
        
        # 返回更新后的planData
        return planData
    
    @staticmethod
    def handle_update_logic(command_model: CommandModel, planData: List[Dict[str, Any]]):
        """
        处理更新逻辑

        根据command_model中的数据更新planData列表中的字典数据
        如果command_model.data为空，则抛出ValueError异常

        参数:
        - command_model: CommandModel实例，包含命令信息
        - planData: 包含计划数据的列表，每个元素是一个字典

        返回:
        - 更新后的planData列表
        """
        # 记录处理更新逻辑的开始
        logger.info(f"Handling update logic for command: {command_model.command}")
        
        # 检查command_model.data是否为空
        if command_model.data is None:
            logger.error("Error: command_model.data is None")
            # 抛出异常
            raise ValueError("Error: command_model.data is None")
        
        # 根据类型查找需要更新的数据
        find_result = MCPService.find_data_by_type_new(command_model.type, planData,
                                                                           command_model.ownerType, command_model.id,
                                                                           'update')
        # 因为收入和支出没有ID，所以要根据收入和支出的序号来进行更新
        if command_model.command=='update' and (command_model.type == "2-1-1" or command_model.type == "2-4-1"):
            to_update_data, parentList, idx = find_result[int(command_model.id)]
        else:
            to_update_data, parentList, idx = find_result[0]
        
        if to_update_data is not None:
            
            # 根据类型和条件决定是合并数据还是直接更新
            if command_model.type == "2-1-1" and command_model.data.get("desp") == "工作收入":
                # 工作收入单独处理 金额相加
                # to_update_data["amount"] = to_update_data["amount"] + command_model.data["amount"]
                # merged_data = to_update_data
                merged_data = always_merger.merge(to_update_data, command_model.data)
            
            elif command_model.type == "1-5-14":
                # 其他收入单独处理 金额相加
               merged_data = merge_list_only(to_update_data, command_model.data,"houseAssetsList")
            else:
                # 执行更新操作
                merger = Merger(
                    [(list, ["append"]), (dict, ["merge"])],
                    ["override"],
                    ["override"]
                )
                merged_data = merger.merge(to_update_data, command_model.data)
            # 记录合并后的数据
            logger.info("Merged Data:%s", json.dumps(merged_data))
            if parentList is not None and idx is not None:
                parentList[idx] = merged_data
            # 记录更新后的planData
            logger.info("cytx_api_saveBasicInfo_url request:%s", planData)
            return planData
        else:
            logger.error("Error: to_update_data is None")
            # 抛出异常
            raise ValueError("Error: to_update_data is None")
    
    @staticmethod
    def handle_delete_logic(command_model: CommandModel, planData: List[Dict[str, Any]]):
        """
        处理删除逻辑

        根据command_model中的数据更新planData列表中的字典数据
        目前此函数未实现任何逻辑，直接返回planData

        参数:
        - command_model: CommandModel实例，包含命令信息
        - planData: 包含计划数据的列表，每个元素是一个字典

        返回:
        - 未修改的planData列表
        """
        # 记录处理删除逻辑的开始
        logger.info(f"Handling delete logic for command: {command_model.command}")
        # 直接返回planData，未执行任何逻辑
        return planData
    
    
    
    @staticmethod
    def handle_merge_logic(merge_json, cytxToken, planId):
        logger.info(f"Handling merge logic")
        # 打印全部参数
        logger.info("Received parameters: save_model=%s, cytxToken=%s, planId=%s", merge_json, cytxToken, planId)
        # 获取基本信息
        try:
            planData = requests_get_plan_data(cytxToken, planId)
        except Exception as e:
            logger.error("Error: %s", e)
            # 抛出异常
            raise ValueError("Error: %s", e)
        # 逻辑分别处理 1.处理基础信息（相同字段更新）  2.处理资产信息（所有资产，每种类型都新增） 3.处理财务信息（财务信息，收入支出都新增）
        
        merge_plan_info = merge_json.get("planInfo")
        merge_fiannce_info = merge_json.get("financeInfoList")
        merge_assets_type_amount_list = merge_json.get("assetsTypeAmountList")
        
        logger.info("merge_plan_data:\n%s", json.dumps(merge_plan_info))
        logger.info("merge_fiannce_info:\n%s", json.dumps(merge_fiannce_info))
        logger.info("merge_assets_type_amount_list:\n%s", json.dumps(merge_assets_type_amount_list))
        # 先把原有数据复制一份
        old_plan_data = copy.deepcopy(planData)
        old_plan_info = old_plan_data.get("planInfo")
        old_fiannce_info = old_plan_data.get("financeInfoList")
        old_assets_type_amount_list = old_plan_data.get("assetsTypeAmountList")
        
        logger.info("old_plan_data:\n%s", json.dumps(old_plan_data))
        logger.info("old_plan_info:\n%s", json.dumps(old_plan_info))
        logger.info("old_fiannce_info:\n%s", json.dumps(old_fiannce_info))
        logger.info("old_assets_type_amount_list:\n%s", json.dumps(old_assets_type_amount_list))
        
        old_plan_info = always_merger.merge(old_plan_info, merge_plan_info)
        merger = Merger(
            [(list, ["append"]), (dict, ["merge"])],
            ["override"],
            ["override"]
        )
        old_fiannce_info = merger.merge(old_fiannce_info,  merge_fiannce_info)
        old_assets_type_amount_list = MCPService.merge_assets_type_amount_lists(old_assets_type_amount_list,  merge_assets_type_amount_list)
        
        logger.info("aftermerge old_plan_data:\n%s", json.dumps(old_plan_data))
        logger.info("aftermerge old_plan_info:\n%s", json.dumps(old_plan_info))
        logger.info("aftermerge old_fiannce_info:\n%s", json.dumps(old_fiannce_info))
        logger.info("aftermerge old_assets_type_amount_list:\n%s", json.dumps(old_assets_type_amount_list))
        
        old_plan_data["planInfo"] = old_plan_info
        old_plan_data["financeInfoList"] = old_fiannce_info
        old_plan_data["assetsTypeAmountList"] = old_assets_type_amount_list
        
        logger.info("aftermerge old_plan_data:\n%s", json.dumps(old_plan_data))
        
        response = requests.post(cytx_api_saveBasicInfo_url, headers=headers, json=old_plan_data)
        
        logger.info("Response:\n%s", response.json())
        
        if response.status_code != 200:
            logger.error("Failed to save basic info: %s", response.text)
            raise ValueError("Failed to save basic info: %s", response.text)
        
        # 把返回数据中的data下的region字段
        try:
            respJson = response.json()
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %s", e)
            raise ValueError("JSON decode error: %s", e)
        
        # 判断respJson的code是否等于10000
        if respJson.get("code") != '10000':
            logger.error("Error: %s", respJson.get("message"))
            raise ValueError("Error: %s", respJson.get("message"))
        
        return json.dumps({"status": "OK"})
    
    @staticmethod
    def merge_asset_lists(base_assets, new_assets):
        """
        合并两个 assetList 列表，基于 id 字段进行匹配更新或追加
        :param base_assets: 原始资产列表（list）
        :param new_assets: 新增/修改的资产列表（list）
        :return: 合并后的资产列表
        """
        # 构建 id -> asset 的映射表
        base_map = {asset["id"]: asset for asset in base_assets}
        new_map = {asset["id"]: asset for asset in new_assets}
        
        # 更新已有资产 or 添加新资产
        merged = []
        for asset_id, base_asset in base_map.items():
            if asset_id in new_map:
                # ID 相同，执行字段合并（你可以换成 deepmerge 或手动处理）
                updated_asset = {**base_asset, **new_map[asset_id]}
                merged.append(updated_asset)
            else:
                merged.append(base_asset)
        
        # 添加新资产中独有的部分
        for asset_id, new_asset in new_map.items():
            if asset_id not in base_map:
                merged.append(new_asset)
        
        return merged
    
    @staticmethod
    def merge_assets_type_amount_lists(base_list, new_list):
        """
        合并 assetsTypeAmountList 列表
        :param base_list: 原始 assetsTypeAmountList 数据
        :param new_list: 新增/修改的 assetsTypeAmountList 数据
        :return: 合并后的 assetsTypeAmountList
        """
        # 构建 type -> assetsTypeAmountList 项 的映射
        base_map = {item["type"]: item for item in base_list}
        new_map = {item["type"]: item for item in new_list}
        
        merged_list = []
        
        # 遍历所有 type
        all_types = set(base_map.keys()).union(set(new_map.keys()))
        
        for asset_type in all_types:
            base_type_item = base_map.get(asset_type, {})
            new_type_item = new_map.get(asset_type, {})
            
            # 如果 base 中没有这个 type，直接复制 new 中的整个 type 条目
            if asset_type not in base_map:
                merged_list.append(copy.deepcopy(new_type_item))
                continue
            
            # 如果 new 中没有这个 type，保留 base 中的原始内容
            if asset_type not in new_map:
                merged_list.append(copy.deepcopy(base_type_item))
                continue
            
            # 类型都存在，需要合并 assetsList
            base_asset_list = base_type_item.get("assetsList", [])
            new_asset_list = new_type_item.get("assetsList", [])
            
            merged_asset_list = MCPService.merge_asset_lists(base_asset_list, new_asset_list)
            
            # 构造新的 type 条目，保留其他字段不变，只替换 assetList
            merged_type_item = copy.deepcopy(base_type_item)
            merged_type_item["assetsList"] = merged_asset_list
            
            merged_list.append(merged_type_item)
        
        return merged_list
    
    
    
    @staticmethod
    def update_base_list(command_models: List[CommandModel], cytxToken: str, planId: str) -> str:
        """
        更新基础列表数据。

        该方法根据提供的命令模型列表、用户令牌和计划ID，获取并更新用户的基础列表数据。
        它通过检查每个命令模型的类型和指令来决定是添加、更新还是删除数据。

        参数:
        - command_models: 一个CommandModel对象列表，包含要处理的命令。
        - cytxToken: 用户的认证令牌。
        - planId: 用户的计划ID。

        返回:
        - 一个字符串，表示更新结果。
        """
        try:
            logger.info("into update_base_list")
            # 打印所有参数
            logger.info("cytxToken: %s, planId: %s", cytxToken, planId)
            # 获取用户的基础列表数据
            base_list_data = requests_get_plan_data(cytxToken, planId)
            
            # 遍历每个命令模型
            for command_model in command_models:
                command_command = command_model.command
                
                # 处理特定类型的命令模型
                if command_model.type == "1-46-46":
                    # 个人养老金只能有一个
                    command_command = MCPService.get_new_command(command_model, base_list_data)
                
                # 根据命令执行相应的逻辑
                if command_command == "add":
                    # 调用新增逻辑处理方法
                    base_list_data = MCPService.handle_add_logic(command_model, base_list_data)
                elif command_command == "update":
                    # 调用更新逻辑处理方法
                    base_list_data = MCPService.handle_update_logic(command_model, base_list_data)
                elif command_command == "delete":
                    # 调用删除逻辑处理方法
                    base_list_data = MCPService.handle_delete_logic(command_model, base_list_data)
            
            # 返回更新结果
            return requests_update_base_list(cytxToken, planId, base_list_data)
        except Exception as e:
            # 捕获并记录任何异常，然后抛出ValueError异常
            logger.error("Error: %s", e)
            raise ValueError("Error: %s", e)
    
    @staticmethod
    def update_target_list(command_models: List[CommandModel], cytxToken: str, planId: str) -> str:
        """
        更新目标列表。

        根据提供的命令模型列表和认证令牌、计划ID，来更新目标列表。这个方法主要通过解析每个命令模型，
        并根据模型中的命令类型（如添加、更新、删除）来调用相应的处理逻辑，最终更新目标列表。

        参数:
        - command_models: CommandModel 的列表，每个模型包含一个命令和相关数据。
        - cytxToken: 认证令牌，用于验证请求。
        - planId: 计划ID，标识特定的计划。

        返回:
        - str: 更新后的目标列表的相关信息。
        """
        try:
            # 记录进入更新目标列表函数的日志
            logger.info("into update_target_list")
            # 打印所有参数
            logger.info("cytxToken: %s, planId: %s", cytxToken, planId)
            # 获取当前目标列表数据
            target_list_data = requests_get_target_list(cytxToken, planId, None, None)
            
            # 遍历命令模型列表，处理每个命令模型
            for command_model in command_models:
                # 获取当前命令模型的命令类型
                command_command = command_model.command
                # 根据命令类型，执行相应的逻辑
                if command_command == "add":
                    # 调用新增逻辑处理方法
                    target_list_data = MCPService.handle_target_add_logic(command_model, target_list_data)
                elif command_command == "update":
                    # 调用更新逻辑处理方法
                    target_list_data = MCPService.handle_target_update_logic(command_model, target_list_data)
                elif command_command == "delete":
                    # 调用删除逻辑处理方法
                    target_list_data = MCPService.handle_target_delete_logic(command_model, target_list_data)
            
            # 更新目标列表后，返回更新后的目标列表的相关信息
            return requests_update_target_list(cytxToken, planId, target_list_data)
        except Exception as e:
            # 捕获并记录任何异常，然后抛出ValueError异常
            logger.error("Error: %s", e)
            raise ValueError("Error: %s", e)
    
    @staticmethod
    def update_insurance_list(command_models: List[CommandModel], cytxToken: str, planId: str) -> str:
        """
        更新保险列表

        该方法根据提供的命令模型列表、用户令牌和计划ID来更新保险列表它首先获取当前的保险列表数据，
        然后根据每个命令模型的指令（添加、更新或删除）来修改保险列表最后，它将更新后的保险列表数据
        发送回服务器

        参数:
        - command_models: CommandModel的列表，包含要执行的命令
        - cytxToken: 用户的认证令牌
        - planId: 保险计划的ID

        返回:
        - str: 更新保险列表后的响应
        """
        try:
            # 记录进入方法的日志
            logger.info("into update_insurance_list")
            # 打印所有参数
            logger.info("cytxToken: %s, planId: %s", cytxToken, planId)
            # 获取当前的保险列表数据
            insurance_list_data = requests_get_insurance(cytxToken, planId)
            # 遍历每个命令模型
            for command_model in command_models:
                command_command = command_model.command
                
                # 根据命令模型的类型处理医疗险
                if command_model.type == "4-1-0":
                    command_command = MCPService.get_new_command(command_model, insurance_list_data)
                # 根据指令执行相应的操作
                if command_command == "add":
                    # 调用新增逻辑处理方法
                    insurance_list_data = MCPService.handle_insurance_add_logic(command_model, insurance_list_data)
                elif command_command == "update":
                    # 调用更新逻辑处理方法
                    insurance_list_data = MCPService.handle_insurance_update_logic(command_model, insurance_list_data)
                elif command_command == "delete":
                    # 调用删除逻辑处理方法
                    insurance_list_data = MCPService.handle_insurance_delete_logic(command_model, insurance_list_data)
            # 返回更新保险列表后的响应
            return requests_update_insurance_list(cytxToken, planId, insurance_list_data)
        except Exception as e:
            # 捕获并记录任何异常，然后抛出ValueError异常
            logger.error("Error: %s", e)
            raise ValueError("Error: %s", e)
    
    @staticmethod
    def get_new_command(command_model: CommandModel, list_data: List[Dict[str, Any]]) -> None:
        """
        根据命令模型和列表数据确定是更新还是添加新命令。

        此函数通过检查给定类型和所有者类型的命令是否存在于列表数据中来决定。
        如果存在，则返回"update"，否则返回"add"。

        参数:
        - command_model: CommandModel实例，包含命令的相关信息。
        - list_data: 包含命令数据的列表，每个命令数据都是一个字典。

        返回:
        - 如果找到匹配的命令数据，则返回"update"，否则返回"add"。
        """
        try:
            # 记录日志，表示开始进入get_new_command函数
            logger.info("into get_new_command")
            # 根据命令模型的类型、所有者类型和ID在列表数据中查找匹配的数据
            find_result = MCPService.find_data_by_type_new(command_model.type, list_data,
                                                                        command_model.ownerType, command_model.id, None)
            update_data, parent, idx = find_result[0]
            # 如果找到匹配的数据，则返回"update"，否则返回"add"
            if update_data is not None:
                return "update"
            else:
                return "add"
        except Exception as e:
            # 捕获并记录任何异常，然后抛出ValueError异常
            logger.error("Error: %s", e)
            raise ValueError("Error: %s", e)
    
    @staticmethod
    def update_solutions_list(command_models: List[CommandModel], cytxToken: str, planId: str) -> str:
        """
        更新解决方案列表。

        根据提供的命令模型列表和认证令牌、计划ID，更新解决方案列表数据，并将其更新到服务器。

        参数:
        - command_models: CommandModel的列表，包含要处理的命令。
        - cytxToken: 用户的认证令牌。
        - planId: 计划的唯一标识符。

        返回:
        - str: 服务器返回的响应。
        """
        try:
            # 记录进入update_solutions_list函数的日志
            logger.info("into update_solutions_list")
            # 打印所有参数
            logger.info("cytxToken: %s, planId: %s", cytxToken, planId)
            # 获取当前解决方案列表数据
            solutions_list_data = requests_get_solution(cytxToken, planId)
            # 遍历命令模型列表，处理每个命令
            for command_model in command_models:
                command_command = command_model.command
                # 根据命令类型调用相应的处理逻辑
                solutions_list_data = MCPService.handle_solutions_add_logic(command_model, solutions_list_data)
                # if command_command == "add":
                # 调用新增逻辑处理方法
                # solutions_list_data = MCPService.handle_solutions_add_logic(command_model, solutions_list_data)
                # elif command_command == "update":
                # 调用更新逻辑处理方法
                # solutions_list_data = MCPService.handle_solutions_update_logic(command_model, solutions_list_data)
                # elif command_command == "delete":
                # 调用删除逻辑处理方法
                # solutions_list_data = MCPService.handle_solutions_delete_logic(command_model, solutions_list_data)
            # 将更新后的解决方案列表数据发送到服务器
            return requests_update_solutions_list(cytxToken, planId, solutions_list_data)
        except Exception as e:
            # 捕获并记录任何异常，然后抛出ValueError异常
            logger.error("Error: %s", e)
            raise ValueError("Error: %s", e)
    
    def handle_target_add_logic(command_model: CommandModel, target_list_data: List[Dict[str, Any]]):
        """
        处理目标添加逻辑的函数。

        参数:
        - command_model: CommandModel类型，包含要添加的数据及其相关元信息。
        - target_list_data: 包含目标数据的列表，数据类型为List[Dict[str, Any]]。

        返回:
        - 更新后的target_list_data列表。

        此函数首先检查command_model.data是否为None，如果是，则记录错误日志并抛出异常。
        然后调用MCPService.find_data_by_type_new函数查找相关数据，如果parentList为None，
        则记录错误日志并抛出异常。最后将command_model.data添加到parentList中，并记录合并后的数据。
        """
        logger.info("into handle_target_add_logic")
        
        if command_model.data is None:
            logger.error("Error: command_model.data is None")
            # 抛出异常
            raise ValueError("Error: command_model.data is None")
        
        find_result = MCPService.find_data_by_type_new(command_model.type, target_list_data,
                                                                           command_model.ownerType, command_model.id,
                                                                           'add')
        to_update_data, parentList, key = find_result[0]
        
        if parentList is None:
            logger.error("Error: parentList is None")
            # 抛出异常
            raise ValueError("Error: parentList is None")
        
        parentList.append(command_model.data)
        
        logger.info("Merged Data:\n%s", json.dumps(parentList))
        
        return target_list_data
    
    def handle_target_update_logic(command_model: CommandModel, target_list_data: List[Dict[str, Any]]):
        """
        处理目标更新逻辑的函数。

        参数:
        - command_model: CommandModel类型，包含要更新的数据及其相关元信息。
        - target_list_data: 包含目标数据的列表，数据类型为List[Dict[str, Any]]。

        返回:
        - 更新后的target_list_data列表。

        此函数首先检查command_model.data是否为None，如果是，则记录错误日志并抛出异常。
        然后调用MCPService.find_data_by_type_new函数查找相关数据，如果to_update_data为None，
        则记录错误日志并抛出异常。最后使用Merger类合并数据，并记录合并后的数据。
        """
        logger.info("into handle_target_add_logic")
        if command_model.data is None:
            logger.error("Error: command_model.data is None")
            # 抛出异常
            raise ValueError("Error: command_model.data is None")
        
        find_result = MCPService.find_data_by_type_new(command_model.type, target_list_data,
                                                                           command_model.ownerType, command_model.id,
                                                                           'update')
        
        to_update_data, parentList, key = find_result[0]

        if to_update_data is not None:
            # 执行更新操作
            merger = Merger(
                [(list, ["append"]), (dict, ["merge"])],
                ["override"],
                ["override"]
            )
            merged_data = merger.merge(to_update_data, command_model.data)
            logger.info("Merged Data:\n%s", json.dumps(merged_data))
            
            return target_list_data
        else:
            logger.error("Error: to_update_data is None")
            # 抛出异常
            raise ValueError("Error: to_update_data is None")
    
    def handle_target_delete_logic(command_model: CommandModel, target_list_data: List[Dict[str, Any]]):
        """
        处理目标删除逻辑的函数。

        参数:
        - command_model: CommandModel类型，包含要删除的数据及其相关元信息。
        - target_list_data: 包含目标数据的列表，数据类型为List[Dict[str, Any]]。

        返回:
        - 更新后的target_list_data列表。

        此函数目前仅记录了进入处理目标删除逻辑的日志，实际删除逻辑未实现。
        """
        logger.info("into handle_target_delete_logic")
        return target_list_data
    
    
    
    def handle_insurance_add_logic(command_model: CommandModel, insurance_list_data: List[Dict[str, Any]]):
        """
        处理保险添加逻辑的函数。

        参数:
        - command_model: CommandModel实例，包含要添加的数据及其元数据。
        - insurance_list_data: 保险数据列表，用于更新和参考。

        返回:
        - 更新后的保险数据列表。

        此函数首先检查command_model中的数据是否为空，如果为空则记录错误并抛出异常。
        然后调用MCPService.find_data_by_type_new函数根据类型和其他条件查找相关数据。
        如果找到的parentList为空，记录错误并抛出异常。
        最后，将command_model中的数据添加到parentList中，并记录合并后的数据。
        """
        logger.info("into handle_insurance_add_logic")
        
        if command_model.data is None:
            logger.error("Error: command_model.data is None")
            # 抛出异常
            raise ValueError("Error: command_model.data is None")
        
        find_result = MCPService.find_data_by_type_new(command_model.type, insurance_list_data,
                                                                           command_model.ownerType,
                                                                           command_model.id, 'add')
        
        to_update_data, parentList, key = find_result[0]
        
        if parentList is None:
            logger.error("Error: parentList is None")
            # 抛出异常
            raise ValueError("Error: parentList is None")
        
        parentList.append(command_model.data)
        
        logger.info("Merged Data:\n%s", json.dumps(parentList))
        
        return insurance_list_data
    
    def handle_insurance_update_logic(command_model: CommandModel, insurance_list_data: List[Dict[str, Any]]):
        """
        处理保险更新逻辑的函数。

        参数:
        - command_model: CommandModel实例，包含要更新的数据及其元数据。
        - insurance_list_data: 保险数据列表，用于更新和参考。

        返回:
        - 更新后的保险数据列表。

        此函数首先检查command_model中的数据是否为空，如果为空则记录错误并抛出异常。
        然后调用MCPService.find_data_by_type_new函数根据类型和其他条件查找相关数据。
        如果找到的数据存在，则使用Merger类合并现有数据和更新数据。
        合并后的数据会替换原有数据，并记录更新后的数据。
        如果找不到相关数据，则记录错误并抛出异常。
        """
        logger.info("into handle_insurance_update_logic")
        if command_model.data is None:
            logger.error("Error: command_model.data is None")
            # 抛出异常
            raise ValueError("Error: command_model.data is None")
        find_result = MCPService.find_data_by_type_new(command_model.type, insurance_list_data,
                                                                       command_model.ownerType, command_model.id, 'update')
        
        to_update_data, parent, key = find_result[0]
        
        if to_update_data is not None:
            # 执行更新操作
            merger = Merger(
                [(list, ["append"]), (dict, ["merge"])],
                ["override"],
                ["override"]
            )
            merged_data = merger.merge(to_update_data, command_model.data)
            logger.info("Merged Data:\n%s", json.dumps(merged_data))
            parent[key] = merged_data
            logger.info("handle_insurance_update_logic return:\n%s", insurance_list_data)
            return insurance_list_data
        else:
            logger.error("Error: to_update_data is None")
            # 抛出异常
            raise ValueError("Error: to_update_data is None")
    
    def handle_insurance_delete_logic(command_model: CommandModel, insurance_list_data: List[Dict[str, Any]]):
        """
        处理保险删除逻辑的函数。

        参数:
        - command_model: CommandModel实例，包含要删除的数据及其元数据。
        - insurance_list_data: 保险数据列表，用于更新和参考。

        返回:
        - 更新后的保险数据列表。

        此函数目前还没有实现具体的删除逻辑，仅记录了进入函数的日志。
        """
        logger.info("into handle_insurance_delete_logic")
        return insurance_list_data
    
    
    
    def handle_solutions_add_logic(command_model: CommandModel, solutions_list_data: List[Dict[str, Any]]):
        """
        处理解决方案添加逻辑的函数。

        本函数通过接收的命令模型和解决方案列表数据，更新或添加相应的解决方案数据。

        参数:
        - command_model: CommandModel类型，包含要添加的数据及其元信息。
        - solutions_list_data: List[Dict[str, Any]]类型，原有的解决方案列表数据。

        返回:
        - 更新后的解决方案列表数据。
        """
        # 记录进入函数的日志
        logger.info("into handle_solutions_add_logic")
        
        # 检查command_model.data是否为None，如果为None，则记录错误日志并抛出异常
        if command_model.data is None:
            logger.error("Error: command_model.data is None")
            # 抛出异常
            raise ValueError("Error: command_model.data is None")
        
        # 根据类型调用MCPService中的方法，查找并获取需要更新的数据、父列表和关键值
        find_result = MCPService.find_data_by_type_new(command_model.type, solutions_list_data,
                                                                           command_model.ownerType,
                                                                           command_model.id, 'add')
        to_update_data, parentList, key = find_result[0]
        
        # 如果parentList为None，则记录错误日志并抛出异常
        if parentList is None:
            logger.error("Error: parentList is None")
            # 抛出异常
            raise ValueError("Error: parentList is None")
        
        # 使用always_merger.merge方法合并父列表数据和命令模型中的数据
        parentList = always_merger.merge(parentList, command_model.data)
        
        # 记录合并后的数据日志
        logger.info("Merged Data:\n%s", json.dumps(parentList))
        
        # 返回更新后的解决方案列表数据
        return solutions_list_data
    
    # def handle_solutions_update_logic(command_model: CommandModel, solutions_list_data: List[Dict[str, Any]]):
    #     logger.info("into handle_solutions_update_logic")
    #     if command_model.data is None:
    #         logger.error("Error: command_model.data is None")
    #         # 抛出异常
    #         raise ValueError("Error: command_model.data is None")
    #
    #     to_update_data = MCPService.find_data_by_type(command_model.type, solutions_list_data, command_model.ownerType,
    #                                                   command_model.id, None, 'update')
    #     if to_update_data is not None:
    #         # 执行更新操作
    #         merger = Merger(
    #             [(list, ["append"]), (dict, ["merge"])],
    #             ["override"],
    #             ["override"]
    #         )
    #         merged_data = merger.merge(to_update_data, command_model.data)
    #         logger.info("Merged Data:\n%s", json.dumps(merged_data))
    #
    #         return solutions_list_data
    #     else:
    #         logger.error("Error: to_update_data is None")
    #         # 抛出异常
    #         raise ValueError("Error: to_update_data is None")
    #
    # def handle_solutions_delete_logic(command_model: CommandModel, solutions_list_data: List[Dict[str, Any]]):
    #     logger.info("into handle_solutions_delete_logic")
    #     return solutions_list_data
    
def merge_list_only(target, source,key_name):
    
    if key_name in source:
        if isinstance(source[key_name], list):
            for idx,item in enumerate(source[key_name]):
                if target[key_name][idx] :
                    merger = Merger(
                        [(list, ["append"]), (dict, ["merge"])],
                        ["override"],
                        ["override"]
                    )
                    # 合并 assetsList 字段
                    target[key_name][idx]  = merger.merge(target[key_name][idx] , source[key_name][idx])
        else:
            merger = Merger(
                [(list, ["append"]), (dict, ["merge"])],
                ["override"],
                ["override"]
            )
            # 合并 assetsList 字段
            target[key_name] = merger.merge(target.get(key_name, []), source.get(key_name, []))
        
        
    return target
        
        
        
    
    



