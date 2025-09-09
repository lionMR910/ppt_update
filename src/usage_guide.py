#!/usr/bin/env python3
"""
使用指南脚本
"""

import os

def show_usage_guide():
    """显示使用指南"""
    print("=" * 60)
    print("PPT模板文字替换程序 - 使用指南")
    print("=" * 60)
    
    print("\n📋 基本使用步骤:")
    print("1. 确保 file/ces.pptx 模板文件存在")
    print("2. 运行替换命令")
    print("3. 检查生成的输出文件")
    
    print("\n💻 命令示例:")
    print("# 基本用法（自动生成输出文件名）")
    print("python ppt_replacer.py -t file/ces.pptx")
    print()
    print("# 指定输出文件名")
    print("python ppt_replacer.py -t file/ces.pptx -o my_report.pptx")
    print()
    print("# 详细模式（显示处理过程）")
    print("python ppt_replacer.py -t file/ces.pptx -o my_report.pptx -v")
    
    print("\n📂 文件检查:")
    
    # 检查模板文件
    template_file = "file/ces.pptx"
    if os.path.exists(template_file):
        size = os.path.getsize(template_file) / 1024
        print(f"✓ 模板文件存在: {template_file} ({size:.1f} KB)")
    else:
        print(f"❌ 模板文件不存在: {template_file}")
        print("   请确保将PPT模板文件放在 file/ 目录下")
    
    # 检查输出文件
    output_files = []
    for file in os.listdir("."):
        if file.endswith(".pptx") and file != "ces.pptx":
            output_files.append(file)
    
    if output_files:
        print(f"\n📄 找到 {len(output_files)} 个输出文件:")
        for file in sorted(output_files):
            size = os.path.getsize(file) / 1024
            print(f"  ✓ {file} ({size:.1f} KB)")
    else:
        print(f"\n📄 未找到输出文件")
        print("   运行程序后会在当前目录生成输出文件")
    
    print("\n🔍 验证替换结果:")
    print("1. 用PowerPoint打开输出文件")
    print("2. 查找包含以下内容的幻灯片:")
    print("   - '沈阳市和大连市收入最高'")
    print("   - '沈阳市客户总量最大'")
    print("3. 确认不再有 {{analysis_text1}} 或 {{analysis_text2}} 占位符")
    
    print("\n🎨 格式要求:")
    print("- 基础字体: 微软雅黑 14号")
    print("- 冒号前文字: 红色加粗")
    print("- 数字: 仅红色（不加粗）")
    
    print("\n❓ 常见问题:")
    print("1. 如果提示'模板文件不存在':")
    print("   - 检查文件路径是否正确")
    print("   - 确保文件名是 ces.pptx")
    print()
    print("2. 如果替换后看不到变化:")
    print("   - 确认打开的是输出文件，不是原始模板")
    print("   - 关闭PPT后重新打开")
    print("   - 检查原始模板是否包含正确的占位符")
    
    print("\n🚀 快速测试:")
    print("运行以下命令进行快速测试:")
    print("python ppt_replacer.py -t file/ces.pptx -o test_result.pptx -v")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    show_usage_guide()