import re

text = "沈阳市和大连市收入最高：沈阳市以 1.71亿元 的全球通客户收入位居全省第一"

colon_pattern = r"(?:^|。|；|\n)([\u4e00-\u9fff]{2,15}?)："
matches = list(re.finditer(colon_pattern, text))

print(f"找到 {len(matches)} 个冒号匹配:")
for match in matches:
    print(f"匹配内容: '{match.group()}'")
    print(f"冒号前文字: '{match.group(1)}'")