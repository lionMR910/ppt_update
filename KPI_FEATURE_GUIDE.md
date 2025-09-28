# KPI 参数替换功能使用指南

## 功能概述

新增的 KPI 参数替换功能能够自动处理 PPT 中的 `{{kpi_X_Y}}` 格式占位符，从数据库中获取相应数据并进行替换。

### 核心特性

- ✅ 自动识别 PPT 中的 KPI 占位符（`{{kpi_1_1}}` 格式）
- ✅ 从数据库表 `anaylsis_deploy_ppt_def` 获取 SQL 语句
- ✅ 自动进行月份参数替换
- ✅ 执行 SQL 查询获取实际数据
- ✅ 按照列索引精确替换对应数值
- ✅ 支持 SQLite 和 MySQL 数据库
- ✅ 集成到现有的 PPT 处理流程

## 快速开始

### 1. 环境准备

```bash
# 安装额外依赖
pip install -r requirements_kpi.txt

# 初始化测试数据库
python src/init_test_database.py
```

### 2. 基本使用

```bash
# 处理包含 KPI 参数的 PPT
python src/kpi_ppt_command.py -t file/ces.pptx -m 202507

# 指定输出文件
python src/kpi_ppt_command.py -t file/ces.pptx -m 202507 -o report_202507.pptx

# 详细模式
python src/kpi_ppt_command.py -t file/ces.pptx -m 202507 -v
```

## KPI 参数格式说明

### 占位符格式

```
{{kpi_X_Y}}
```

- **X**: `anaylsis_sql_id`，对应数据库表中的记录行
- **Y**: 列索引，对应 SQL 查询结果的第几列数据（从1开始）

### 示例

```
{{kpi_1_1}} - 取 anaylsis_sql_id=1 记录的 SQL 查询结果第1列
{{kpi_1_2}} - 取 anaylsis_sql_id=1 记录的 SQL 查询结果第2列  
{{kpi_2_1}} - 取 anaylsis_sql_id=2 记录的 SQL 查询结果第1列
{{kpi_2_4}} - 取 anaylsis_sql_id=2 记录的 SQL 查询结果第4列
```

## 数据库配置

### 数据库表结构

系统需要访问 `anaylsis_deploy_ppt_def` 表，包含以下字段：

```sql
CREATE TABLE anaylsis_deploy_ppt_def (
    anaylsis_sql_id INTEGER PRIMARY KEY,    -- SQL ID
    anaylsis_id INTEGER,                     -- 分析ID
    anaylsis_name TEXT,                      -- 分析名称
    anaylsis_lev1_name TEXT,                 -- 一级分类
    anaylsis_lev2_name TEXT,                 -- 二级分类
    anaylsis_sql_test TEXT,                  -- 原始SQL模板
    top_sql_test TEXT,                       -- 实际执行的SQL
    op_month TEXT,                           -- 操作月份
    sql_flag INTEGER                         -- 启用标志
);
```

### 数据库连接配置

系统支持多种数据库配置：

```python
# SQLite 配置（默认）
DEFAULT_CONFIGS = {
    'sqlite_test': DatabaseConfig(
        db_type='sqlite',
        file_path='data/test.db'
    ),
    
    # MySQL 配置
    'mysql_prod': DatabaseConfig(
        db_type='mysql',
        host='localhost',
        port=3306,
        database='market_analysis',
        username='root',
        password='password'
    )
}
```

## 使用示例

### 示例1：完整的 KPI 替换流程

假设数据库中有以下数据：

| anaylsis_sql_id | top_sql_test | 
|-----------------|--------------|
| 1 | `SELECT 5.8, -101, 5.5, -112` |
| 2 | `SELECT 156.7, 23.4, 15.0, 8.9` |

PPT 模板内容：
```
分析报告：
本月全球通客户收入为 {{kpi_1_1}} 亿元，
较上月减少 {{kpi_1_2}} 万元。
拍照全球通客户收入为 {{kpi_1_3}} 亿元，
较上月减少 {{kpi_1_4}} 万元。

客户数据：
全球通客户数为 {{kpi_2_1}} 万户，
白金及以上客户为 {{kpi_2_2}} 万户。
```

替换后结果：
```
分析报告：
本月全球通客户收入为 5.8 亿元，
较上月减少 -101 万元。
拍照全球通客户收入为 5.5 亿元，
较上月减少 -112 万元。

客户数据：
全球通客户数为 156.7 万户，
白金及以上客户为 23.4 万户。
```

### 示例2：月份参数处理

对于包含月份变量的 SQL 模板：

```sql
-- 原始 SQL 模板
SELECT a.qqt_amt, a.pzqqt_amt
FROM anaylsis_qqt_lzgx_st_mm a, 
     anaylsis_qqt_lzgx_st_mm b
WHERE a.op_month = {op_month} 
  AND b.op_month = {last_op_month}
```

当指定月份参数为 `202507` 时，系统会自动替换为：

```sql
-- 替换后的 SQL
SELECT a.qqt_amt, a.pzqqt_amt  
FROM anaylsis_qqt_lzgx_st_mm a,
     anaylsis_qqt_lzgx_st_mm b
WHERE a.op_month = '202507'
  AND b.op_month = '202506'
```

## 编程接口

### 基本使用

```python
from enhanced_ppt_processor import EnhancedPPTProcessor

# 初始化处理器
processor = EnhancedPPTProcessor("template.pptx")

# 加载模板
processor.load_template()

# 执行完整替换（包含KPI和传统占位符）
results = processor.process_complete_replacement("202507")

# 保存结果
processor.save_presentation("output.pptx")
```

### 高级使用

```python
from kpi_replacer import KpiReplacer
from database_config import DatabaseManager, DatabaseConfig

# 自定义数据库配置
db_config = DatabaseConfig(
    db_type='mysql',
    host='your-host',
    database='your-db',
    username='user',
    password='pass'
)

db_manager = DatabaseManager(db_config)

# 初始化KPI替换器
kpi_replacer = KpiReplacer(db_manager)

# 处理文本中的KPI占位符
text = "收入为 {{kpi_1_1}} 亿元"
result = kpi_replacer.replace_kpi_in_text(text, "202507")
```

## 命令行工具

### 基本命令

```bash
# 显示帮助
python src/kpi_ppt_command.py -h

# 基本替换
python src/kpi_ppt_command.py -t template.pptx -m 202507

# 指定数据库配置
python src/kpi_ppt_command.py -t template.pptx -m 202507 --db-config mysql_prod

# 详细输出
python src/kpi_ppt_command.py -t template.pptx -m 202507 -v
```

### 参数说明

| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| `--template` | `-t` | PPT模板文件路径 | 是 |
| `--month` | `-m` | 月份参数（YYYYMM） | 是 |
| `--output` | `-o` | 输出文件路径 | 否 |
| `--db-config` |  | 数据库配置名称 | 否 |
| `--verbose` | `-v` | 显示详细信息 | 否 |

## 错误处理

### 常见问题

1. **数据库连接失败**
   - 检查数据库配置是否正确
   - 确认数据库服务是否运行
   - 验证用户权限

2. **未找到KPI数据**
   - 检查 `anaylsis_sql_id` 是否存在
   - 确认 `sql_flag = 1`
   - 验证 SQL 语句是否有效

3. **月份参数格式错误**
   - 确保格式为 YYYYMM（如 202507）
   - 月份范围：01-12
   - 年份范围：2020-2030

4. **SQL 执行失败**
   - 检查 SQL 语法是否正确
   - 确认表名和字段名是否存在
   - 验证月份替换是否正确

### 日志输出

系统会生成详细的日志文件：
- 文件名格式：`kpi_ppt_log_YYYYMMDD.log`
- 包含处理过程、错误信息、替换详情

## 测试验证

### 1. 初始化测试环境

```bash
# 创建测试数据库和示例数据
python src/init_test_database.py
```

### 2. 验证功能

```bash
# 测试基本功能
python src/kpi_ppt_command.py -t file/ces.pptx -m 202507 -v

# 检查输出文件
ls file/ces_kpi_updated_*.pptx
```

### 3. 查看日志

```bash
# 查看处理日志
cat kpi_ppt_log_*.log
```

## 性能优化

### 数据库优化

1. **索引优化**
   ```sql
   CREATE INDEX idx_sql_id_flag ON anaylsis_deploy_ppt_def(anaylsis_sql_id, sql_flag);
   ```

2. **连接池**
   - 对于频繁操作，建议使用连接池
   - 减少连接建立/关闭的开销

### 处理优化

1. **批量处理**
   - 一次性获取所有需要的KPI数据
   - 避免重复数据库查询

2. **缓存机制**
   - 缓存查询结果
   - 避免重复执行相同的SQL

## 集成到现有流程

KPI 替换功能已经集成到现有的 PPT 处理流程中：

1. **兼容性**：完全兼容现有的占位符替换功能
2. **扩展性**：可以轻松添加新的 KPI 类型
3. **独立性**：可以单独使用 KPI 功能，不影响其他功能

## 更新历史

- **v1.0** (2024-12): 
  - 初始版本
  - 支持基本的 KPI 参数替换
  - 集成数据库查询功能
  - 提供命令行工具

---

如有问题或建议，请查看日志文件或联系开发团队。