# 数据分析自动化程序 - 简化需求文档

## 1. 项目概述

开发一个简单的Python程序，从数据库读取SQL配置，执行查询，调用大模型分析数据，并将结果回写到数据库。

## 2. 核心功能

### 2.1 基本流程
```
读取配置表 → 执行SQL查询 → 调用大模型分析 → 更新分析结论
```

### 2.2 功能要求
1. 从 `anaylsis_deploy_ppt_def` 表读取配置
2. 执行 `anaylsis_sql_test` 字段中的SQL语句
3. 将查询结果发送给大模型分析
4. 更新 `anaylsis_text` 字段保存分析结论

## 3. 数据库表结构

使用现有表结构（保持原样）：
```sql
CREATE TABLE `anaylsis_deploy_ppt_def` (
  `anaylsis_sql_id` bigint(20) NOT NULL COMMENT "分析元数据唯一ID",
  `anaylsis_id` bigint(20) NULL COMMENT "分析ID",
  `anaylsis_name` varchar(128) NULL COMMENT "分析名称",
  `anaylsis_lev1_name` varchar(128) NULL COMMENT "分类名称1",
  `anaylsis_lev2_name` varchar(128) NULL COMMENT "分类名称2",
  `anaylsis_sql_test` varchar(4000) NULL COMMENT "分析sql语句",
  `op_month` int(11) NULL COMMENT "分析月份",
  `anaylsis_text` varchar(4000) NULL COMMENT "分析结论",
  `sql_flag` int(1) NULL COMMENT "生效标记"
) 
```

## 4. 技术配置

### 4.1 大模型配置
```python
MODEL_CONFIG = {
    "base_url": "http://36.138.184.222:11434",
    "llm_model": "qwen3:14b",
    "timeout": 120,
    "max_retries": 3
}
```

### 4.2 数据库配置
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "username",
    "password": "password",
    "database": "database_name",
    "charset": "utf8mb4"
}
```

## 5. 程序设计

### 5.1 主要模块
- **数据库连接器**：连接MySQL数据库
- **SQL执行器**：安全执行SQL查询
- **AI分析器**：调用大模型进行分析
- **结果更新器**：回写分析结论

### 5.2 核心逻辑
1. 连接数据库
2. 查询 `sql_flag=1` 的记录
3. 逐条执行SQL查询
4. 调用大模型分析数据
5. 更新分析结论到数据库

### 5.3 提示词模板
```python
PROMPT_TEMPLATE = """
请分析以下数据并给出专业的分析结论：

数据名称：{analysis_name}
数据分类：{lev1_name} - {lev2_name}
分析月份：{op_month}

数据内容：
{data}

请提供简洁明了的分析结论，包括：
1. 数据概况
2. 关键发现
3. 趋势分析
4. 建议

分析结论：
"""
```

## 6. 程序结构

```
data_analysis/
├── main.py              # 主程序入口
├── config.py           # 配置文件
├── database.py         # 数据库操作
├── ai_analyzer.py      # AI分析模块
├── utils.py            # 工具函数
└── requirements.txt    # 依赖包
```

## 7. 运行方式

### 7.1 命令行执行
```bash
python main.py
```

### 7.2 定时任务
```bash
# 每天凌晨2点执行
0 2 * * * cd /path/to/data_analysis && python main.py
```

## 8. 依赖包

```
pymysql==1.1.0
requests==2.31.0
pandas==2.1.3
```

## 9. 错误处理

- SQL执行失败：跳过当前记录，继续处理下一条
- AI调用失败：重试3次，失败后跳过
- 数据库连接失败：程序终止并输出错误信息

## 10. 安全考虑

- 使用参数化查询防止SQL注入
- 限制SQL执行时间，避免长时间阻塞
- 验证查询结果大小，避免内存溢出

## 11. 验收标准

- [ ] 程序能正确读取配置表数据
- [ ] 能安全执行SQL查询
- [ ] 成功调用大模型API
- [ ] 分析结论能正确回写到数据库
- [ ] 程序运行稳定，错误处理完善

---
*版本：v1.0*  
*类型：简化需求*