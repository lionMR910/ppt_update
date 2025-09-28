#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试KPI数据获取问题
"""

import sys
sys.path.append('src')

from kpi_replacer import KpiReplacer

def debug_kpi_data():
    """调试KPI数据获取"""
    print("🔍 调试KPI数据获取问题")
    
    replacer = KpiReplacer()
    
    # 获取分析数据
    analysis_data_list = replacer.get_analysis_data()
    
    print(f"\n📋 找到 {len(analysis_data_list)} 条分析数据:")
    for data in analysis_data_list:
        print(f"  SQL ID {data.sql_id}: {data.analysis_name}")
        print(f"    SQL: {data.top_sql_test[:100]}...")
    
    # 逐个测试SQL执行
    print(f"\n🔄 逐个测试SQL执行:")
    for data in analysis_data_list:
        print(f"\n--- SQL ID {data.sql_id} ---")
        
        # 执行原始SQL
        try:
            results = replacer.execute_sql_query(data.top_sql_test)
            print(f"查询结果: {len(results)} 行")
            
            if results:
                row = results[0]
                print(f"第一行数据类型: {type(row)}")
                
                if isinstance(row, dict):
                    print(f"字典键值: {list(row.keys())}")
                    print(f"字典数据: {list(row.values())}")
                    
                    # 测试列数据提取
                    for i, (key, value) in enumerate(row.items(), 1):
                        print(f"  列 {i}: {key} = {value}")
                        
                else:
                    print(f"元组数据: {row}")
                    for i, value in enumerate(row, 1):
                        print(f"  列 {i}: {value}")
        
        except Exception as e:
            print(f"❌ SQL执行失败: {e}")
    
    # 测试完整的KPI数据获取
    print(f"\n📊 完整KPI数据获取测试:")
    try:
        kpi_values = replacer.get_kpi_values("202507")
        
        print(f"获取到 {len(kpi_values)} 个KPI值:")
        
        # 按SQL ID分组显示
        for sql_id in [1, 2, 3]:
            print(f"\nSQL ID {sql_id}:")
            found_any = False
            for col in range(1, 6):  # 检查前5列
                key = (sql_id, col)
                if key in kpi_values:
                    print(f"  {{{{kpi_{sql_id}_{col}}}}} = {kpi_values[key]}")
                    found_any = True
            
            if not found_any:
                print(f"  (没有找到数据)")
                
    except Exception as e:
        print(f"❌ KPI数据获取失败: {e}")

if __name__ == "__main__":
    debug_kpi_data()