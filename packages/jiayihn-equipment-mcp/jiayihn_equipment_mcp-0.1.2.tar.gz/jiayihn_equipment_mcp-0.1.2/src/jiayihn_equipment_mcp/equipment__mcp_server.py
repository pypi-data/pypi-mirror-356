from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP server
mcp = FastMCP("equipment_mcp_server")

# Constants
API_PREV = "http://dev-openapi.jiayihn.com/api/open"

async def post_request(
        url: str,
        headers: dict[str, str] | None = None,
        request_body: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
    """jiayihn open api发送请求,并进行适当的错误处理。"""
    headers = {
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, timeout=30.0, json=request_body)
            response.raise_for_status()
            return response.json()
        except Exception:
            return '提交失败'

@mcp.tool()
async def get_options_by_column(
    column_name: str
) -> list[str]:
    """根据字段名称获取可选的选项,当用户不知道某些字段有哪些选项时,可以使用此工具获取，
    比如用户不知道设备大类具体有哪些选项,可以传equipmentCategory,获取设备大类的可选选项
    Args:

    column_name (str): 字段名称,
        例如:
            equipmentCategory (str): 设备大类
            equipmentSubcategory (str): 设备小类
            brandManufacturer (str): 品牌厂家

    Returns:
        list[str]: 选项列表

    """
    url = f"{API_PREV}/franchisee-equipment-maintenance/get-options-by-column"
    params = {
        "columnName": column_name
    }
    request_body = {
        "merchantId": 100004,
        "timeStamp": 1000000000,
        "sign": "asdfasfsafsa",
        "params": params
    }

    result = await post_request(url=url, request_body=request_body)
    print(f"选项列表:{result}")
    return result

@mcp.tool()
async def equipment_repair_submit(
    storeCode: str,
    reporterPhone: str,
    equipmentCategory: str,
    equipmentSubcategory: str,
    brandManufacturer: str,
    equipmentImagesUrl: list[str],
    faultSymptom: str,
    additionalDescription: str
) -> str:
    """提交设备维修单,每个参数都必须从用户的输入信息中获取,如果用户没有输入对应的信息,则需要询问用户相关信息

    Args:
    
    storeCode (str): 门店编号
    reporterPhone (str): 报修人手机号
    equipmentCategory (str): 设备大类
    equipmentSubcategory (str): 设备小类
    brandManufacturer (str): 品牌厂家
    equipmentImagesUrl (list[str]): 设备图片链接
    faultSymptom (str): 故障现象
    additionalDescription (str): 其它补充描述

    Returns:
        str: 提交结果

    """
    url = f"{API_PREV}/franchisee-equipment-maintenance/submit"
    params = {
        "storeCode": storeCode,
        "reporterPhone": reporterPhone,
        "equipmentCategory": equipmentCategory,
        "equipmentSubcategory": equipmentSubcategory,
        "brandManufacturer": brandManufacturer,
        "equipmentImagesUrl": equipmentImagesUrl,
        "faultSymptom": faultSymptom,
        "additionalDescription": additionalDescription
    }
    request_body = {
        "merchantId": 100004,
        "timeStamp": 1000000000,
        "sign": "asdfasfsafsa",
        "params": params
    }

    result = await post_request(url=url, request_body=request_body)
    print(f"设备维修提交结果:{result}")
    return result

def run():
    mcp.run(transport='stdio')
    print("equipment-repair server start success!")

if __name__ == "__main__":
    # 初始化并运行 server
   run()