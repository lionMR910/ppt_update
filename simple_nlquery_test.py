#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版ChatBI自然语言查询接口测试
"""

import requests
import json
import random


def test_nlquery():
    """简化版自然语言查询接口测试"""
    
    # 生成18位随机conversationUid
    conversation_uid = str(random.randint(100000000000000000, 999999999999999999))
    
    # 请求配置
    url = "http://10.68.76.66/chatbi/biapi/v1/open/bi/chat/nlQuery"
    params = {"currentWorkspace": 2, "currentTeam": 1}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer ak0b3049946fc647f5800ed1ffc64c0531"
    }
    
    # 请求数据
    data = {
        "userInput": "统计各地市全球通拍照离网客户数",
        "conversationUid": conversation_uid,
        "topicId": 665
    }
    
    print("=== ChatBI自然语言查询测试 ===")
    print(f"发送请求到: {url}")
    print(f"conversationUid: {conversation_uid}")
    print(f"查询内容: {data['userInput']}")
    
    try:
        response = requests.post(url, params=params, headers=headers, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ 查询成功!")
                print("响应数据:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print("❌ 查询失败!")
                print(f"错误码: {result.get('errorNo', '未知')}")
                print(f"错误信息: {result.get('errorMsg', '未知')}")
                print("完整响应:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("❌ HTTP错误:")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")


if __name__ == "__main__":
    test_nlquery()
