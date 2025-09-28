#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试错误修正功能
"""

import sys
sys.path.append('src')

from precise_corrector import PreciseCorrector

def test_error_correction():
    """测试具体错误的修正"""
    
    # 包含错误的分析文本
    problematic_analysis = """全球通客户收入集中度高：沈阳和大连收入合计占比53.3%（29.2%+24.1%），远超其他地市，形成明显双极格局。鞍山和营口并列第三，收入仅为沈阳的22%（3680/16761），收入梯队差异显著。  
收入环比降幅普遍：14个地市全球通客户收入环比下降，沈阳降幅最大（-111万元），大连（-100万元）和盘锦（-70万元）紧随其后，降幅前3名合计减少281万元，占全省总降幅的68.5%（281/410）。  
拍照收入全面下滑：所有地市拍照球通客户收入环比均为负增长，沈阳（-137万元）和大连（-135万元）降幅最大，鞍山（-47万元）、营口（-56万元）、盘锦（-78万元）降幅显著，降幅前3名合计减少270万元，占全省总降幅的39.1%（270/691）。  
结构性差异突出：沈阳全球通客户收入与拍照收入差额达667万元（16761-16094），全省唯一差额超500万元的地市，反映其非拍照收入占比显著高于其他地市。"""

    # 原始数据
    test_data = """数据分析表格

地市	全球通客户收入-万元	拍照球通客户收入-万元	球通客户收入较上月变化-万元	拍照球通客户收入较上月变化-万元
全省	57491	54002	-410	-691
沈阳	16761	16094	-111	-137
大连	13841	12964	-100	-135
盘锦	1860	1720	-70	-78
营口	3671	3390	-35	-56
鞍山	3680	3518	-35	-47
铁岭	1535	1411	-33	-43
抚顺	1578	1452	-23	-31
锦州	2348	2133	-22	-45
本溪	1545	1458	-15	-31
葫芦岛	1704	1562	-2	-19
丹东	3414	3245	-2	-13
朝阳	2297	2132	5	-24
阜新	1567	1421	11	-18
辽阳	1684	1496	23	-11

数据说明：共15行数据，5个指标"""

    print("=" * 80)
    print("测试错误修正功能")
    print("=" * 80)
    
    corrector = PreciseCorrector()
    
    print("原始分析（包含错误）:")
    print("-" * 50)
    print(problematic_analysis)
    
    print("\n开始错误检测和修正...")
    print("-" * 50)
    
    corrected_analysis, corrections = corrector.correct_data_errors(
        problematic_analysis, test_data
    )
    
    print("修正后的分析:")
    print("-" * 50)
    print(corrected_analysis)
    
    print("\n修正详情:")
    print("-" * 50)
    if corrections:
        for i, correction in enumerate(corrections, 1):
            print(f"{i}. {correction}")
    else:
        print("未发现需要修正的错误")
    
    print("\n" + "=" * 80)
    print("预期修正项目:")
    print("1. '14个地市全球通客户收入环比下降' -> '11个地市全球通客户收入环比下降'")
    print("2. 需要人工检查拍照收入降幅前3名的计算")
    print("3. 需要人工检查'全省唯一差额超500万元'的表述")
    print("=" * 80)

if __name__ == "__main__":
    test_error_correction()
