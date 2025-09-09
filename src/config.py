# 配置文件

# 数据库配置
"""
DB_CONFIG = {
    "host": "36.138.184.222",
    "port": 9030,
    "user": "vanna",
    "password": "aibi!1230",
    "database": "analysis",
    "charset": "utf8mb4"
}
"""
DB_CONFIG = {
    "host": "10.68.111.11",
    "port": 9030,
    "user": "root",
    "password": "radar_360",
    "database": "chatbi",
    "charset": "utf8mb4"
}
# 大模型配置
"""
# 之前的本地模型配置（已注释）
MODEL_CONFIG = {
    "base_url": "http://36.138.184.222:11434",
    "llm_model": "qwen3:14b",
    "timeout": 120,
    "max_retries": 3,
    "api_key": "sk-XIval4xD5HWrvG7956C534B6Cd7348C2B22dFc22B1Ca308e"  # 专业分析API密钥
}
"""

"""
# 之前的内网模型配置（已注释）
MODEL_CONFIG = {
    "base_url": "http://10.68.130.11:3001",
    "llm_model": "qwen3-32b",
    "timeout": 120,
    "max_retries": 3,
    "api_key": "sk-XIval4xD5HWrvG7956C534B6Cd7348C2B22dFc22B1Ca308e",  # 专业分析API密钥
    "temperature": 0.1  # 降低温度减少幻觉
}
"""

# 阿里云通义千问3-max-preview配置（网络问题暂时注释）
"""
MODEL_CONFIG = {
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "llm_model": "qwen-max-preview",  # 使用qwen3-max-preview
    "timeout": 120,
    "max_retries": 3,
    "api_key": "sk-3739d12ced0a41b4b12881f2e7fc1209",  # 阿里云API密钥
    "temperature": 0.1,  # 降低温度减少幻觉
    "enable_thinking": False  # 禁用思考过程输出
}
"""

# 当前使用配置（已优化的短期方案）
MODEL_CONFIG = {
    "base_url": "http://10.68.130.11:3001",
    "llm_model": "qwen3-32b",
    "timeout": 120,
    "max_retries": 3,
    "api_key": "sk-XIval4xD5HWrvG7956C534B6Cd7348C2B22dFc22B1Ca308e",  # 专业分析API密钥
    "temperature": 0.3  # 调整温度平衡准确性和创造性
}

# PPT格式配置
FORMAT_CONFIG = {
    "font_name": "微软雅黑",
    "font_size": 11,
    "highlight_color": "FF0000",  # 红色 RGB
    "line_spacing": 1.5,  # 行间距（1.5倍行距）
    "bold_patterns": [
        r"([^：]*?)：",  # 冒号前的文字
        r"(\d+(?:\.\d+)?%?)",  # 数字和百分号
    ]
}

# 提示词模板
PROMPT_TEMPLATE = """请对以下数据进行分析，要求：
1. 直接给出分析结论，不要包含思考过程
2. 使用规范的格式，包括标题、要点
3. 语言简洁明了，重点突出
4. 只输出主要结论，不超过300字
5. 有些显而易见的内容没必要说，比如各市拍照全球通收入占比普遍超过90%，保有类指标结论重点对保有率低于97%的地市进行分析。
6. 报告的地市请直接输出地市名称，如沈阳，不要输出沈阳市。

【样例如下】
整体收入稳定：2025年6月，辽宁全球通客户收入整体保持稳定，其中拍照全球通收入占比高达 97.11%，表明拍照全球通业务是主要收入来源。
阜新表现突出：阜新全球通客户收入环比增长 10.20%，是唯一增长超过10%的地市，表现最为突出。
沈阳收入最高：沈阳以 1.73亿元 的全球通客户收入位居全省第一，占全省总收入的 43.45%。
多数地市收入下降：除朝阳和阜新外，其余12个地市全球通客户收入均出现不同程度的环比下降，需重点关注。
营口收入下降幅度较大：营口全球通客户收入环比下降 3.45%，是降幅最大的地市之一，需深入分析原因并采取措施。

【严格禁止事项】

- 禁止重复表达相同观点
- 禁止输出任何思考过程、<think>标签、分析推理步骤或中间计算过程
- 分析报告文字中禁止带有空格
- 禁止在同一份报告中出现逻辑矛盾的结论（如先说"差异明显"后说"接近"）
- 禁止使用模糊或相互冲突的形容词描述同一现象

【准确的排序结果】（请严格按照以下排序结果进行分析，确保准确性）：
{sort_results}

用户问题：{user_input}
原始数据：{chart_obj}

请严格按照上述排序结果进行分析，确保所有极值判断准确无误。重要提醒：绝对禁止输出任何思考过程、<think>标签或推理步骤，直接给出最终分析结论："""

# 系统消息模板
SYSTEM_MESSAGE = "你是中国移动的专业数据分析师。严格要求：1)严格基于提供数据分析，禁止编造数字 2)引用数值必须与原数据完全一致  3)直接给出最终结论，绝对禁止输出任何思考过程、<think>标签或分析推理步骤 5)只输出最终的分析结果"

# PPT文件配置
FILE_CONFIG = {
    "default_template": "file/ces.pptx",
    "output_suffix": "_updated"
}

# PPT占位符替换数据配置
REPLACEMENT_DATA = {
    "{{analysis_text1}}": "数据分析报告内容1：这里是第一部分的分析内容，包括主要发现和结论。",
    "{{analysis_text2}}": "数据分析报告内容2：这里是第二部分的分析内容，包括详细的数据解读和建议。"
}

# 其他配置
MAX_DATA_ROWS = 1000  # 最大查询行数限制
SQL_TIMEOUT = 60      # SQL执行超时时间（秒）