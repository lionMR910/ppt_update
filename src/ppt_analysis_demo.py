#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PPT分析报告生成演示脚本
"""

from ppt_processor import PPTProcessor
from config import MODEL_CONFIG

def main():
    """主函数 - 演示PPT分析报告生成流程"""
    
    # 配置参数
    template_path = "file/ces.pptx"
    output_path = "analysis_report_output.pptx"
    api_key = MODEL_CONFIG['api_key']
    
    # 示例数据
    user_input = "请分析以下数据，并给出主要结论"
    chart_obj = """
全球通组家、宽带、集团、长机龄客户占比

地市	全球通组家客户占比	全球通宽带客户占比	全球通集团客户占比	全球通长机龄客户占比
辽阳	19.83 	50.24 	78.56 	29.55 
本溪	24.53 	56.18 	77.84 	29.43 
葫芦岛	24.58 	47.95 	77.62 	25.53 
盘锦	29.70 	54.36 	75.97 	26.65 
鞍山	21.20 	52.19 	75.71 	28.32 
丹东	25.77 	53.03 	73.93 	29.92 
阜新	24.91 	53.24 	70.87 	28.20 
大连	23.44 	56.50 	68.72 	29.62 
锦州	23.74 	54.47 	65.27 	27.15 
铁岭	24.22 	48.77 	65.02 	27.20 
营口	27.59 	56.12 	64.94 	28.24 
全省	23.19 	54.08 	63.81 	29.01 
朝阳	30.03 	55.77 	60.41 	29.07 
抚顺	25.16 	56.36 	55.37 	29.67 
沈阳	19.60 	53.27 	49.21 	29.71 
"""
    
    try:
        print("开始PPT分析报告生成流程...")
        
        # 1. 初始化PPT处理器
        processor = PPTProcessor(template_path)
        print(f"✓ 初始化PPT处理器，模板: {template_path}")
        
        # 2. 加载PPT模板
        if not processor.load_template():
            print("✗ 加载PPT模板失败")
            return
        print("✓ PPT模板加载成功")
        
        # 3. 生成分析报告数据
        print("正在生成分析报告...")
        if not processor.generate_analysis_data(api_key, user_input, chart_obj):
            print("✗ 分析报告生成失败")
            return
        print("✓ 分析报告生成成功")
        
        # 4. 查找PPT中的占位符
        placeholders = processor.find_placeholders()
        print(f"✓ 找到 {len(placeholders)} 个占位符:")
        for slide_idx, placeholder in placeholders:
            print(f"  - 幻灯片 {slide_idx + 1}: {placeholder}")
        
        # 5. 执行文本替换
        print("正在执行文本替换...")
        replace_results = processor.replace_all_text()
        print(f"✓ 替换完成: 成功 {replace_results['success']} 项, "
              f"失败 {replace_results['failed']} 项, "
              f"未找到 {replace_results['not_found']} 项")
        
        # 6. 保存处理后的PPT
        if processor.save_presentation(output_path):
            print(f"✓ PPT已保存至: {output_path}")
        else:
            print("✗ PPT保存失败")
            return
        
        print("\n=== 处理完成 ===")
        print(f"输出文件: {output_path}")
        print(f"替换的数据项: {list(processor.replacement_data.keys())}")
        
    except Exception as e:
        print(f"✗ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()