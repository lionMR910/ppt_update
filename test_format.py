#!/usr/bin/env python3
"""
测试格式匹配逻辑
"""

import re

def test_format_matching():
    """测试格式匹配"""
    
    # 测试文本
    test_text = """沈阳市和大连市收入最高：沈阳市以 1.71亿元 的全球通客户收入位居全省第一，大连市以 1.43亿元 紧随其后，合计占全省总收入的 52.83%。
拍照全球通收入占比高：各市拍照全球通收入占比普遍超过 90%，其中沈阳市拍照全球通收入占比高达 98.51%，表明拍照全球通是主要收入来源。"""
    
    print("测试文本:")
    print(test_text)
    print("\n" + "="*60)
    
    # 测试正则表达式
    colon_pattern = r"(?:^|。|；|\n)([\u4e00-\u9fff]{2,15}?)："
    number_pattern = r"(\d+(?:\.\d+)?%?)"
    
    print("\n冒号前文字匹配:")
    colon_matches = list(re.finditer(colon_pattern, test_text))
    for i, match in enumerate(colon_matches):
        colon_text = match.group(1)
        print(f"{i+1}. 位置 {match.start(1)}-{match.end(1)+1}: '{colon_text}：'")
    
    print(f"\n数字匹配:")
    number_matches = list(re.finditer(number_pattern, test_text))
    for i, match in enumerate(number_matches):
        print(f"{i+1}. 位置 {match.start()}-{match.end()}: '{match.group()}'")
    
    # 模拟格式处理
    print(f"\n格式处理模拟:")
    matches = []
    
    # 收集冒号匹配
    for match in colon_matches:
        colon_text = match.group(1)
        colon_start = match.start(1)
        colon_end = match.end(1)
        matches.append((colon_start, colon_end + 1, 'bold_red', colon_text + '：'))
    
    # 收集数字匹配（检查重叠）
    for match in number_matches:
        overlap = False
        for existing_start, existing_end, _, _ in matches:
            if not (match.end() <= existing_start or match.start() >= existing_end):
                overlap = True
                break
        if not overlap:
            matches.append((match.start(), match.end(), 'red_only', match.group()))
    
    # 排序
    matches.sort(key=lambda x: x[0])
    
    # 构建结果
    parts = []
    last_end = 0
    
    for start, end, format_type, match_text in matches:
        if start > last_end:
            parts.append(('normal', test_text[last_end:start]))
        parts.append((format_type, match_text))
        last_end = end
    
    if last_end < len(test_text):
        parts.append(('normal', test_text[last_end:]))
    
    print("\n格式化结果:")
    for i, (part_type, part_text) in enumerate(parts):
        if part_text.strip():
            print(f"{i+1}. {part_type}: '{part_text}'")

if __name__ == "__main__":
    test_format_matching()