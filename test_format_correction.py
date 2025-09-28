#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试格式修正功能
"""

import sys
sys.path.append('src')

from precise_corrector import PreciseCorrector

def test_format_correction():
    """测试格式错误的修正"""
    
    print("=" * 80)
    print("测试格式修正功能")
    print("=" * 80)
    
    # 包含格式错误的分析文本
    problematic_text = """全球通客户收入集中度高：沈阳大连双城主导全省格局沈阳以16761万元全球通客户收入位居全省第一占比292大连13841万元占比241两市合计占比超53全省收入分布呈现明显头部效应
收入环比下降趋势显著：11地市全球通收入负增长全省收入环比下降410万元其中大连沈阳降幅最大分别减少100万元111万元拍照球通收入全面下滑全省下降691万元沈阳大连降幅达137万元135万元需重点排查市场波动因素"""

    # 模拟数据
    test_data = """数据分析表格

地市	全球通客户收入-万元	拍照球通客户收入-万元	球通客户收入较上月变化-万元	拍照球通客户收入较上月变化-万元
沈阳	16761	16094	-111	-137
大连	13841	12964	-100	-135
鞍山	3680	3518	-35	-47

数据说明：共3行数据，5个指标"""

    print("原始分析（包含格式错误）:")
    print("-" * 50)
    print(problematic_text)
    
    corrector = PreciseCorrector()
    
    print("\n开始格式修正...")
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
    print("1. '占比292' -> '占比29.2%'")
    print("2. '占比241' -> '占比24.1%'")
    print("3. 添加必要的标点符号")
    print("=" * 80)

if __name__ == "__main__":
    test_format_correction()
