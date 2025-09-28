#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的KPI替换测试
"""

import sys
sys.path.append('src')

from kpi_replacer import KpiReplacer

def test_kpi_replacement():
    """测试KPI替换功能"""
    print("🔍 测试KPI替换功能")
    
    # 初始化替换器
    replacer = KpiReplacer()
    
    # 测试文本
    test_text = """
分析结果：
1. 全球通客户收入：{{kpi_1_1}} 亿元
2. 收入变化：{{kpi_1_2}} 万元  
3. 拍照全球通收入：{{kpi_1_3}} 亿元
4. 客户数量：{{kpi_2_1}} 万户
5. 白金客户：{{kpi_2_2}} 万户
6. 客户占比：{{kpi_2_3}}%
"""
    
    print("原始文本:")
    print(test_text)
    
    # 执行替换
    print("\n🔄 正在执行KPI替换...")
    try:
        result = replacer.replace_kpi_in_text(test_text, "202507")
        print("\n✅ 替换完成！")
        print("替换后文本:")
        print(result)
        
        # 显示数据库中的所有KPI数据
        print("\n📊 数据库中的KPI数据:")
        kpi_values = replacer.get_kpi_values("202507")
        for (sql_id, col_index), value in kpi_values.items():
            print(f"  {{{{kpi_{sql_id}_{col_index}}}}} = {value}")
        
    except Exception as e:
        print(f"❌ 替换失败: {e}")

if __name__ == "__main__":
    test_kpi_replacement()