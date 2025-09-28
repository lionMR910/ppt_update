#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数值错误修正功能
"""

import sys
sys.path.append('src')

from precise_corrector import PreciseCorrector

def test_value_correction():
    """测试数值错误的修正"""
    
    print("=" * 80)
    print("测试数值错误修正功能")
    print("=" * 80)
    
    # 包含数值错误的分析文本
    problematic_text = """全球通客户收入集中度显著：沈阳和大连合计贡献全省53.3%的全球通客户收入，远高于其他地市，形成明显头部效应。鞍山、营口、丹东三地收入均超3400万元，但均低于全省均值3833万元，显示中游梯队与头部存在较大差距。收入变动呈现全面下行趋势：全球通客户收入11个地市环比下降，降幅前3位为沈阳-111万元、大连-100万元、盘锦-70万元，降幅均超70万元。鞍山、营口、盘锦三地全球通收入降幅均达-35万元，与拍照球通收入降幅形成显著联动。"""

    # 原始数据
    test_data = """数据分析表格

地市	全球通客户收入-万元	拍照球通客户收入-万元	球通客户收入较上月变化-万元	拍照球通客户收入较上月变化-万元
全省	57491	54002	-410	-691
沈阳	16761	16094	-111	-137
大连	13841	12964	-100	-135
鞍山	3680	3518	-35	-47
营口	3671	3390	-35	-56
丹东	3414	3245	-2	-13
锦州	2348	2133	-22	-45
朝阳	2297	2132	5	-24
盘锦	1860	1720	-70	-78
葫芦岛	1704	1562	-2	-19
辽阳	1684	1496	23	-11
抚顺	1578	1452	-23	-31
阜新	1567	1421	11	-18
本溪	1545	1458	-15	-31
铁岭	1535	1411	-33	-43

数据说明：共15行数据，5个指标"""

    print("原始分析（包含数值错误）:")
    print("-" * 50)
    print(problematic_text)
    
    corrector = PreciseCorrector()
    
    print("\n开始数值修正...")
    print("-" * 50)
    
    corrected_analysis, corrections = corrector.correct_data_errors(
        problematic_text, test_data
    )
    
    print("修正后的分析:")
    print("-" * 50)
    print(corrected_analysis)
    
    print(f"\n修正详情:")
    print("-" * 50)
    if corrections:
        for i, correction in enumerate(corrections, 1):
            print(f"{i}. {correction}")
    else:
        print("未发现需要修正的错误")
    
    print("\n" + "=" * 80)
    print("预期修正:")
    print("1. '全省均值3833万元' -> '全省均值4106万元'")
    print("2. '降幅均超70万元' -> '降幅均达70万元'")
    print("3. 检测盘锦降幅数据错误（-35万元实际应为-70万元）")
    print("=" * 80)

if __name__ == "__main__":
    test_value_correction()
