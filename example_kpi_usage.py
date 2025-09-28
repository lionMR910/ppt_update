#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KPI 更新功能调用示例

演示如何使用 KPI 替换功能的各种调用方式
"""

import sys
import os
sys.path.append('src')

def example_1_command_line():
    """示例1: 命令行调用方式"""
    print("=== 示例1: 命令行调用 ===")
    print("命令格式:")
    print("python src/kpi_ppt_command.py -t PPT文件路径 -m 月份参数")
    print()
    print("具体示例:")
    print("python src/kpi_ppt_command.py -t file/ces.pptx -m 202507")
    print("python src/kpi_ppt_command.py -t file/ces.pptx -m 202507 -o output.pptx -v")
    print()

def example_2_text_replacement():
    """示例2: 纯文本替换"""
    print("=== 示例2: 纯文本KPI替换 ===")
    
    from kpi_replacer import KpiReplacer
    
    # 初始化替换器
    replacer = KpiReplacer()
    
    # 示例文本（包含KPI占位符）
    sample_text = """
    分析报告：
    本月全球通客户收入为 {{kpi_1_1}} 亿元，
    较上月减少 {{kpi_1_2}} 万元。
    拍照全球通客户收入为 {{kpi_1_3}} 亿元，
    较上月减少 {{kpi_1_4}} 万元。
    
    客户数据：
    全球通客户数为 {{kpi_2_1}} 万户，
    白金及以上客户为 {{kpi_2_2}} 万户。
    """
    
    print("原始文本:")
    print(sample_text)
    
    # 执行替换
    try:
        result = replacer.replace_kpi_in_text(sample_text, "202507")
        print("替换后文本:")
        print(result)
    except Exception as e:
        print(f"替换失败: {e}")
    
    print()

def example_3_ppt_processing():
    """示例3: PPT文件处理"""
    print("=== 示例3: PPT文件处理 ===")
    
    from enhanced_ppt_processor import EnhancedPPTProcessor
    
    # PPT文件路径（需要确保文件存在）
    template_path = "file/ces.pptx"
    
    if not os.path.exists(template_path):
        print(f"警告: PPT模板文件不存在: {template_path}")
        print("请确保有包含KPI占位符的PPT文件")
        return
    
    try:
        # 初始化处理器
        processor = EnhancedPPTProcessor(template_path)
        
        # 加载模板
        if processor.load_template():
            print(f"✅ PPT模板加载成功: {template_path}")
            
            # 执行完整替换
            results = processor.process_complete_replacement("202507")
            
            # 显示结果
            print("替换结果:")
            print(f"- 成功替换: {results.get('success', 0)} 个")
            print(f"- 替换失败: {results.get('failed', 0)} 个")
            print(f"- 未找到: {results.get('not_found', 0)} 个")
            
            # 保存结果
            output_path = "file/example_output.pptx"
            if processor.save_presentation(output_path):
                print(f"✅ PPT保存成功: {output_path}")
            else:
                print("❌ PPT保存失败")
        else:
            print("❌ PPT模板加载失败")
            
    except Exception as e:
        print(f"处理过程出错: {e}")
    
    print()

def example_4_database_query():
    """示例4: 直接数据库查询"""
    print("=== 示例4: 数据库查询 ===")
    
    from kpi_replacer import KpiReplacer
    
    try:
        replacer = KpiReplacer()
        
        # 获取所有KPI数据
        kpi_values = replacer.get_kpi_values("202507")
        
        print("从数据库获取的KPI数据:")
        for (sql_id, col_index), value in kpi_values.items():
            print(f"{{{{kpi_{sql_id}_{col_index}}}}} = {value}")
            
    except Exception as e:
        print(f"数据库查询失败: {e}")
    
    print()

def main():
    """主函数 - 运行所有示例"""
    print("🚀 KPI 更新功能调用示例")
    print("=" * 50)
    
    # 1. 命令行调用方式
    example_1_command_line()
    
    # 2. 纯文本替换
    example_2_text_replacement()
    
    # 3. PPT文件处理
    example_3_ppt_processing()
    
    # 4. 数据库查询
    example_4_database_query()
    
    print("=" * 50)
    print("📖 更多信息请查看: KPI_FEATURE_GUIDE.md")

if __name__ == "__main__":
    main()