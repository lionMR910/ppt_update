#!/usr/bin/env python3
"""
检查替换结果的脚本
"""

import os
import zipfile
import xml.etree.ElementTree as ET

def extract_text_from_pptx(pptx_path):
    """从PPTX文件中提取所有文本内容"""
    try:
        texts = []
        
        with zipfile.ZipFile(pptx_path, 'r') as zip_file:
            # 获取所有幻灯片文件
            slide_files = [name for name in zip_file.namelist() 
                          if name.startswith('ppt/slides/slide') and name.endswith('.xml')]
            
            for slide_file in sorted(slide_files):
                try:
                    content = zip_file.read(slide_file)
                    root = ET.fromstring(content)
                    
                    # 提取所有文本节点
                    for text_elem in root.iter():
                        if text_elem.tag.endswith('}t') and text_elem.text:
                            texts.append(text_elem.text.strip())
                
                except Exception as e:
                    print(f"处理 {slide_file} 时出错: {e}")
        
        return texts
    
    except Exception as e:
        print(f"提取文本时出错: {e}")
        return []

def check_replacement():
    """检查替换结果"""
    print("=" * 60)
    print("检查PPT替换结果")
    print("=" * 60)
    
    # 检查原始文件
    original_file = "file/ces.pptx"
    if os.path.exists(original_file):
        print(f"✓ 原始文件存在: {original_file}")
        original_texts = extract_text_from_pptx(original_file)
        print(f"✓ 原始文件包含 {len(original_texts)} 个文本元素")
        
        # 查找占位符
        placeholders_found = []
        for text in original_texts:
            if "{{" in text and "}}" in text:
                placeholders_found.append(text)
        
        print(f"✓ 原始文件中找到 {len(placeholders_found)} 个包含占位符的文本:")
        for i, placeholder_text in enumerate(placeholders_found, 1):
            print(f"  {i}. {placeholder_text[:100]}...")
    else:
        print(f"❌ 原始文件不存在: {original_file}")
        return False
    
    # 检查输出文件
    output_file = "demo_output.pptx"
    if os.path.exists(output_file):
        print(f"\n✓ 输出文件存在: {output_file}")
        output_texts = extract_text_from_pptx(output_file)
        print(f"✓ 输出文件包含 {len(output_texts)} 个文本元素")
        
        # 查找是否还有占位符
        remaining_placeholders = []
        replaced_content = []
        
        for text in output_texts:
            if "{{" in text and "}}" in text:
                remaining_placeholders.append(text)
            elif "沈阳市" in text or "大连市" in text or "营口市" in text:
                replaced_content.append(text)
        
        print(f"\n替换结果分析:")
        print(f"✓ 剩余占位符: {len(remaining_placeholders)} 个")
        print(f"✓ 包含替换内容的文本: {len(replaced_content)} 个")
        
        if remaining_placeholders:
            print("\n❌ 仍有未替换的占位符:")
            for i, placeholder in enumerate(remaining_placeholders, 1):
                print(f"  {i}. {placeholder}")
        
        if replaced_content:
            print("\n✓ 替换成功的内容示例:")
            for i, content in enumerate(replaced_content[:3], 1):
                print(f"  {i}. {content[:100]}...")
        
        # 总结
        if len(remaining_placeholders) == 0 and len(replaced_content) > 0:
            print(f"\n🎉 替换成功！所有占位符已被替换为新内容")
            return True
        elif len(remaining_placeholders) > 0:
            print(f"\n⚠️  部分替换：{len(remaining_placeholders)} 个占位符未被替换")
            return False
        else:
            print(f"\n❓ 未检测到明显的替换内容，请手动检查文件")
            return False
    else:
        print(f"❌ 输出文件不存在: {output_file}")
        return False

if __name__ == "__main__":
    check_replacement()