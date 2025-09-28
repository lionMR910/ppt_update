#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试ChatBI接口的Python程序
"""

import requests
import json
import random
import time
from typing import Dict, Any


def generate_conversation_uid() -> str:
    """生成18位随机数作为conversationUid"""
    return str(random.randint(100000000000000000, 999999999999999999))


def prepare_chart_result() -> list:
    """准备chartResult数据"""
    # 原始数据
    raw_data = """
地市	全球通客户收入-万元	拍照球通客户收入-万元	球通客户收入较上月变化-万元	拍照球通客户收入较上月变化-万元
锦州	2348.0	2133.0	-22	-45
抚顺	1578.0	1452.0	-23	-31
辽阳	1684.0	1496.0	23	-11
阜新	1567.0	1421.0	11	-18
铁岭	1535.0	1411.0	-33	-43
营口	3671.0	3390.0	-35	-56
葫芦岛	1704.0	1562.0	-2	-19
大连	13841.0	12964.0	-100	-135
沈阳	16761.0	16094.0	-111	-137
朝阳	2297.0	2132.0	5	-24
盘锦	1860.0	1720.0	-70	-78
丹东	3414.0	3245.0	-2	-13
全省	57491.0	54002.0	-410	-691
本溪	1545.0	1458.0	-15	-31
鞍山	3680.0	3518.0	-35	-47"""
    
    chart_result = []
    lines = raw_data.strip().split('\n')
    
    # 跳过空行和表头行
    for line in lines:
        line = line.strip()
        if not line or '地市' in line or '全球通客户收入-万元' in line:
            continue
            
        parts = line.split('\t')
        if len(parts) == 5:
            try:
                chart_result.append({
                    "city": parts[0],
                    "value1": float(parts[1]),
                    "value2": float(parts[2]),
                    "diff1": int(parts[3]),
                    "diff2": int(parts[4])
                })
            except (ValueError, IndexError) as e:
                print(f"跳过无法解析的行: {line} - 错误: {e}")
                continue
    
    return chart_result


def test_chatbi_api(api_key: str = None) -> Dict[str, Any]:
    """
    测试ChatBI接口
    
    Args:
        api_key: API密钥，如果没有请设置为None或空字符串
    
    Returns:
        接口响应结果
    """
    
    # 接口配置
    base_url = "http://10.68.76.66/chatbi/biapi/v1/open/bi/chat/conclusion"
    params = {
        "currentWorkspace": 2,
        "currentTeam": 1
    }
    
    # 准备请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    # 如果提供了API密钥，添加Authorization头
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        print("警告: 未提供API密钥，请求可能会失败")
    
    # 准备请求数据
    conversation_uid = generate_conversation_uid()
    chart_result = prepare_chart_result()
    
    request_data = {
        "userInput": "请对全球通客户收入情况进行解读",
        "conversationUid": conversation_uid,
        "topicId": 683,
        "chartResult": chart_result
    }
    
    print("=== 请求信息 ===")
    print(f"URL: {base_url}")
    print(f"参数: {params}")
    print(f"请求头: {headers}")
    print(f"conversationUid: {conversation_uid}")
    print(f"数据行数: {len(chart_result)}")
    print("\n=== 请求数据示例 ===")
    print(json.dumps(request_data, ensure_ascii=False, indent=2)[:500] + "...")
    
    try:
        print("\n=== 发送请求 ===")
        start_time = time.time()
        
        response = requests.post(
            url=base_url,
            params=params,
            headers=headers,
            json=request_data,
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"请求耗时: {response_time:.2f}秒")
        print(f"状态码: {response.status_code}")
        
        # 打印响应头
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("\n=== 响应成功 ===")
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "data": result
                }
            except json.JSONDecodeError:
                print(f"\n=== JSON解析失败 ===")
                print(f"原始响应: {response.text}")
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": "JSON解析失败",
                    "raw_response": response.text
                }
        else:
            print(f"\n=== 请求失败 ===")
            print(f"错误信息: {response.text}")
            return {
                "success": False,
                "status_code": response.status_code,
                "response_time": response_time,
                "error": response.text
            }
            
    except requests.exceptions.Timeout:
        print("\n=== 请求超时 ===")
        return {
            "success": False,
            "error": "请求超时"
        }
    except requests.exceptions.ConnectionError:
        print("\n=== 连接错误 ===")
        return {
            "success": False,
            "error": "无法连接到服务器"
        }
    except Exception as e:
        print(f"\n=== 其他错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """主函数"""
    print("ChatBI接口测试程序")
    print("=" * 50)
    
    # 这里可以设置您的API密钥
    # 如果没有API密钥，设置为None
    api_key = "akcada59e8ffa74fde85eef836e664ed27"  # 实际的API密钥
    
    # 如果需要从环境变量获取API密钥
    # import os
    # api_key = os.getenv('CHATBI_API_KEY')
    
    result = test_chatbi_api(api_key)
    
    print("\n" + "=" * 50)
    print("测试结果总结:")
    if result["success"]:
        print("✅ 接口调用成功")
        print(f"📊 响应时间: {result['response_time']:.2f}秒")
    else:
        print("❌ 接口调用失败")
        print(f"🚫 错误信息: {result['error']}")
    
    return result


if __name__ == "__main__":
    # 安装依赖提示
    try:
        import requests
    except ImportError:
        print("请先安装requests库: pip install requests")
        exit(1)
    
    main()
