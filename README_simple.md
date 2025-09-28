# 数据分析自动化程序

一个简单的Python程序，自动从数据库读取配置，执行SQL查询，调用大模型分析数据，并回写分析结论。

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置数据库和AI服务
编辑 `config.py` 文件：
```python
# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "your_username",
    "password": "your_password",
    "database": "your_database",
    "charset": "utf8mb4"
}

# 大模型配置
MODEL_CONFIG = {
    "base_url": "http://36.138.184.222:11434",
    "llm_model": "qwen3:14b",
    "timeout": 120,
    "max_retries": 3
}
```

### 3. 运行程序
```bash
python main.py
```

## 程序功能

### 核心流程
1. 连接MySQL数据库
2. 读取 `anaylsis_deploy_ppt_def` 表中 `sql_flag=1` 的记录
3. 执行每条记录的 `anaylsis_sql_test` SQL语句
4. 将查询结果格式化为制表符分隔的表格
5. 调用专业分析函数 `analysis_data_text` 进行AI分析
6. 将AI分析结果写入 `anaylsis_text` 字段

### 专业分析特性
- 使用专业的数据分析提示词模板
- 自动进行数据排序和极值分析
- 输出规范化的分析结论格式
- 专门针对移动通信业务数据优化

### 安全特性
- 只允许执行SELECT查询
- 自动添加行数限制防止大数据量查询
- SQL执行超时控制
- AI调用重试机制

## 文件说明

```
项目目录/
├── main.py                      # 主程序入口
├── config.py                   # 配置文件
├── database.py                 # 数据库操作模块
├── ai_analyzer.py              # AI分析模块
├── analysis_data_text_order.py # 专业分析函数
├── requirements.txt            # Python依赖包
├── README_simple.md            # 使用说明
└── prd_simple.md               # 需求文档
```

## 配置说明

### 数据库表结构
程序使用现有的表结构：
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

### 使用方法
1. 在表中插入分析配置，设置 `sql_flag=1` 启用
2. 在 `anaylsis_sql_test` 字段填写SQL查询语句
3. 运行程序，自动分析并更新 `anaylsis_text` 字段

## 示例

### 插入分析任务
```sql
INSERT INTO anaylsis_deploy_ppt_def 
(anaylsis_name, anaylsis_lev1_name, anaylsis_lev2_name, 
 anaylsis_sql_test, op_month, sql_flag) 
VALUES 
('销售数据分析', '市场分析', '销售分析', 
 'SELECT product_name, sales_amount, sales_date FROM sales WHERE MONTH(sales_date) = 12', 
 202412, 1);
```

### 运行结果
程序会自动：
1. 执行SQL查询获取销售数据
2. 调用AI分析销售趋势和特点
3. 将分析结论更新到 `anaylsis_text` 字段

## 定时执行

### 使用crontab（Linux/Mac）
```bash
# 每天凌晨2点执行
0 2 * * * cd /path/to/your/project && python main.py
```

### 使用任务计划程序（Windows）
创建定时任务执行 `python main.py`

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库配置信息
   - 确认数据库服务正在运行
   - 验证用户名密码正确

2. **AI服务连接失败**
   - 检查AI服务地址是否正确
   - 确认网络连接正常
   - 验证AI服务正在运行

3. **SQL执行失败**
   - 检查SQL语句语法
   - 确认表和字段存在
   - 检查数据库权限

### 日志信息
程序运行时会输出详细的执行信息，包括：
- 数据库连接状态
- AI服务连接状态
- 每个任务的执行结果
- 成功和失败统计

## 技术特点

- **简单易用**：单个Python脚本，配置简单
- **安全可靠**：SQL注入防护，执行限制
- **错误处理**：完善的异常处理和重试机制
- **实时反馈**：详细的执行状态显示

---
*版本：v1.0*  
*类型：简化实现*