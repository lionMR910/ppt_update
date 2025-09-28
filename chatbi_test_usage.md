# ChatBI接口测试程序使用说明

## 文件说明

1. **test_chatbi_api.py** - 完整版测试程序，包含详细的错误处理和日志输出
2. **simple_chatbi_test.py** - 简化版测试程序，代码简洁易懂
3. **requirements_test.txt** - 依赖包列表

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements_test.txt
```

### 2. 运行简化版测试
```bash
python simple_chatbi_test.py
```

### 3. 运行完整版测试
```bash
python test_chatbi_api.py
```

## 参数说明

程序会自动使用以下参数：

- **userInput**: "请对全球通客户收入情况进行解读"
- **conversationUid**: 自动生成的18位随机数
- **topicId**: 683 (固定值)
- **chartResult**: 包含辽宁省各地市全球通客户收入数据

## API密钥配置

如果接口需要API密钥，请在 `test_chatbi_api.py` 中的第125行修改：

```python
api_key = "your_actual_api_key_here"  # 替换为实际的API密钥
```

或者设置环境变量：

```bash
export CHATBI_API_KEY="your_api_key"
```

## 数据格式

chartResult数据包含15个地市的信息，每个地市包含：
- city: 城市名称
- value1: 第一个数值 (收入相关)
- value2: 第二个数值 (收入相关)  
- diff1: 第一个差值
- diff2: 第二个差值

## 预期响应

如果接口正常工作，应该会返回对全球通客户收入情况的AI解读分析。

## 故障排除

1. **连接错误**: 检查网络连接和服务器地址
2. **认证失败**: 检查API密钥是否正确
3. **超时**: 增加timeout参数值
4. **JSON解析错误**: 检查服务器响应格式
