# AI分析结论验证和修正模块使用指南

## 概述

本模块旨在解决AI分析过程中的"幻觉"问题，通过二次检查和修正机制确保分析结论的准确性和一致性。

## 功能特性

### 1. 自动问题检测
- **数据类型不匹配**：检测时间序列数据中错误的地市分析
- **数值准确性**：验证分析中的数值是否来源于原始数据
- **排序准确性**：确保"最高"、"最低"等表述与实际排序一致
- **逻辑一致性**：检查自相矛盾的表述

### 2. 智能修正
- 根据数据类型（时间序列 vs 地市数据）生成专门的修正提示词
- 使用大模型进行智能修正
- 保持分析的专业性和可读性

### 3. 配置灵活性
- 可通过配置文件启用/禁用验证功能
- 支持自定义验证超时时间和重试次数

## 使用方法

### 1. 配置设置

在 `src/config.py` 中配置验证功能：

```python
VERIFICATION_CONFIG = {
    "enable_verification": True,  # 是否启用分析结论验证和修正
    "verification_timeout": 60,   # 验证超时时间（秒）
    "max_correction_attempts": 1  # 最大修正尝试次数
}
```

### 2. 直接使用验证器

```python
from src.analysis_verifier import AnalysisVerifier

# 创建验证器实例
verifier = AnalysisVerifier()

# 验证和修正分析结论
corrected_analysis, errors = verifier.verify_and_correct_analysis(
    original_analysis="原始分析结论",
    user_input="用户问题",
    chart_obj="原始数据",
    task_info={"anaylsis_name": "任务名称", "op_month": "202508"}
)

# 查看发现的问题
for error in errors:
    print(f"问题: {error['description']} (严重程度: {error['severity']})")

print("修正后的分析:", corrected_analysis)
```

### 3. 集成使用（推荐）

验证功能已自动集成到 `AIAnalyzer` 中：

```python
from src.ai_analyzer import AIAnalyzer

# 创建分析器（自动包含验证功能）
analyzer = AIAnalyzer()

# 进行分析（自动验证和修正）
result = analyzer.analyze_data(task_info, data_content)
```

## 问题类型说明

### 1. 数据类型不匹配 (data_type_mismatch)
- **问题**：时间序列数据中出现地市分析
- **严重程度**：高
- **示例**：时间序列数据中提到"锦州市"、"沈阳市"等

### 2. 可疑数值 (suspicious_numbers)
- **问题**：分析中出现不在原始数据中的数值
- **严重程度**：中
- **示例**：原始数据中没有的百分比或数值

### 3. 逻辑矛盾 (logical_contradiction)
- **问题**：同一实体既被描述为最高又被描述为最低
- **严重程度**：高
- **示例**：某地市既是"最高"又是"最低"

### 4. 不当时间分析 (inappropriate_time_analysis)
- **问题**：地市数据中使用时间序列分析术语
- **严重程度**：中
- **示例**：地市数据中提到"环比变化"、"时间趋势"等

## 修正策略

### 时间序列数据修正
- 移除所有地市名称引用
- 专注于时间趋势分析
- 使用"时间点"而非"地市"的表述

### 地市数据修正
- 确保排序准确性
- 使用具体地市名称
- 避免占比相加错误

## 测试方法

运行测试脚本验证功能：

```bash
python test_verification_module.py
```

测试包括：
1. 时间序列数据验证测试
2. 地市数据验证测试
3. 集成功能测试

## 性能考虑

- 验证过程会增加约30-60秒的处理时间
- 可通过配置禁用验证功能以提高性能
- 建议在生产环境中启用验证以确保质量

## 日志输出示例

```
🤖 开始AI分析: 全球通量质构效分析
✓ AI分析完成
🔍 启动分析结论验证...
📊 检测到数据类型: time_series
⚠️ 发现 1 个问题，开始修正...
🔧 发现并修正了 1 个问题
   - 时间序列数据中不应包含地市分析，但提到了: 锦州, 丹东, 沈阳
✅ 分析结论修正完成
```

## 故障排除

### 1. 验证失败
- 检查网络连接
- 确认API密钥有效
- 查看错误日志

### 2. 修正效果不佳
- 调整修正提示词
- 增加问题检测规则
- 降低模型temperature参数

### 3. 性能问题
- 禁用验证功能（设置 `enable_verification: False`）
- 调整超时时间
- 减少重试次数

## 扩展开发

### 添加新的问题检测类型

在 `_perform_fact_check` 方法中添加新的检测逻辑：

```python
def _perform_fact_check(self, analysis, structured_data, headers, statistics, sort_results, data_type):
    errors = []
    
    # 现有检测逻辑...
    
    # 添加新的检测类型
    if self._check_new_problem_type(analysis):
        errors.append({
            "type": "new_problem_type",
            "description": "发现新类型问题",
            "severity": "medium"
        })
    
    return {"has_errors": len(errors) > 0, "errors": errors}
```

### 自定义修正提示词

修改 `_build_*_correction_prompt` 方法来自定义修正策略。

## 版本历史

- v1.0: 基础验证和修正功能
- 支持时间序列和地市数据类型检测
- 集成到现有分析流程
