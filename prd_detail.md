# 数据分析自动化系统 - 产品需求文档 (PRD)

## 1. 项目概述

### 1.1 项目背景
开发一个基于大模型的数据分析自动化系统，实现从数据库取数、AI分析、结果回写的完整闭环流程，提升数据分析效率和质量。

### 1.2 核心目标
- 自动化执行预配置的SQL查询
- 利用大模型智能分析数据
- 自动生成分析结论并存储
- 支持批量处理和定时任务

### 1.3 系统架构
```
数据库配置表 → SQL执行引擎 → 数据预处理 → 大模型分析 → 结果回写 → 日志记录
```

## 2. 功能需求

### 2.1 核心功能模块

#### 2.1.1 配置管理模块
- **数据源配置**：支持多种数据库连接
- **SQL模板管理**：维护分析SQL语句
- **分析任务配置**：设置分析参数和触发条件

#### 2.1.2 数据查询模块
- **SQL执行引擎**：安全执行预配置SQL
- **数据验证**：检查查询结果的有效性
- **数据预处理**：格式化数据用于AI分析

#### 2.1.3 AI分析模块
- **大模型集成**：对接Qwen3:14b模型
- **提示词管理**：可配置的分析提示模板
- **结果解析**：提取和验证AI分析结果

#### 2.1.4 结果管理模块
- **数据回写**：更新分析结论到数据库
- **版本控制**：记录分析历史和变更
- **结果验证**：确保分析结果质量

## 3. 数据库设计

### 3.1 主表结构优化

#### 3.1.1 分析配置表
```sql
CREATE TABLE `analysis_deploy_market_def` (
  `analysis_sql_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '分析元数据唯一ID',
  `analysis_id` bigint(20) NOT NULL COMMENT '分析ID',
  `analysis_name` varchar(128) NOT NULL COMMENT '分析名称',
  `analysis_lev1_name` varchar(128) NULL COMMENT '分类名称1',
  `analysis_lev2_name` varchar(128) NULL COMMENT '分类名称2',
  `analysis_sql_text` text NOT NULL COMMENT '分析SQL语句',
  `op_month` int(11) NOT NULL COMMENT '分析月份',
  `analysis_text` text NULL COMMENT '分析结论',
  `sql_flag` tinyint(1) DEFAULT 1 COMMENT '生效标记(0:禁用,1:启用)',
  `prompt_template` text NULL COMMENT '分析提示词模板',
  `data_source` varchar(64) DEFAULT 'default' COMMENT '数据源标识',
  `priority` int(11) DEFAULT 0 COMMENT '执行优先级',
  `max_rows` int(11) DEFAULT 10000 COMMENT '最大查询行数限制',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `last_analysis_time` datetime NULL COMMENT '最后分析时间',
  `analysis_status` tinyint(1) DEFAULT 0 COMMENT '分析状态(0:待分析,1:分析中,2:完成,3:失败)',
  PRIMARY KEY (`analysis_sql_id`),
  INDEX `idx_analysis_id` (`analysis_id`),
  INDEX `idx_op_month_flag` (`op_month`, `sql_flag`),
  INDEX `idx_status_priority` (`analysis_status`, `priority`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='市场分析配置表';
```

#### 3.1.2 分析执行日志表
```sql
CREATE TABLE `analysis_execution_log` (
  `log_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `analysis_sql_id` bigint(20) NOT NULL COMMENT '关联的分析配置ID',
  `execution_start_time` datetime NOT NULL COMMENT '执行开始时间',
  `execution_end_time` datetime NULL COMMENT '执行结束时间',
  `execution_status` tinyint(1) NOT NULL COMMENT '执行状态(0:运行中,1:成功,2:失败)',
  `data_rows_count` int(11) NULL COMMENT '查询数据行数',
  `ai_response_time` int(11) NULL COMMENT 'AI响应时间(秒)',
  `error_message` text NULL COMMENT '错误信息',
  `analysis_result` text NULL COMMENT 'AI分析原始结果',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`log_id`),
  INDEX `idx_analysis_sql_id` (`analysis_sql_id`),
  INDEX `idx_execution_time` (`execution_start_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='分析执行日志表';
```

#### 3.1.3 系统配置表
```sql
CREATE TABLE `system_config` (
  `config_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `config_key` varchar(128) NOT NULL COMMENT '配置键',
  `config_value` text NOT NULL COMMENT '配置值',
  `config_desc` varchar(255) NULL COMMENT '配置描述',
  `config_type` varchar(32) DEFAULT 'string' COMMENT '配置类型',
  `is_active` tinyint(1) DEFAULT 1 COMMENT '是否激活',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`config_id`),
  UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';
```

### 3.2 初始配置数据
```sql
-- 大模型配置
INSERT INTO `system_config` (`config_key`, `config_value`, `config_desc`, `config_type`) VALUES
('ai_model_base_url', 'http://36.138.184.222:11434', '大模型API基础URL', 'string'),
('ai_model_name', 'qwen3:14b', '使用的大模型名称', 'string'),
('ai_model_timeout', '120', 'AI请求超时时间(秒)', 'integer'),
('ai_model_max_retries', '3', 'AI请求最大重试次数', 'integer'),
('default_prompt_template', '请分析以下数据并提供专业的结论和建议：\n\n数据：\n{data}\n\n请从以下几个角度进行分析：\n1. 数据趋势分析\n2. 关键指标解读\n3. 潜在问题识别\n4. 改进建议\n\n请用简洁专业的语言输出分析结论。', '默认分析提示词模板', 'text');
```

## 4. 技术架构

### 4.1 系统架构设计
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web管理界面    │    │   API服务层      │    │   定时任务调度   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────────┐
         │                核心服务层                            │
         │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
         │  │ 配置管理器  │  │ SQL执行器   │  │ AI分析器    │  │
         │  └─────────────┘  └─────────────┘  └─────────────┘  │
         │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
         │  │ 数据预处理  │  │ 结果回写器  │  │ 日志记录器  │  │
         │  └─────────────┘  └─────────────┘  └─────────────┘  │
         └─────────────────────────────────────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────────┐
         │                数据访问层                            │
         │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
         │  │ 数据库连接池│  │ Redis缓存   │  │ 大模型API   │  │
         │  └─────────────┘  └─────────────┘  └─────────────┘  │
         └─────────────────────────────────────────────────────┘
```

### 4.2 技术选型

#### 4.2.1 后端技术栈
- **编程语言**: Python 3.9+
- **Web框架**: FastAPI / Flask
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy
- **任务调度**: Celery + Redis
- **HTTP客户端**: httpx / requests
- **配置管理**: Pydantic

#### 4.2.2 核心依赖库
```python
# requirements.txt
fastapi==0.104.1
sqlalchemy==2.0.23
pymysql==1.1.0
redis==5.0.1
celery==5.3.4
httpx==0.25.2
pydantic==2.5.0
pandas==2.1.3
python-multipart==0.0.6
uvicorn==0.24.0
```

## 5. 核心业务流程

### 5.1 分析执行流程
```
1. 系统启动/定时触发
   ↓
2. 扫描待分析任务 (sql_flag=1 且 analysis_status=0)
   ↓
3. 按优先级排序执行
   ↓
4. 更新状态为"分析中"
   ↓
5. 执行SQL查询
   ↓
6. 数据预处理和验证
   ↓
7. 调用大模型分析
   ↓
8. 解析和验证AI结果
   ↓
9. 回写分析结论
   ↓
10. 更新状态为"完成"
    ↓
11. 记录执行日志
```

### 5.2 错误处理流程
```
异常发生
   ↓
记录错误日志
   ↓
更新任务状态为"失败"
   ↓
判断是否可重试
   ↓
是 → 加入重试队列
   ↓
否 → 发送告警通知
```

## 6. 接口设计

### 6.1 RESTful API规范

#### 6.1.1 分析任务管理
```python
# 获取分析任务列表
GET /api/v1/analysis/tasks?page=1&size=20&status=0

# 创建分析任务
POST /api/v1/analysis/tasks
{
  "analysis_name": "市场份额分析",
  "analysis_lev1_name": "市场分析",
  "analysis_lev2_name": "份额分析",
  "analysis_sql_text": "SELECT * FROM market_data WHERE month = ?",
  "op_month": 202401,
  "prompt_template": "请分析市场数据...",
  "priority": 1
}

# 更新分析任务
PUT /api/v1/analysis/tasks/{task_id}

# 删除分析任务
DELETE /api/v1/analysis/tasks/{task_id}

# 手动触发分析
POST /api/v1/analysis/tasks/{task_id}/execute
```

#### 6.1.2 分析结果查询
```python
# 获取分析结果
GET /api/v1/analysis/results/{task_id}

# 获取执行日志
GET /api/v1/analysis/logs?task_id={task_id}&page=1&size=20
```

#### 6.1.3 系统配置管理
```python
# 获取系统配置
GET /api/v1/system/config

# 更新系统配置
PUT /api/v1/system/config
{
  "ai_model_timeout": 180,
  "ai_model_max_retries": 5
}
```

## 7. 安全设计

### 7.1 数据安全
- **SQL注入防护**: 使用参数化查询，禁止动态SQL拼接
- **权限控制**: 数据库连接使用最小权限原则
- **数据脱敏**: 敏感数据在日志中脱敏处理
- **访问审计**: 记录所有数据访问和修改操作

### 7.2 API安全
- **认证授权**: JWT Token认证机制
- **请求限流**: 防止API滥用
- **输入验证**: 严格验证所有输入参数
- **HTTPS通信**: 强制使用HTTPS协议

### 7.3 AI模型安全
- **输入长度限制**: 防止过长输入导致的问题
- **输出过滤**: 过滤可能的有害输出内容
- **超时控制**: 防止长时间等待
- **重试机制**: 智能重试避免系统过载

## 8. 性能优化

### 8.1 数据库优化
- **索引优化**: 关键查询字段建立合适索引
- **连接池**: 使用数据库连接池提升性能
- **分页查询**: 大数据量分页处理
- **查询缓存**: 缓存频繁查询结果

### 8.2 系统性能
- **异步处理**: 使用异步任务处理长时间操作
- **并发控制**: 合理控制并发执行数量
- **内存管理**: 及时释放大对象内存
- **监控告警**: 实时监控系统性能指标

## 9. 监控与运维

### 9.1 监控指标
- **业务指标**: 任务执行成功率、平均执行时间、AI响应时间
- **系统指标**: CPU、内存、磁盘使用率
- **数据库指标**: 连接数、查询响应时间、锁等待
- **API指标**: 请求量、响应时间、错误率

### 9.2 日志管理
- **结构化日志**: 使用JSON格式记录日志
- **日志级别**: 合理设置日志级别
- **日志轮转**: 定期清理历史日志
- **集中管理**: 统一收集和分析日志

### 9.3 告警机制
- **实时告警**: 关键错误实时通知
- **阈值告警**: 性能指标超过阈值告警
- **定期报告**: 定期生成系统运行报告

## 10. 部署方案

### 10.1 环境要求
- **操作系统**: CentOS 7+ / Ubuntu 20.04+
- **Python**: 3.9+
- **MySQL**: 8.0+
- **Redis**: 6.0+
- **内存**: 8GB+
- **存储**: 100GB+

### 10.2 部署架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx反向代理  │    │   Web应用服务器  │    │   Celery Worker │
│                │    │   (FastAPI)     │    │   (后台任务)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────────┐
         │                基础设施层                            │
         │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
         │  │ MySQL数据库 │  │ Redis缓存   │  │ 文件存储    │  │
         │  └─────────────┘  └─────────────┘  └─────────────┘  │
         └─────────────────────────────────────────────────────┘
```

### 10.3 配置文件
```yaml
# config.yaml
database:
  host: localhost
  port: 3306
  username: analysis_user
  password: ${DB_PASSWORD}
  database: analysis_db
  pool_size: 20

redis:
  host: localhost
  port: 6379
  password: ${REDIS_PASSWORD}
  db: 0

ai_model:
  base_url: http://36.138.184.222:11434
  model_name: qwen3:14b
  timeout: 120
  max_retries: 3

scheduler:
  interval_seconds: 300
  max_concurrent_tasks: 5
```

## 11. 测试策略

### 11.1 单元测试
- **核心模块测试**: 覆盖所有核心业务逻辑
- **边界条件测试**: 测试各种边界情况
- **异常处理测试**: 验证异常处理机制

### 11.2 集成测试
- **数据库集成测试**: 验证数据库操作正确性
- **AI模型集成测试**: 验证大模型调用功能
- **端到端测试**: 完整业务流程测试

### 11.3 性能测试
- **负载测试**: 模拟高并发场景
- **压力测试**: 测试系统极限性能
- **稳定性测试**: 长时间运行稳定性

## 12. 项目计划

### 12.1 开发阶段
1. **阶段1（2周）**: 数据库设计、基础框架搭建
2. **阶段2（3周）**: 核心功能开发、SQL执行器、AI集成
3. **阶段3（2周）**: API开发、Web界面开发
4. **阶段4（2周）**: 测试、优化、部署

### 12.2 里程碑
- **M1**: 数据库设计完成，基础框架可运行
- **M2**: 核心分析功能完成，可执行单个任务
- **M3**: 完整系统功能完成，通过集成测试
- **M4**: 系统部署上线，通过验收测试

## 13. 风险管控

### 13.1 技术风险
- **AI模型不可用**: 准备备用模型或降级方案
- **数据库性能瓶颈**: 优化查询、分库分表
- **网络连接不稳定**: 增加重试和容错机制

### 13.2 业务风险
- **SQL安全风险**: 严格验证SQL语句，禁止危险操作
- **数据质量问题**: 增加数据验证和清洗机制
- **分析结果准确性**: 人工抽检和反馈机制

## 14. 成功标准

### 14.1 功能指标
- [ ] 系统能够自动执行预配置的SQL查询
- [ ] 成功集成大模型进行数据分析
- [ ] 分析结果能够自动回写到数据库
- [ ] 提供完整的Web管理界面

### 14.2 性能指标
- [ ] 单个分析任务执行时间 < 5分钟
- [ ] 系统并发处理能力 ≥ 10个任务
- [ ] AI分析准确率 ≥ 85%
- [ ] 系统可用性 ≥ 99%

### 14.3 质量指标
- [ ] 代码测试覆盖率 ≥ 80%
- [ ] 关键业务零错误
- [ ] 完整的操作文档和用户手册
- [ ] 7×24小时稳定运行

---
*文档版本：v1.0*  
*最后更新：2024年*  
*文档状态：待评审*