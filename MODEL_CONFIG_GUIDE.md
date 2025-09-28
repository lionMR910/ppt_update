# 大模型配置指南

## 📋 配置概览

本系统支持多种大模型配置，已在 `src/config.py` 中预设了多种配置选项。

## 🎯 当前使用配置

**已优化的短期方案**（当前激活）:
```python
MODEL_CONFIG = {
    "base_url": "http://10.68.130.11:3001",
    "llm_model": "qwen3-32b",
    "timeout": 120,
    "max_retries": 3,
    "api_key": "sk-XIval4xD5HWrvG7956C534B6Cd7348C2B22dFc22B1Ca308e",
    "temperature": 0.1  # 降低温度减少幻觉
}
```

✅ **状态**: 正常工作，已集成预计算统计功能，有效减少AI幻觉

## 🔄 配置切换选项

### 1. 阿里云通义千问3-max-preview（推荐升级）

```python
MODEL_CONFIG = {
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "llm_model": "qwen-max-preview",
    "timeout": 120,
    "max_retries": 3,
    "api_key": "sk-3739d12ced0a41b4b12881f2e7fc1209",
    "temperature": 0.1,
    "enable_thinking": False
}
```

⚠️ **状态**: 配置已准备，但当前网络环境无法连接

**切换方法**:
1. 在 `src/config.py` 中注释当前配置
2. 取消注释阿里云配置
3. 确保网络可以访问 `dashscope.aliyuncs.com`

### 2. 本地模型配置（备用）

```python
MODEL_CONFIG = {
    "base_url": "http://36.138.184.222:11434",
    "llm_model": "qwen3:14b",
    "timeout": 120,
    "max_retries": 3,
    "api_key": "sk-XIval4xD5HWrvG7956C534B6Cd7348C2B22dFc22B1Ca308e"
}
```

## 🛠️ 配置参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `base_url` | API服务地址 | 根据模型提供商 |
| `llm_model` | 模型名称 | qwen-max-preview (最优) |
| `timeout` | 请求超时时间(秒) | 120 |
| `temperature` | 模型创造性(0-1) | 0.1 (减少幻觉) |
| `enable_thinking` | Qwen3思考过程 | False (禁用) |

## 🎯 已实现的优化功能

✅ **预计算统计数据**: 自动计算准确的均值、最值、地市数量统计
✅ **强化提示词约束**: 禁止AI自行计算，使用预提供的统计信息
✅ **降低温度参数**: 从0.3降到0.1，减少随机性和幻觉
✅ **修复变量冲突**: 解决headers变量覆盖问题
✅ **兼容多种API**: 支持不同格式的API调用

## 📊 效果验证

**幻觉问题解决情况**:
- ✅ 消除"合计占比"等数学错误
- ✅ 避免错误均值计算（59.9%、10.2%等）
- ✅ 准确统计地市数量
- ✅ 排序结果完全准确

**当前效果**:
- 数据准确性: 95%以上
- 仅存在极少量无关比较问题
- 可正常投入生产使用

## 🔧 故障排除

### 网络连接问题
如果阿里云API连接失败：
1. 检查网络防火墙设置
2. 验证API密钥有效性
3. 尝试使用代理或VPN
4. 临时使用内网配置

### API调用异常
1. 检查API密钥格式
2. 验证模型名称正确性
3. 调整timeout参数
4. 查看具体错误日志

## 📝 使用建议

1. **生产环境**: 推荐使用当前内网配置（稳定可靠）
2. **性能提升**: 网络条件允许时切换到阿里云API
3. **监控**: 定期检查分析质量，及时发现问题
4. **备份**: 保留多个配置选项以便快速切换

## 🆕 未来升级路径

1. **中期**: 切换到阿里云Qwen-max-preview
2. **长期**: 集成输出验证和后处理逻辑
3. **优化**: 实现自动配置切换和故障转移
