"""
处理阿里云的请求的方法
"""

import os
import logging
import requests
import time


from . import file_utils
from urllib.parse import urlparse
logging.basicConfig(level=logging.DEBUG)
import sys
from dotenv import load_dotenv
load_dotenv()


from typing import List

from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

print(os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'))
print(os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))
print(os.getenv('ALIBABA_CLOUD_CATEGORYID'))
print(os.getenv('ALIBABA_CLOUD_WORKSPACEID'))
print(os.getenv('ALIBABA_CLOUD_CATEGORYTYPE'))

class AliyunApiService:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> bailian20231229Client:
        """
        使用凭据初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码建议使用更安全的无AK方式，凭据配置方式请参见：https://help.aliyun.com/document_detail/378659.html。
        credential = CredentialClient()
        config = open_api_models.Config(
            credential=credential
        )
        # 试下改成固定ak配置
        # config = open_api_models.Config(
        #     type="access_key",
        #     access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        #     access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
        # )

        # Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = f'bailian.cn-beijing.aliyuncs.com'
        return bailian20231229Client(config)

    @staticmethod
    def upload_lease(
            fileName: str,
            md5: str,
            size_in_bytes: str,
    ) -> str:
        """
                   申请文档上传租约接口
               """
        category_id = os.getenv('ALIBABA_CLOUD_CATEGORYID')
        workspace_id = os.getenv('ALIBABA_CLOUD_WORKSPACEID')
        category_type = os.getenv('ALIBABA_CLOUD_CATEGORYTYPE')

        #在一条打印语句中打印所有入参
        logging.info(f'upload_lease categoryId: %s,workspaceId: %s,categoryType: %s,fileName: %s,md5: %s,size_in_bytes: %s', category_id,workspace_id,category_type,fileName,md5,size_in_bytes)


        client = AliyunApiService.create_client()
        apply_file_upload_lease_request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
            file_name=fileName,
            md_5=md5,
            size_in_bytes=size_in_bytes,
            category_type=category_type
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = client.apply_file_upload_lease_with_options(category_id, workspace_id, apply_file_upload_lease_request, headers, runtime)
            logging.info(f'uploadLease applyFileUploadLeaseResponse: %s', UtilClient.to_jsonstring(resp))
            return UtilClient.to_jsonstring(resp)
        except Exception as error:
            logging.error(f"upload_lease error:%s",  error)
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            #抛出异常
            raise error


    @staticmethod
    async def upload_lease_async(
            fileName: str,
            md5: str,
            size_in_bytes: str,
    ) -> str:
        """
                   申请文档上传租约接口-异步接口
               """
        category_id = os.getenv('ALIBABA_CLOUD_CATEGORYID')
        workspace_id = os.getenv('ALIBABA_CLOUD_WORKSPACEID')
        category_type = os.getenv('ALIBABA_CLOUD_CATEGORYTYPE')

        # 在一条打印语句中打印所有入参
        logging.info(
            f'upload_lease_async categoryId: %s,workspaceId: %s,categoryType: %s,fileName: %s,md5: %s,size_in_bytes: %s',
            category_id, workspace_id, category_type, fileName, md5, size_in_bytes)

        client = AliyunApiService.create_client()
        apply_file_upload_lease_request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
            file_name=fileName,
            md_5=md5,
            size_in_bytes=size_in_bytes,
            category_type=category_type
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = await client.apply_file_upload_lease_with_options_async(category_id, workspace_id,
                                                               apply_file_upload_lease_request, headers, runtime)
            logging.info(f'uploadLease applyFileUploadLeaseResponse: %s', UtilClient.to_jsonstring(resp))
            return UtilClient.to_jsonstring(resp)
        except Exception as error:
            logging.error(f"upload_lease_async error:%s",  error)
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            # 抛出异常
            raise error


    @staticmethod
    def upload_file(pre_signed_url:str,
                    file_path:str,
                    bailian_extra:str,
                    bailian_content_type:str)->str:
        """
        上传文件
        """
        try:
            # 设置请求头
            headers = {
                "X-bailian-extra": bailian_extra,
                "Content-Type": bailian_content_type
            }

            #在一条打印语句中打印所有入参
            logging.info(f'upload_file preSignedUrl: %s,filePath: %s,bailianExtra: %s,bailianContentType: %s', pre_signed_url,file_path,bailian_extra,bailian_content_type)

            # 读取文档并上传
            with open(file_path, 'rb') as file:
                # 下方设置请求方法用于文档上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
                response = requests.put(pre_signed_url, data=file, headers=headers)

            # 检查响应状态码
            if response.status_code == 200:
                logging.info("uploadFile uploadFileResponse: %s", response)
                print("File uploaded successfully.")
                return "true"

            else:
                logging.error(f"uploadFile uploadFileResponse: %s", response)
                logging.error("Failed to upload the file. ResponseCode: %s", response.status_code)
                print(f"Failed to upload the file. ResponseCode: {response.status_code}")
                return "false"

        except Exception as error:
            print(f"An error occurred: {str(error)}")
            logging.error(f"An error occurred: {str(error)}")
            # 抛出异常
            raise error

    @staticmethod
    def upload_file_link(pre_signed_url:str,
                    source_url_string:str,
                    bailian_extra:str,
                    bailian_content_type:str):
        """
        上传文件链接
        """
        try:
            # 设置请求头
            headers = {
                "X-bailian-extra": bailian_extra,
                "Content-Type": bailian_content_type
            }

            # 在一条打印语句中打印所有入参
            logging.info(f'upload_file_link preSignedUrl: %s,filePath: %s,bailianExtra: %s,bailianContentType: %s',
                         pre_signed_url, file_path, bailian_extra, bailian_content_type)

            # 设置访问OSS的请求方法为GET
            source_response = requests.get(source_url_string)
            if source_response.status_code != 200:
                raise RuntimeError("Failed to get source file.")

            # 下方设置请求方法用于文档上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
            response = requests.put(pre_signed_url, data=source_response.content, headers=headers)

            # 检查响应状态码
            if response.status_code == 200:
                logging.info("uploadFile uploadFileResponse: %s", response)
                print("File uploaded successfully.")
                return "true"
            else:
                logging.error(f"uploadFile uploadFileResponse: %s", response)
                logging.error("Failed to upload the file. ResponseCode: %s", response.status_code)
                print(f"Failed to upload the file. ResponseCode: {response.status_code}")
                return "false"


        except Exception as error:
            print(f"An error occurred: {str(error)}")
            logging.error(f"An error occurred: {str(error)}")
            # 抛出异常
            raise error

    @staticmethod
    def add_file_to_bailian(
        lease_id: str,
    ) -> str:
        """
        添加文件到百炼
        """
        category_id = os.getenv('ALIBABA_CLOUD_CATEGORYID')
        workspace_id = os.getenv('ALIBABA_CLOUD_WORKSPACEID')
        category_type = os.getenv('ALIBABA_CLOUD_CATEGORYTYPE')

        # 在一条打印语句中打印所有入参
        logging.info(f'add_file_to_bailian leaseId: %s,categoryId: %s,workspaceId: %s,categoryType: %s', lease_id,category_id,workspace_id,category_type)

        client = AliyunApiService.create_client()
        add_file_request = bailian_20231229_models.AddFileRequest(
            lease_id=lease_id,
            parser='DASHSCOPE_DOCMIND',
            category_id=category_id,
            category_type=category_type
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = client.add_file_with_options(workspace_id, add_file_request, headers, runtime)
            logging.info('add_file_to_bailian resp: %s',UtilClient.to_jsonstring(resp))
            return UtilClient.to_jsonstring(resp)
        except Exception as error:
            logging.error(f"add_file_to_bailian error: %s", error)
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            # 抛出异常
            raise error

    @staticmethod
    async def add_file_to_bailian_async(
            lease_id: str,
    ) -> str:
        """
        添加文件到百炼-异步
        """
        category_id = os.getenv('ALIBABA_CLOUD_CATEGORYID')
        workspace_id = os.getenv('ALIBABA_CLOUD_WORKSPACEID')
        category_type = os.getenv('ALIBABA_CLOUD_CATEGORYTYPE')

        # 在一条打印语句中打印所有入参
        logging.info(f'add_file_to_bailian_async leaseId: %s,categoryId: %s,workspaceId: %s,categoryType: %s', lease_id,category_id,workspace_id,category_type)


        client = AliyunApiService.create_client()
        add_file_request = bailian_20231229_models.AddFileRequest(
            lease_id=lease_id,
            parser='DASHSCOPE_DOCMIND',
            category_id=category_id,
            category_type=category_type
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = client.add_file_with_options_async(workspace_id, add_file_request, headers, runtime)
            logging.info('add_file_to_bailian resp: %s', UtilClient.to_jsonstring(resp))
            return UtilClient.to_jsonstring(resp)
        except Exception as error:
            logging.error(f"add_file_to_bailian_async error: %s", error)
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            # 抛出异常
            raise error

    @staticmethod
    def file_status(
            file_id:str,
    ) -> str:
        """
        查询文件状态
        """
        workspace_id = os.getenv('ALIBABA_CLOUD_WORKSPACEID')
        # 在一条打印语句中打印所有入参
        logging.info(f'file_status fileId: %s,workspaceId: %s', file_id,workspace_id)

        client = AliyunApiService.create_client()
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = client.describe_file_with_options(workspace_id,
                                              file_id, headers,
                                              runtime)
            logging.info(f'file_status resp: %s', UtilClient.to_jsonstring(resp))
            return UtilClient.to_jsonstring(resp)
        except Exception as error:
            logging.error(f"file_status error: %s", error)
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            # 抛出异常
            raise error

    @staticmethod
    async def file_status_async(
            file_id: str,
    ) -> str:
        """
        查询文件状态
        """
        workspace_id = os.getenv('ALIBABA_CLOUD_WORKSPACEID')
        # 在一条打印语句中打印所有入参
        logging.info(f'file_status_async fileId: %s,workspaceId: %s', file_id,workspace_id)

        client = AliyunApiService.create_client()
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = await client.describe_file_with_options_async(workspace_id,
                                                     file_id, headers,
                                                     runtime)
            logging.info(f'file_status resp: %s', UtilClient.to_jsonstring(resp))
            return UtilClient.to_jsonstring(resp)
        except Exception as error:
            logging.error(f"file_status_async error: %s", error)
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            # 抛出异常
            raise error

    @staticmethod
    def do_upload_file_to_bailian(
            file_path: str,
            file_name: str,
            file_md5: str,
            file_size: str
    ) -> str|None:
        """
        执行将文件上传阿里云的操作
        1.判断参数
        2.阿里云上传文件租约申请
        3.执行文件上传
        4.将文件上传到百炼，得到fileId
        5.遍历查询文件解析状态，直到获取到文件就绪的状态，返回fileId
        """

        try:
            # 1.判断参数
            if not file_path:
                return None
            if not file_name:
                file_name = file_utils.get_file_name(file_path)
            if not file_md5:
                file_md5 = file_utils.calculate_md5(file_path)
            if not file_size:
                file_size = file_utils.get_file_size(file_path)
            leaseJson = AliyunApiService.upload_lease(file_name, file_md5, file_size)

            logging.info(f'leaseJson: %s', leaseJson)
            leaseJson = UtilClient.parse_json(leaseJson)


            pre_signed_url = leaseJson['body']['Data']['Param']['Url']
            lease_id = leaseJson['body']['Data']['FileUploadLeaseId']
            method = leaseJson['body']['Data']['Param']['Method']
            bailian_extra = leaseJson['body']['Data']['Param']['Headers']['X-bailian-extra']
            bailian_content_type = leaseJson['body']['Data']['Param']['Headers']['Content-Type']

            logging.info(f'pre_signed_url: %s', pre_signed_url)
            logging.info(f'leaseId: %s', lease_id)
            logging.info(f'Method: %s', method)
            logging.info(f'X-bailian-extra: %s', bailian_extra)
            logging.info(f'Content-Type: %s', bailian_content_type)

            upload_file_resp = AliyunApiService.upload_file(pre_signed_url, file_path, bailian_extra,
                                                            bailian_content_type)
            logging.info(f'upload_file_resp: %s', upload_file_resp)

            add_file_resp = AliyunApiService.add_file_to_bailian(lease_id)
            logging.info(f'add_file_to_bailian_resp: %s', add_file_resp)

            file_id = UtilClient.parse_json(add_file_resp)['body']['Data']['FileId']
            logging.info(f'file_id: %s', file_id)

            """
                循环遍历查询状态，直到返回结果中Status字段值为FILE_IS_READY
            """
            while True:
                # file_status_resp = asyncio.run(AliyunApiService.file_status_async(file_id))
                file_status_resp = AliyunApiService.file_status(file_id)
                logging.info(f'file_status_resp: %s', file_status_resp)
                status = UtilClient.parse_json(file_status_resp)['body']['Data']['Status']
                logging.info(f'status: %s', status)
                if status == 'FILE_IS_READY':
                    break
                #  休眠2秒
                time.sleep(2)

            return file_id

        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            logging.error("Error: %s", error)
            return None




if __name__ == '__main__':

    try:
        file_path='/Users/lazylee/Works/doc/01Mlink/3.project/ai/01财蕴天下/1.xlsx'
        file_name = file_utils.get_file_name(file_path)
        file_md5 = file_utils.calculate_md5(file_path)
        file_size = file_utils.get_file_size(file_path)
        leaseJson = AliyunApiService.upload_lease(file_name, file_md5, file_size)

        logging.info(f'leaseJson: %s', leaseJson)
        leaseJson = UtilClient.parse_json(leaseJson)

        pre_signed_url = leaseJson['body']['Data']['Param']['Url']
        lease_id = leaseJson['body']['Data']['FileUploadLeaseId']
        method = leaseJson['body']['Data']['Param']['Method']
        bailian_extra = leaseJson['body']['Data']['Param']['Headers']['X-bailian-extra']
        bailian_content_type = leaseJson['body']['Data']['Param']['Headers']['Content-Type']

        logging.info(f'pre_signed_url: %s', pre_signed_url)
        logging.info(f'leaseId: %s', lease_id)
        logging.info(f'Method: %s', method)
        logging.info(f'X-bailian-extra: %s', bailian_extra)
        logging.info(f'Content-Type: %s', bailian_content_type)

        upload_file_resp = AliyunApiService.upload_file(pre_signed_url, file_path, bailian_extra,
                                                        bailian_content_type)
        logging.info(f'upload_file_resp: %s', upload_file_resp)

        add_file_resp = AliyunApiService.add_file_to_bailian(lease_id)
        logging.info(f'add_file_to_bailian_resp: %s', add_file_resp)

        file_id = UtilClient.parse_json(add_file_resp)['body']['Data']['FileId']
        logging.info(f'file_id: %s', file_id)

        """
            循环遍历查询状态，直到返回结果中Status字段值为FILE_IS_READY
        """
        while True:
            # data = UtilClient.parse_json(resp)
            file_status_resp = AliyunApiService.file_status(file_id)
            logging.info(f'file_status_resp: %s', file_status_resp)
            status = UtilClient.parse_json(file_status_resp)['body']['Data']['Status']
            logging.info(f'status: %s', status)
            if status == 'FILE_IS_READY':
                break
            time.sleep(2)
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        print(error.message)
        # 诊断地址
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
