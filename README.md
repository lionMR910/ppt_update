# PPT模板文字替换程序

一个自动化工具，用于替换PPT模板中的占位符文本，支持静态文本替换和动态KPI数据替换。

## 功能特点

### 核心功能
- ✅ 自动识别并替换PPT中的占位符（`{{placeholder}}`格式）
- ✅ 完全保持模板原有格式和布局不变
- ✅ 支持静态文本替换和动态数据库KPI替换
- ✅ 智能格式处理：完全保持原有字体、大小、颜色等样式
- ✅ 命令行界面，操作简单
- ✅ 详细的日志记录和错误处理

### KPI动态替换功能 🆕
- ✅ 从数据库自动获取KPI数据并替换到PPT
- ✅ 支持月份参数自动处理（YYYYMM格式）
- ✅ 智能SQL执行和数据映射
- ✅ 支持SQLite和MySQL数据库
- ✅ 精确的运行块级别替换，100%保持原有格式
- ✅ 支持多种分析配置（全球通/中高端"量质构效"分析）
- ✅ 支持指定单个或多个分析任务处理
- ✅ 集成SQL执行和分析结论生成功能

## 安装要求

### 系统要求
- Windows 10/11
- Python 3.7+

### 依赖库
```bash
# 基础依赖
pip install -r requirements.txt

# KPI功能额外依赖
pip install -r requirements_kpi.txt
```

## 快速开始

### 静态文本替换

#### 1. 基本用法
```bash
python ppt_replacer.py -t file/ces.pptx
```

#### 2. 指定输出文件
```bash
python src/ppt_replacer.py -t file/ces.pptx -o file/report_202507.pptx
```

#### 3. 详细模式
```bash
python ppt_replacer.py -t file/ces.pptx -v
```

### KPI动态替换 🆕

#### 1. 激活虚拟环境
```bash
conda activate envs/pptup_env
```

#### 2. 初始化测试数据库（首次使用）
```bash
python src/init_test_database.py
```

#### 3. KPI替换基本用法
```bash
# 基本KPI替换（默认全球通分析）
python src/kpi_ppt_command.py -t file/model.pptx -m 202507

# 详细模式（推荐）
python src/kpi_ppt_command.py -t file/model.pptx -m 202507 -v

# 指定输出文件
python src/kpi_ppt_command.py -t file/model.pptx -m 202507 -o 报告_202507.pptx

# 使用中高端分析配置
python src/kpi_ppt_command.py -t file/model.pptx -m 202507 -a 2

# 指定单个分析任务
python src/kpi_ppt_command.py -t file/model.pptx -m 202507 --sql-id 5

# 指定多个分析任务
python src/kpi_ppt_command.py -t file/model.pptx -m 202507 --sql-id 1 2 3

# 指定任务+中高端分析配置
python src/kpi_ppt_command.py -t file/model.pptx -m 202507 --sql-id 5 -a 2
```

## 命令行参数

### 静态文本替换参数

| 参数 | 简写 | 说明 | 是否必需 |
|------|------|------|----------|
| `--template` | `-t` | PPT模板文件路径 | 是 |
| `--output` | `-o` | 输出文件路径 | 否 |
| `--config` | `-c` | 配置文件路径 | 否 |
| `--verbose` | `-v` | 显示详细信息 | 否 |
| `--help` | `-h` | 显示帮助信息 | 否 |
| `--version` |  | 显示版本信息 | 否 |

### KPI动态替换参数

| 参数 | 简写 | 说明 | 是否必需 | 示例 |
|------|------|------|----------|------|
| `--template` | `-t` | PPT模板文件路径 | 是 | `file/model.pptx` |
| `--month` | `-m` | 月份参数（YYYYMM） | 是 | `202507` |
| `--output` | `-o` | 输出文件路径 | 否 | `报告_202507.pptx` |
| `--analysis-id` | `-a` | 分析配置ID | 否 | `1`(全球通), `2`(中高端) |
| `--sql-id` | `--id` | 指定分析任务SQL ID | 否 | `5` 或 `1 2 3` |
| `--db-config` |  | 数据库配置 | 否 | `sqlite_test`, `mysql_prod` |
| `--verbose` | `-v` | 显示详细信息 | 否 |  |
| `--help` | `-h` | 显示帮助信息 | 否 |  |

## 配置说明

### 占位符格式

#### 静态文本占位符
程序会自动查找并替换以下格式的占位符：
- `{{analysis_text1}}` - 收入分析内容
- `{{analysis_text2}}` - 保有率分析内容

#### KPI动态占位符 🆕
KPI占位符格式为 `{{kpi_X_Y}}`，其中：
- **X**: `anaylsis_sql_id`，对应数据库表中的记录行
- **Y**: 列索引，对应 SQL 查询结果的第几列数据（从1开始）

**示例：**
- `{{kpi_1_1}}` - 取 sql_id=1 记录的 SQL 查询结果第1列
- `{{kpi_1_2}}` - 取 sql_id=1 记录的 SQL 查询结果第2列  
- `{{kpi_2_1}}` - 取 sql_id=2 记录的 SQL 查询结果第1列
- `{{kpi_2_4}}` - 取 sql_id=2 记录的 SQL 查询结果第4列

### 格式保持规范 🆕
- **格式完全保持**: 替换时100%保持原有字体、大小、颜色、粗体等所有样式
- **运行块级别替换**: 使用精确的文本运行块替换，确保格式不被修改
- **原有布局不变**: 保持段落结构、行间距、对齐方式等所有布局属性

### 数据库配置
KPI功能支持多种数据库配置：

#### SQLite配置（默认）
```python
sqlite_test: {
    db_type: 'sqlite',
    file_path: 'data/test.db'
}
```

#### MySQL配置
```python
mysql_prod: {
    db_type: 'mysql',
    host: 'localhost',
    port: 3306,
    database: 'market_analysis',
    username: 'root',
    password: 'password'
}
```

## 项目结构

```
ppt_update/
├── src/
│   ├── ppt_replacer.py          # PPT替换主程序
│   ├── ppt_processor.py         # PPT处理核心模块
│   ├── enhanced_ppt_processor.py # 增强PPT处理器（含KPI功能）🆕
│   ├── kpi_replacer.py          # KPI参数替换模块 🆕
│   ├── kpi_ppt_command.py       # KPI命令行工具 🆕
│   ├── database_config.py       # 数据库配置管理 🆕
│   ├── init_test_database.py    # 测试数据库初始化 🆕
│   ├── month_processor.py       # 月份参数处理器
│   ├── month_command.py         # 月份处理命令行工具
│   ├── trigger_month.py         # 月份触发命令
│   ├── ppt_data_generator.py    # PPT数据生成器
│   ├── analysis_data_text_order.py # AI分析模块
│   └── config.py                # 配置文件
├── file/
│   ├── ces.pptx                 # PPT模板文件
│   └── model.pptx               # KPI模板示例文件 🆕
├── data/
│   └── test.db                  # SQLite测试数据库 🆕
├── requirements.txt             # 基础依赖库列表
├── requirements_kpi.txt         # KPI功能依赖库 🆕
├── test_ppt_replacer.py         # 测试脚本
├── KPI_FEATURE_GUIDE.md         # KPI功能详细指南 🆕
├── README.md                    # 使用说明（本文档）
└── prd_optimized.md             # 产品需求文档
```

## 测试程序

### 静态文本替换测试
```bash
python test_ppt_replacer.py
```

测试内容包括：
- 配置文件验证
- 基本功能测试
- 文字替换测试
- 命令行界面测试

### KPI功能测试 🆕
```bash
# 激活虚拟环境
conda activate envs/pptup_env

# 初始化测试数据库
python src/init_test_database.py

# 测试纯文本KPI替换
python test_format_preserve.py

# 测试PPT文件KPI替换
python src/kpi_ppt_command.py -t file/model.pptx -m 202507 -v

# 调试KPI数据获取
python debug_kpi_data.py
```

## 使用示例

### 静态文本替换示例

#### 示例1：处理默认模板
```bash
# 处理默认模板文件
python ppt_replacer.py -t file/ces.pptx

# 输出：file/ces_updated_20240101_120000.pptx
```

#### 示例2：指定输出文件名
```bash
# 指定输出文件名
python src/ppt_generator.py -t file/model.pptx -o file/ppt_report_202507.pptx -m 202507  
# 输出：monthly_report.pptx
```

#### 示例3：详细模式查看处理过程
```bash
# 启用详细模式
python ppt_replacer.py -t file/ces.pptx -v

# 会显示详细的处理信息和日志
```

### KPI动态替换示例 🆕

#### 示例1：基本KPI替换
```bash
# 激活虚拟环境
conda activate envs/pptup_env

# 基本KPI替换（202507月份数据）
python src/kpi_ppt_command.py -t file/model.pptx -m 202507

# 输出：file/model_kpi_updated_20241229_123456.pptx
```

#### 示例2：详细模式KPI替换
```bash
# 详细模式，查看完整处理过程
python src/kpi_ppt_command.py -t file/model.pptx -m 202507 -v

# 显示数据库查询、SQL执行、数据替换等详细信息
```

#### 示例3：自定义输出和数据库
```bash
# 指定输出文件和数据库配置
python src/kpi_ppt_command.py -t file/model.pptx -m 202507 \
    -o 全球通分析报告_202507.pptx --db-config mysql_prod
```

#### 示例4：KPI数据映射
假设PPT模板包含：
```
收入情况：
本月全球通客户收入为 {{kpi_1_1}} 亿元，较上月减少 {{kpi_1_2}} 万元。
拍照全球通客户收入为 {{kpi_1_3}} 亿元，较上月减少 {{kpi_1_4}} 万元。

客户分析：
全球通客户数为 {{kpi_2_1}} 万户，白金及以上客户为 {{kpi_2_2}} 万户。
```

替换后输出：
```
收入情况：
本月全球通客户收入为 5.8 亿元，较上月减少 -101 万元。
拍照全球通客户收入为 5.5 亿元，较上月减少 -112 万元。

客户分析：
全球通客户数为 156.7 万户，白金及以上客户为 23.4 万户。
```

## 输出说明

### 成功处理
程序成功运行后会：
- 在指定位置生成新的PPT文件
- 显示处理结果统计
- 生成带时间戳的日志文件

### 文件命名规则
如果没有指定输出文件名，程序会自动生成：
```
原文件名_updated_YYYYMMDD_HHMMSS.pptx
```

## 常见问题

### 静态文本替换问题

#### Q1: 提示"模板文件不存在"
**A**: 请确保PPT模板文件路径正确，支持的格式为 `.ppt` 或 `.pptx`

#### Q2: 程序运行但没有替换内容
**A**: 请检查PPT模板中是否包含正确格式的占位符（如 `{{analysis_text1}}`）

#### Q3: 替换后格式不正确
**A**: 请确保系统已安装"微软雅黑"字体，或修改配置文件中的字体设置

#### Q4: 文件太大处理缓慢
**A**: 程序支持最大50MB的文件，超大文件建议优化模板大小

### KPI动态替换问题 🆕

#### Q5: 提示"数据库连接失败"
**A**: 
- 检查数据库配置是否正确
- 确认数据库服务是否运行
- 验证用户名密码是否正确
- 使用 `python src/init_test_database.py` 初始化测试数据库

#### Q6: KPI占位符没有被替换
**A**: 
- 检查占位符格式是否正确（`{{kpi_X_Y}}`）
- 确认数据库中存在对应的 `anaylsis_sql_id`
- 验证 `sql_flag = 1` 
- 使用 `-v` 参数查看详细日志

#### Q7: 字体大小被修改了
**A**: 
- 新版本已修复此问题，使用运行块级别替换
- 确保使用最新的 `enhanced_ppt_processor.py`
- 替换时会100%保持原有格式

#### Q8: 月份参数格式错误
**A**: 
- 确保格式为 YYYYMM（如 202507）
- 月份范围：01-12
- 年份范围：2020-2030

#### Q9: SQL执行失败
**A**: 
- 检查数据库中的 `top_sql_test` 字段内容
- 确认SQL语法是否正确
- 验证表名和字段名是否存在
- 使用 `python debug_kpi_data.py` 调试

#### Q10: 虚拟环境问题
**A**: 
- 确保激活正确的虚拟环境：`conda activate envs/pptup_env`
- 安装必要依赖：`pip install -r requirements_kpi.txt`
- 检查Python版本：Python 3.7+

## 技术支持

### 调试和日志

#### 静态文本替换
如遇到问题，请查看：
1. 程序生成的日志文件
2. 运行测试脚本检查环境
3. 确认PPT模板格式正确

#### KPI动态替换 🆕
如遇到问题，可以：
1. 查看详细日志：使用 `-v` 参数运行
2. 检查数据库：运行 `python debug_kpi_data.py`
3. 测试连接：运行 `python src/init_test_database.py`
4. 查看日志文件：`kpi_ppt_log_YYYYMMDD.log`

#### 编程接口
```python
# KPI替换编程接口示例
from src.enhanced_ppt_processor import EnhancedPPTProcessor

# 初始化处理器
processor = EnhancedPPTProcessor("template.pptx")

# 加载模板
processor.load_template()

# 执行完整替换（包含KPI和传统占位符）
results = processor.process_complete_replacement("202507")

# 保存结果
processor.save_presentation("output.pptx")
```

## PPT报告生成器 🆕

### 功能概述

`src/ppt_generator.py` 是一个多功能的PPT报告生成工具，集成了数据分析、SQL处理和PPT生成功能。它将原来需要多个工具才能完成的工作整合到一个命令中。

#### 核心功能

1. **PPT生成模式**: 完整的数据分析+PPT生成流程
2. **SQL执行模式**: 快速测试和验证分析任务的SQL
3. **SQL预览模式**: 显示处理后的SQL，不执行
4. **分析配置支持**: 支持多种分析配置（全球通/中高端）
5. **任务过滤**: 支持指定单个或多个分析任务
6. **月份参数处理**: 自动处理月份变量替换

### 使用方法

#### 1. PPT生成模式
```bash
# 激活虚拟环境
conda activate envs/pptup_env
# 生成完整PPT报告（默认全球通分析）
python src/ppt_generator.py -t file/model.pptx -o file/ppt_report_202507.pptx -m 202507

# 指定特定分析任务
python src/ppt_generator.py -t file/model.pptx -o file/ppt_report_202507.pptx -m 202507 --sql-id 5

# 使用中高端分析配置
python src/ppt_generator.py -t file/zgd/zgd_model.pptx -o file/zgd/ppt_zgd_report_202508.pptx -m 202508 -a 2 --sql-id 1
# 使用全球通分析配置
python src/ppt_generator.py -t file/qqt/qqt_model.pptx -o file/qqt/ppt_qqt_report_202508.pptx -m 202508 -a 1 
# 指定多个任务
python src/ppt_generator.py -t file/zgd/zgd_model.pptx -o file/ppt_report_202507_add.pptx -m 202507 --sql-id 1 13 18 19 -a 2
```

#### 示例1：基本KPI替换
```bash

# 基本KPI替换（202507月份数据）
python src/kpi_ppt_command.py -t file/model.pptx -m 202507

# 输出：file/model_kpi_updated_20241229_123456.pptx
```

#### 示例2：详细模式KPI替换
```bash
# 详细模式，查看完整处理过程 -a 2 中高端分析
python src/kpi_ppt_command.py -t file/zgd/ppt_zgd_report_202508.pptx -m 202508 -v -a 2 --sql-id 1 2 3
# 详细模式，查看完整处理过程 -a 1 全球通分析
python src/kpi_ppt_command.py -t file/qqt/ppt_qqt_report_202508.pptx -m 202508 -v -a 1 --sql-id 1 2 3

# 显示数据库查询、SQL执行、数据替换等详细信息

# 使用中高端分析配置处理所有KPI
python src/kpi_ppt_command.py -t file/zgd/ppt_report_202507.pptx -m 202507 -a 2

# 使用全球通分析配置
python src/kpi_ppt_command.py -t file/qqt/ppt_report_202507.pptx -m 202507 -a 1

# 指定特定的SQL ID
python src/kpi_ppt_command.py -t file/zgd/ppt_report_202507.pptx -m 202507 -a 2 --sql-id 1 2 3
```


#### 2. SQL执行模式
```bash
# 处理分析任务的SQL并执行
python src/ppt_generator.py -t file/model.pptx -m 202507 --sql-id 5 --execute

# 处理自定义SQL模板并执行
python src/ppt_generator.py -t file/model.pptx -m 202507 -s "SELECT * FROM table WHERE month = {op_month}" --execute

# 从文件读取SQL模板并执行
python src/ppt_generator.py -t file/model.pptx -m 202507 -f sql_template.sql --execute
```

#### 3. SQL预览模式
```bash
# 只显示处理后的SQL，不执行
python src/ppt_generator.py -t file/model.pptx -m 202507 -s "SELECT * FROM table WHERE month = {op_month}"

# 显示分析任务的处理后SQL
python src/ppt_generator.py -t file/model.pptx -m 202507 --sql-id 5
```

### 参数说明

| 参数 | 简写 | 说明 | 是否必需 | 示例 |
|------|------|------|----------|------|
| `--template` | `-t` | PPT模板文件路径 | 是 | `file/model.pptx` |
| `--output` | `-o` | 输出PPT文件路径 | PPT模式必需 | `file/report.pptx` |
| `--month` | `-m` | 月份参数（YYYYMM） | 是 | `202507` |
| `--sql-id` | `--id` | 指定分析任务SQL ID | 否 | `5` 或 `1 2 3` |
| `--analysis-id` | `-a` | 分析配置ID | 否 | `1`(全球通), `2`(中高端) |
| `--execute` | `-e` | 实际执行SQL | 否 | - |
| `--sql` | `-s` | SQL模板 | SQL模式 | `"SELECT * FROM ..."` |
| `--file` | `-f` | SQL文件路径 | SQL模式 | `sql_template.sql` |

## 月份参数处理工具

### 功能概述

月份参数处理工具用于处理格式为YYYYMM的月份参数，自动计算上个月参数，并替换SQL模板中的变量。

#### 核心功能

1. **月份解析**: 将202507格式的月份字符串解析为当前月份和上个月份
2. **跨年处理**: 自动处理跨年情况（如202501 → 上个月为202412）
3. **SQL变量替换**: 替换SQL中的{op_month}和{last_op_month}变量
4. **错误验证**: 验证月份格式和范围的有效性

### 使用方法

#### 1. 基础月份处理

```bash
# 只处理月份参数
python src/trigger_month.py 202507
```

输出：
```
🚀 触发月份命令: 202507
✅ 当前月份参数: 202507
✅ 上个月份参数: 202506
```

#### 2. SQL模板替换

```bash
# 处理SQL模板中的变量
python src/trigger_month.py 202507 "SELECT * FROM table WHERE month = {op_month} AND last_month = {last_op_month}"
```

输出：
```
🚀 触发月份命令: 202507
✅ 当前月份参数: 202507
✅ 上个月份参数: 202506

📝 处理后的SQL:
SELECT * FROM table WHERE month = 202507 AND last_month = 202506
```

#### 3. 高级命令行工具

```bash
# 基础月份处理
python src/month_command.py --month 202507

# SQL模板处理
python src/month_command.py --month 202507 --sql "SELECT * FROM table WHERE month = {op_month}"

# 从文件读取SQL模板
python src/month_command.py --month 202507 --file src/test_sql_template.sql

# 处理数据库中的分析任务
python src/month_command.py --month 202507 --tasks

# 处理指定SQL ID的任务（单个）
python src/month_command.py --month 202507 --tasks --sql-id 5

# 处理指定SQL ID的任务（多个）
python src/month_command.py --month 202507 --tasks --sql-id 5 6 7

# 使用中高端分析配置
python src/month_command.py --month 202507 --tasks --sql-id 5 -a 2

# 实际执行SQL（加上--execute参数）
python src/month_command.py --month 202507 --tasks --sql-id 5 --execute
```

### 月份参数示例

| 输入月份 | 当前月份 | 上个月份 | 说明 |
|---------|----------|----------|------|
| 202507  | 202507   | 202506   | 正常情况 |
| 202501  | 202501   | 202412   | 跨年情况 |
| 202512  | 202512   | 202511   | 年末情况 |

### 分析配置说明

系统支持多种分析配置，通过 `--analysis-id` 或 `-a` 参数指定：

| 配置ID | 分析类型 | 说明 |
|---------|----------|------|
| `1` | 全球通"量质构效"分析 | 默认配置，适用于全球通业务分析 |
| `2` | 中高端"量质构效"分析 | 适用于中高端业务分析 |

### SQL变量说明

在SQL模板中可以使用以下变量：

- `{op_month}`: 当前月份参数
- `{last_op_month}`: 上个月份参数

示例SQL模板：
```sql
SELECT 
    city_name,
    qqt_amt,
    pzqqt_amt
FROM anaylsis_qqt_lzgx_st_mm 
WHERE op_month = {op_month}
  AND last_month = {last_op_month}
ORDER BY qqt_amt DESC;
```

### 与数据库集成

工具可以与现有的数据库分析任务集成：

```bash
# 处理数据库中所有包含月份变量的分析任务
python src/month_command.py --month 202507 --tasks

# 处理指定ID的分析任务（定制化更新）
python src/month_command.py --month 202507 --tasks --sql-id 1 2 3

# 实际执行分析任务
python src/month_command.py --month 202507 --tasks --execute
python src/month_command.py --month 202507 --tasks --sql-id 5 --execute
```

#### SQL ID定制化处理

通过`--sql-id`参数，可以精确指定要处理的分析任务：

- **单个任务**: `--sql-id 5`
- **多个任务**: `--sql-id 5 6 7 8`
- **与执行结合**: `--sql-id 5 --execute`

#### 使用场景

- **全量处理**: 不指定SQL ID，处理所有任务
- **定制处理**: 指定特定的SQL ID，只处理指定任务
- **批量更新**: 指定多个SQL ID，批量处理多个任务

### 编程接口

#### MonthProcessor类

```python
from src.month_processor import MonthProcessor

processor = MonthProcessor()

# 解析月份
op_month, last_op_month = processor.parse_month("202507")
print(f"当前月份: {op_month}, 上个月份: {last_op_month}")

# 替换SQL变量
sql_template = "SELECT * FROM table WHERE month = {op_month}"
processed_sql = processor.replace_sql_variables(sql_template, op_month, last_op_month)
print(processed_sql)
```

#### 触发函数

```python
from src.trigger_month import trigger_month_command, replace_sql_with_month

# 触发月份命令
result = trigger_month_command("202507")
if result['success']:
    print(f"当前月份: {result['op_month']}")
    print(f"上个月份: {result['last_op_month']}")

# 替换SQL
sql = replace_sql_with_month("SELECT * WHERE month = {op_month}", "202507")
print(sql)
```

## 版本信息

- **当前版本**: v2.0 🆕
- **更新日期**: 2024年12月
- **兼容性**: Python 3.7+, Windows 10/11

### 版本历史
- **v2.0** (2024-12): 新增KPI动态替换功能，支持数据库查询和月份参数处理
- **v1.0** (2024): 基础PPT文本替换功能

### 新功能亮点 🆕
- ✨ KPI动态数据替换：从数据库自动获取数据
- ✨ 格式完全保持：运行块级别替换，100%保持原有样式
- ✨ 智能月份处理：自动计算当前月和上月参数
- ✨ 多数据库支持：SQLite、MySQL等数据库支持
- ✨ 详细日志记录：完整的处理过程追踪

## 工具功能对比

系统提供了三个主要的命令行工具，各有特色：

| 工具 | 主要功能 | 适用场景 | 特殊功能 |
|------|----------|----------|----------|
| `ppt_generator.py` | 一体化PPT生成工具 | 日常报告生成、SQL调试 | 集成所有功能，支持多种模式 |
| `kpi_ppt_command.py` | KPI头部指标更新 | KPI数据替换 | 专注于KPI占位符处理 |
| `month_command.py` | 月份参数处理 | SQL调试、数据查询 | 纯SQL处理，无PPT生成 |

### 推荐使用方式

1. **日常PPT生成**: 优先使用 `ppt_generator.py`
2. **纯KPI更新**: 使用 `kpi_ppt_command.py`
3. **SQL调试**: 使用 `ppt_generator.py` 的SQL模式或 `month_command.py`
4. **开发测试**: 使用 `ppt_generator.py` 的预览模式

---

*功能完善，已投入生产使用！*

## 相关文档
- 📖 [KPI功能详细指南](KPI_FEATURE_GUIDE.md) - KPI替换功能的完整文档
- 📋 [产品需求文档](prd_optimized.md) - 项目需求和设计文档