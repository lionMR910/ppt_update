#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试分析结论验证和修正模块
"""

import sys
import os
sys.path.append('src')

from analysis_verifier import AnalysisVerifier
from ai_analyzer import AIAnalyzer


def test_time_series_verification():
    """测试时间序列数据的验证功能"""
    print("=" * 60)
    print("测试时间序列数据验证功能")
    print("=" * 60)
    
    # 构造测试数据 - 时间序列数据
    test_data = """数据分析表格

月份	拍照全球通综合保有率(%)	拍照全球通规模保有率(%)	拍照全球通价值保有率(%)
202501	98.20	100	96.40
202502	99.20	99.80	98.60
202503	99.20	99.50	98.90
202504	98.50	99.10	97.80
202505	97.80	98.80	96.80
202506	96.95	98.50	95.39
202507	98.98	98.18	99.77
202508	96.8	97.9	95.8

数据说明：共8行数据，4个指标"""
    
    # 构造有问题的分析结论（包含地市信息的幻觉）
    problematic_analysis = """【拍照全球通保有率分析】  
综合保有率表现突出：锦州市以99.2%的综合保有率位居全省第一，高于均值1.0个百分点，是唯一突破99%的地市。  
价值保有率差距显著：丹东市价值保有率95.39%为全省最低，低于均值2.01个百分点，需重点提升高价值客户留存能力。  
规模保有率梯队分化：沈阳市规模保有率100.0%稳居首位，大连市以99.5%紧随其后，两者合计贡献全省28.6%的规模保有率。  
波动性特征明显：综合保有率在8个时间点均高于60%，但近4个月出现4次低于均值的情况，需警惕阶段性波动风险。"""
    
    user_input = "请分析全球通"量质构效"分析，分析月份：202508"
    task_info = {"anaylsis_name": "全球通量质构效分析", "op_month": "202508"}
    
    # 测试验证器
    verifier = AnalysisVerifier()
    corrected_analysis, errors = verifier.verify_and_correct_analysis(
        problematic_analysis, user_input, test_data, task_info
    )
    
    print("原始分析（有问题）：")
    print(problematic_analysis)
    print("\n发现的问题：")
    for i, error in enumerate(errors, 1):
        print(f"{i}. {error['description']} (严重程度: {error['severity']})")
    
    print("\n修正后的分析：")
    print(corrected_analysis)
    print("\n" + "=" * 60)


def test_city_data_verification():
    """测试地市数据的验证功能"""
    print("测试地市数据验证功能")
    print("=" * 60)
    
    # 构造测试数据 - 地市数据
    test_data = """数据分析表格

地市	全球通客户收入(万元)	拍照全球通收入占比(%)
沈阳	17300	97.2
大连	12500	96.8
鞍山	8900	95.5
锦州	7200	98.1
营口	6800	94.3

数据说明：共5行数据，3个指标"""
    
    # 构造有问题的分析结论（排序错误）
    problematic_analysis = """【全球通客户收入分析】
大连收入最高：大连以17300万元的全球通客户收入位居全省第一。
沈阳紧随其后：沈阳以12500万元排名第二。
营口表现突出：营口拍照全球通收入占比达到98.1%，全省最高。"""
    
    user_input = "请分析全球通客户收入情况"
    task_info = {"anaylsis_name": "全球通客户收入分析", "op_month": "202508"}
    
    # 测试验证器
    verifier = AnalysisVerifier()
    corrected_analysis, errors = verifier.verify_and_correct_analysis(
        problematic_analysis, user_input, test_data, task_info
    )
    
    print("原始分析（有问题）：")
    print(problematic_analysis)
    print("\n发现的问题：")
    for i, error in enumerate(errors, 1):
        print(f"{i}. {error['description']} (严重程度: {error['severity']})")
    
    print("\n修正后的分析：")
    print(corrected_analysis)
    print("\n" + "=" * 60)


def test_integrated_analyzer():
    """测试集成了验证功能的AI分析器"""
    print("测试集成验证功能的AI分析器")
    print("=" * 60)
    
    # 使用之前的时间序列数据
    test_data = """数据分析表格

月份	拍照全球通综合保有率(%)	拍照全球通规模保有率(%)	拍照全球通价值保有率(%)
202501	98.20	100	96.40
202502	99.20	99.80	98.60
202503	99.20	99.50	98.90
202504	98.50	99.10	97.80
202505	97.80	98.80	96.80
202506	96.95	98.50	95.39
202507	98.98	98.18	99.77
202508	96.8	97.9	95.8

数据说明：共8行数据，4个指标"""
    
    task_info = {"anaylsis_name": "全球通量质构效分析", "op_month": "202508"}
    
    # 创建AI分析器实例
    analyzer = AIAnalyzer()
    
    print(f"验证功能状态: {'启用' if analyzer.enable_verification else '禁用'}")
    
    # 注意：这里会调用实际的AI API，确保网络连接正常
    try:
        result = analyzer.analyze_data(task_info, test_data)
        if result:
            print("最终分析结果：")
            print(result)
        else:
            print("分析失败")
    except Exception as e:
        print(f"测试过程中出错: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("开始测试AI分析结论验证和修正模块")
    print("=" * 60)
    
    # 测试1: 时间序列数据验证
    test_time_series_verification()
    
    # 测试2: 地市数据验证
    test_city_data_verification()
    
    # 测试3: 集成测试（需要API连接）
    print("是否进行集成测试（需要AI API连接）？(y/n): ", end="")
    user_choice = input().strip().lower()
    if user_choice in ['y', 'yes']:
        test_integrated_analyzer()
    else:
        print("跳过集成测试")
    
    print("测试完成！")
