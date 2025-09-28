#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试精确数据修正功能
"""

import sys
sys.path.append('src')

from ai_analyzer import AIAnalyzer

def test_precise_correction():
    """测试精确数据修正功能"""
    print("=" * 80)
    print("测试精确数据修正功能")
    print("=" * 80)
    
    # 使用原始问题数据
    test_data = """数据分析表格

地市	全球通客户收入-万元	拍照球通客户收入-万元	球通客户收入较上月变化-万元	拍照球通客户收入较上月变化-万元
锦州	2348	2133	-22	-45
抚顺	1578	1452	-23	-31
辽阳	1684	1496	23	-11
阜新	1567	1421	11	-18
铁岭	1535	1411	-33	-43
营口	3671	3390	-35	-56
葫芦岛	1704	1562	-2	-19
大连	13841	12964	-100	-135
沈阳	16761	16094	-111	-137
盘锦	1860	1720	-70	-78
朝阳	2297	2132	5	-24
丹东	3414	3245	-2	-13
全省	57491	54002	-410	-691
本溪	1545	1458	-15	-31
鞍山	3680	3518	-35	-47

数据说明：共15行数据，5个指标"""

    task_info = {
        'anaylsis_sql_id': 1,
        'anaylsis_name': '全球通"量质构效"分析',
        'op_month': '202508'
    }
    
    # 模拟原始分析结果（包含错误）
    print("模拟原始AI分析结果（包含数据错误）:")
    print("-" * 50)
    original_problematic_analysis = """全球通客户收入集中度较高：沈阳和大连以29.2%和24.1%的占比合计贡献全省53.3%的收入，形成明显头部效应。鞍山营口丹东三地收入均超3400万元，但合计占比不足19%，其余11地市收入均低于3000万元，呈现长尾分布特征。收入环比降幅显著：全省14个地市全球通客户收入均出现下滑，沈阳大连降幅最大（-111万元/-100万元），降幅超过50万元的地市达5个。拍照球通客户收入全量负增长，无任何地市实现正向变化，显示业务整体承压。"""
    print(original_problematic_analysis)
    
    # 创建AI分析器
    analyzer = AIAnalyzer()
    print(f"\n数据修正功能状态: {'启用' if analyzer.enable_verification else '禁用'}")
    
    # 直接测试修正器
    if analyzer.corrector:
        print("\n开始精确数据修正...")
        print("-" * 50)
        
        corrected_result, corrections = analyzer.corrector.correct_data_errors(
            original_problematic_analysis, test_data
        )
        
        print("\n修正后的分析结果:")
        print("-" * 50)
        print(corrected_result)
        
        print("\n修正详情:")
        print("-" * 50)
        if corrections:
            for i, correction in enumerate(corrections, 1):
                print(f"{i}. {correction}")
        else:
            print("未发现需要修正的数据错误")
        
        # 对比显示
        print("\n" + "=" * 80)
        print("修正对比")
        print("=" * 80)
        print("原文: 降幅超过50万元的地市达5个")
        print("修正: 降幅超过50万元的地市达3个")
        print("说明: 实际只有沈阳(-111)、大连(-100)、盘锦(-70)三个地市降幅超过50万元")
        
    else:
        print("❌ 数据修正功能未启用")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_precise_correction()
