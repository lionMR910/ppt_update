#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试ChatBI自然语言查询接口的Python程序
"""

import requests
import json
import random
import time
from typing import Dict, Any


def generate_conversation_uid() -> str:
    """生成18位随机数作为conversationUid"""
    return str(random.randint(100000000000000000, 999999999999999999))


def test_nlquery_api(api_key: str = None) -> Dict[str, Any]:
    """
    测试ChatBI自然语言查询接口
    
    Args:
        api_key: API密钥
    
    Returns:
        接口响应结果
    """
    
    # 接口配置
    base_url = "http://10.68.76.66/chatbi/biapi/v1/open/bi/chat/nlQuery"
    params = {
        "currentWorkspace": 2,
        "currentTeam": 1
    }
    
    # 准备请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer akcada59e8ffa74fde85eef836e664ed27"
    }
    
    # 准备请求数据
    conversation_uid = generate_conversation_uid()
    
    request_data = {
        "userInput": "统计各地市全球通拍照离网客户数",
        "conversationUid": conversation_uid,
        "topicId": 683
    }
    
    print("=== ChatBI自然语言查询接口测试 ===")
    print(f"URL: {base_url}")
    print(f"参数: {params}")
    print(f"请求头: {headers}")
    print(f"conversationUid: {conversation_uid}")
    print(f"用户输入: {request_data['userInput']}")
    print(f"topicId: {request_data['topicId']}")
    
    print("\n=== 请求数据 ===")
    print(json.dumps(request_data, ensure_ascii=False, indent=2))
    
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
                print("\n=== 响应结果 ===")
                if result.get("success"):
                    print("✅ 查询成功!")
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                else:
                    print("❌ 查询失败!")
                    print(f"错误码: {result.get('errorNo', '未知')}")
                    print(f"错误信息: {result.get('errorMsg', '未知错误')}")
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                
                return {
                    "success": result.get("success", False),
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
            print(f"HTTP错误码: {response.status_code}")
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


def test_multiple_queries():
    """测试多个不同的自然语言查询"""
    
    print("\n" + "=" * 60)
    print("=== 测试多个查询语句 ===")
    
    test_queries = [
        "统计各地市全球通拍照离网客户数",
        "查看全球通客户收入分布情况",
        "分析各地市客户结构",
        "全球通客户数排名",
        "各地市收入对比"
    ]
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- 测试查询 {i}: {query} ---")
        
        conversation_uid = generate_conversation_uid()
        request_data = {
            "userInput": query,
            "conversationUid": conversation_uid,
            "topicId": 683
        }
        
        try:
            response = requests.post(
                url="http://10.68.76.66/chatbi/biapi/v1/open/bi/chat/nlQuery",
                params={"currentWorkspace": 2, "currentTeam": 1},
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer akcada59e8ffa74fde85eef836e664ed27"
                },
                json=request_data,
                timeout=20
            )
            
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                success = result.get("success", False)
                print(f"查询结果: {'成功' if success else '失败'}")
                if not success:
                    print(f"错误信息: {result.get('errorMsg', '未知')}")
                results.append({"query": query, "success": success, "result": result})
            else:
                print(f"HTTP错误: {response.status_code}")
                results.append({"query": query, "success": False, "error": response.text})
                
        except Exception as e:
            print(f"请求异常: {e}")
            results.append({"query": query, "success": False, "error": str(e)})
    
    # 汇总结果
    print(f"\n=== 测试结果汇总 ===")
    success_count = sum(1 for r in results if r["success"])
    print(f"成功查询: {success_count}/{len(results)}")
    
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['query']}")
    
    return results


def main():
    """主函数"""
    print("ChatBI自然语言查询接口测试程序")
    print("=" * 60)
    
    # 测试主要查询
    result = test_nlquery_api()
    
    print("\n" + "=" * 60)
    print("主查询测试结果:")
    if result["success"]:
        print("✅ 自然语言查询成功")
        print(f"📊 响应时间: {result['response_time']:.2f}秒")
    else:
        print("❌ 自然语言查询失败")
        print(f"🚫 错误信息: {result.get('error', '未知错误')}")
    
    # 测试多个查询
    test_multiple_queries()
    
    return result


if __name__ == "__main__":
    # 安装依赖提示
    try:
        import requests
    except ImportError:
        print("请先安装requests库: pip install requests")
        exit(1)
    
    main()
