#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版ChatBI接口测试
"""

import requests
import json
import random


def test_api():
    """简化版接口测试"""
    
    # 生成18位随机conversationUid
    conversation_uid = str(random.randint(100000000000000000, 999999999999999999))
    
    # 准备chartResult数据
    chart_data = [
      {
        "离网客户数": {
          "v": 155951
        },
        "city_id": {
          "v": "410"
        }
      },
      {
        "离网客户数": {
          "v": 172103
        },
        "city_id": {
          "v": "419"
        }
      },
      {
        "离网客户数": {
          "v": 220280
        },
        "city_id": {
          "v": "421"
        }
      },
      {
        "离网客户数": {
          "v": 339848
        },
        "city_id": {
          "v": "417"
        }
      },
      {
        "离网客户数": {
          "v": 222991
        },
        "city_id": {
          "v": "416"
        }
      },
      {
        "离网客户数": {
          "v": 154845
        },
        "city_id": {
          "v": "413"
        }
      },
      {
        "离网客户数": {
          "v": 137564
        },
        "city_id": {
          "v": "414"
        }
      },
      {
        "离网客户数": {
          "v": 160821
        },
        "city_id": {
          "v": "429"
        }
      },
      {
        "离网客户数": {
          "v": 1101010
        },
        "city_id": {
          "v": "411"
        }
      },
      {
        "离网客户数": {
          "v": 274343
        },
        "city_id": {
          "v": "415"
        }
      },
      {
        "离网客户数": {
          "v": 171502
        },
        "city_id": {
          "v": "427"
        }
      },
      {
        "离网客户数": {
          "v": 1362054
        },
        "city_id": {
          "v": "240"
        }
      },
      {
        "离网客户数": {
          "v": 147719
        },
        "city_id": {
          "v": "418"
        }
      },
      {
        "离网客户数": {
          "v": 314049
        },
        "city_id": {
          "v": "412"
        }
      }
    ]
    
    # 请求配置
    url = "http://10.68.76.66/chatbi/biapi/v1/open/bi/chat/conclusion"
    params = {"currentWorkspace": 2, "currentTeam": 1}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer ak0b3049946fc647f5800ed1ffc64c0531"
    }
    
    # 请求数据
    data = {
        "userInput": "请对各地市全球通拍照离网客户数分布图表进行解读",
        "conversationUid": conversation_uid,
        "topicId": 665,
        "chartResult": chart_data
    }
    
    print(f"发送请求到: {url}")
    print(f"conversationUid: {conversation_uid}")
    
    try:
        response = requests.post(url, params=params, headers=headers, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("响应数据:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("错误响应:")
            print(response.text)
            
    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    test_api()
