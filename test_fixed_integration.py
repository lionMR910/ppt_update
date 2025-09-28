#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的集成效果
"""

import sys
import os
sys.path.append('src')

from ai_analyzer import AIAnalyzer
from config import VERIFICATION_CONFIG

def test_fixed_integration():
    """测试修复后的集成效果"""
    print("=" * 80)
    print("测试修复后的AI分析器集成")
    print("=" * 80)
    
    # 检查配置
    print(f"验证功能配置: {VERIFICATION_CONFIG}")
    
    # 创建AI分析器
    analyzer = AIAnalyzer()
    print(f"验证功能状态: {'启用' if analyzer.enable_verification else '禁用'}")
    
    if not analyzer.enable_verification:
        print("⚠️ 验证功能被禁用，请检查配置文件")
        return
    
    # 模拟有问题的地市数据分析
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
    
    print("\n开始AI分析（应该看到验证日志）...")
    print("-" * 50)
    
    # 这应该会触发验证模块
    result = analyzer.analyze_data(task_info, test_data)
    
    print("-" * 50)
    if result:
        print("✅ 分析完成，结果:")
        print(result)
    else:
        print("❌ 分析失败")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_fixed_integration()
