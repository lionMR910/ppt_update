-- 根据中高端客户数据字段创建MySQL建表语句
-- 表名：中高端客户量质构效指标数据表

CREATE TABLE zhongd_customer_metrics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    
    -- 基础地市信息
    city_name VARCHAR(50) NOT NULL COMMENT '地市',
    
    -- 收入相关字段（单位：万元）
    zhongd_revenue DECIMAL(15,2) COMMENT '中高端客户收入-万元',
    photo_zhongd_revenue DECIMAL(15,2) COMMENT '拍照中高端客户收入-万元',
    
    -- 客户数量相关字段（单位：户）
    current_zhongd_customers BIGINT COMMENT '当前中高端客户-户',
    net_increase_zhongd_customers BIGINT COMMENT '中高端净增客户-户',
    monthly_new_zhongd_customers BIGINT COMMENT '当月新增中高端客户-户',
    monthly_new_zhongd_stock_inflow BIGINT COMMENT '当月新增中高端客户（存量流入）-户',
    monthly_new_zhongd_new_access BIGINT COMMENT '当月新增中高端客户（新入网）-户',
    monthly_outflow_zhongd_customers BIGINT COMMENT '当月流出中高端客户-户',
    monthly_offline_zhongd_customers BIGINT COMMENT '当月离网中高端客户-户',
    monthly_offline_zhongd_portout BIGINT COMMENT '当月离网中高端客户（携出）-户',
    monthly_offline_zhongd_cancel BIGINT COMMENT '当月离网中高端客户（申销）-户',
    monthly_offline_zhongd_debt BIGINT COMMENT '当月离网中高端客户（欠销）-户',
    continuous_zhongd_customers BIGINT COMMENT '连续中高端客户-户',
    
    -- 年度数据
    yearly_new_zhongd_customers BIGINT COMMENT '今年新增中高端客户-户',
    yearly_new_zhongd_stock_inflow BIGINT COMMENT '今年新增中高端客户（存量流入）-户',
    yearly_new_zhongd_new_access BIGINT COMMENT '今年新增中高端客户（新入网）-户',
    photo_zhongd_yearly_outflow BIGINT COMMENT '拍照中高端今年流出客户-户',
    photo_zhongd_yearly_offline BIGINT COMMENT '拍照中高端今年离网客户-户',
    photo_zhongd_yearly_portout BIGINT COMMENT '拍照中高端今年离网客户（携出）-户',
    photo_zhongd_yearly_cancel BIGINT COMMENT '拍照中高端今年离网客户（申销）-户',
    photo_zhongd_yearly_debt BIGINT COMMENT '拍照中高端今年离网客户（欠销）-户',
    photo_zhongd_online_customers BIGINT COMMENT '拍照中高端在网客户-户',
    
    -- 其他客户类型
    family_customers BIGINT COMMENT '组家客户-户',
    broadband_customers BIGINT COMMENT '宽带客户-户',
    group_customers BIGINT COMMENT '集团客户-户',
    long_tenure_customers BIGINT COMMENT '长机龄客户-户',
    billing_customers BIGINT COMMENT '出账客户-户',
    communication_customers BIGINT COMMENT '通信客户-户',
    mobile_internet_customers BIGINT COMMENT '手机上网客户',
    g5_terminal_customers BIGINT COMMENT '5G终端客户-户',
    g5_network_customers BIGINT COMMENT '5G登网客户-户',
    traffic_exceed_customers BIGINT COMMENT '流量超套客户-户',
    traffic_exceed_avg_fee DECIMAL(10,2) COMMENT '流量超套客户户均超套费-元',
    voice_exceed_customers BIGINT COMMENT '语音超套客户-户',
    voice_exceed_avg_fee DECIMAL(10,2) COMMENT '语音超套客户户均超套费-元',
    
    -- 比率指标（单位：%）
    zhongd_value_retention_rate DECIMAL(5,2) COMMENT '中高端客户价值保拓率-%',
    cmcc_app_active_rate DECIMAL(5,2) COMMENT '中国移动APP当月活跃率-%',
    domestic_roaming_rate DECIMAL(5,2) COMMENT '国漫渗透率-%',
    inter_province_roaming_rate DECIMAL(5,2) COMMENT '常漫客户（省际漫游）渗透率-%',
    call_10086_in_rate DECIMAL(5,2) COMMENT '10086呼入客户占比-%',
    call_10086_out_rate DECIMAL(5,2) COMMENT '10086呼出客户占比-%',
    complaint_rate DECIMAL(5,2) COMMENT '投诉客户占比-%',
    service_cancel_rate DECIMAL(5,2) COMMENT '业务退订客户占比-%',
    activity_continue_rate DECIMAL(5,2) COMMENT '活动接续客户占比-%',
    debt_rate DECIMAL(5,2) COMMENT '欠费客户占比-%',
    
    -- 融合率和其他比率
    zhongd_fixed_mobile_fusion_rate DECIMAL(5,2) COMMENT '中高端客户固移融合率',
    zhongd_effective_fusion_rate DECIMAL(5,2) COMMENT '中高端客户有效融合率',
    abnormal_customer_rate DECIMAL(5,2) COMMENT '异动客户占比',
    elderly_customer_rate DECIMAL(5,2) COMMENT '银发客户占比',
    international_customer_rate DECIMAL(5,2) COMMENT '国际客户占比',
    campus_customer_rate DECIMAL(5,2) COMMENT '校园客户占比',
    
    -- 宽带带宽分类
    broadband_1000mb BIGINT COMMENT '宽带带宽1000mb',
    broadband_500mb BIGINT COMMENT '宽带带宽500mb',
    broadband_300mb BIGINT COMMENT '宽带带宽300mb',
    broadband_200mb BIGINT COMMENT '宽带带宽200mb',
    broadband_100mb BIGINT COMMENT '宽带带宽100mb',
    broadband_below_100mb BIGINT COMMENT '宽带带宽100mb以下',
    no_broadband_zhongd BIGINT COMMENT '无宽带中高端客户',
    fttr_customers BIGINT COMMENT 'fttr客户',
    
    -- TARPU分档（单位：元）
    tarpu_0_below BIGINT COMMENT 'tarpu0元及以下',
    tarpu_0_30 BIGINT COMMENT 'tarpu0_30元',
    tarpu_30_50 BIGINT COMMENT 'tarpu30_50元',
    tarpu_50_100 BIGINT COMMENT 'tarpu50_100元',
    tarpu_100_150 BIGINT COMMENT 'tarpu100_150元',
    tarpu_150_200 BIGINT COMMENT 'tarpu150_200元',
    tarpu_200_300 BIGINT COMMENT 'tarpu200_300元',
    tarpu_300_above BIGINT COMMENT 'tarpu300元以上',
    
    -- DOU分档（单位：GB）
    dou_0gb BIGINT COMMENT 'dou0gb',
    dou_0_1gb BIGINT COMMENT 'dou0_1gb',
    dou_1_5gb BIGINT COMMENT 'dou1_5gb',
    dou_5_10gb BIGINT COMMENT 'dou5_10gb',
    dou_10_20gb BIGINT COMMENT 'dou10_20gb',
    dou_20_30gb BIGINT COMMENT 'dou20_30gb',
    dou_30_50gb BIGINT COMMENT 'dou30_50gb',
    dou_50_100gb BIGINT COMMENT 'dou50_1000gb',
    dou_100_200gb BIGINT COMMENT 'dou100_200gb',
    dou_200gb_above BIGINT COMMENT 'dou200gb_1',
    
    -- 网龄分档
    tenure_0_1_year BIGINT COMMENT '网龄0_1年',
    tenure_1_5_year BIGINT COMMENT '网龄1_5年',
    tenure_5_10_year BIGINT COMMENT '网龄5_10年',
    tenure_10_15_year BIGINT COMMENT '网龄10_15年',
    tenure_15_20_year BIGINT COMMENT '网龄15_20年',
    tenure_20_30_year BIGINT COMMENT '网龄20_30年',
    tenure_30_above_year BIGINT COMMENT '网龄30年以上',
    
    -- 年龄分档
    age_empty_abnormal BIGINT COMMENT '年龄为空或异常客户',
    age_0_18 BIGINT COMMENT '岁龄0_18岁',
    age_18_25 BIGINT COMMENT '岁龄18_25岁',
    age_25_35 BIGINT COMMENT '岁龄25_35岁',
    age_35_45 BIGINT COMMENT '岁龄35_45岁',
    age_45_55 BIGINT COMMENT '岁龄45_55岁',
    age_55_60 BIGINT COMMENT '岁龄55_60岁',
    age_60_65 BIGINT COMMENT '岁龄60_65岁',
    age_65_70 BIGINT COMMENT '岁龄65_70岁',
    age_70_100 BIGINT COMMENT '岁龄70_100岁',
    
    -- 价值变化客户
    value_decrease_customers BIGINT COMMENT '价值下降客户',
    total_decrease_value DECIMAL(15,2) COMMENT '下降总价值',
    value_increase_customers BIGINT COMMENT '价值提升客户',
    total_increase_value DECIMAL(15,2) COMMENT '提升总价值',
    
    -- 合约相关
    contract_customers BIGINT COMMENT '合约客户',
    contract_customers_effective_fusion BIGINT COMMENT '合约客户_有效融合口径',
    terminal_contract_customers BIGINT COMMENT '终端合约客户',
    package_downgrade_customers BIGINT COMMENT '套餐降档客户',
    package_upgrade_customers BIGINT COMMENT '套餐升档客户',
    
    -- 套餐费实收分档（单位：元）
    package_fee_0_below BIGINT COMMENT '套餐费实收0元及以下',
    package_fee_0_10 BIGINT COMMENT '套餐费实收0_10元',
    package_fee_10_30 BIGINT COMMENT '套餐费实收10_30元',
    package_fee_30_50 BIGINT COMMENT '套餐费实收30_50元',
    package_fee_50_80 BIGINT COMMENT '套餐费实收50_80元',
    package_fee_80_108 BIGINT COMMENT '套餐费实收80_108元',
    package_fee_108_150 BIGINT COMMENT '套餐费实收108_150元',
    package_fee_150_200 BIGINT COMMENT '套餐费实收150_200元',
    package_fee_200_300 BIGINT COMMENT '套餐费实收200_300元',
    package_fee_300_above BIGINT COMMENT '套餐费实收300元以上',
    
    -- 拍照中高端客户指标
    photo_zhongd_tarpu DECIMAL(10,2) COMMENT '拍照中高端客户tarpu',
    photo_zhongd_dou DECIMAL(10,2) COMMENT '拍照中高端客户dou',
    photo_zhongd_monthly_traffic_saturation DECIMAL(5,2) COMMENT '拍照中高端客户通用包月流量饱和度',
    photo_zhongd_outgoing_mou DECIMAL(10,2) COMMENT '拍照中高端客户主叫mou',
    
    -- 到达中高端客户指标
    target_zhongd_tarpu DECIMAL(10,2) COMMENT '到达中高端客户tarpu_元',
    target_zhongd_dou DECIMAL(10,2) COMMENT '到达中高端客户dou_gb',
    target_zhongd_monthly_traffic_saturation DECIMAL(5,2) COMMENT '到达中高端客户通用包月流量饱和度',
    target_zhongd_outgoing_mou DECIMAL(10,2) COMMENT '到达中高端客户主叫mou_分钟',
    
    -- 时间戳
    op_month INT COMMENT '操作月份',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX idx_city_month (city_name, op_month),
    INDEX idx_op_month (op_month),
    INDEX idx_zhongd_revenue (zhongd_revenue),
    INDEX idx_current_zhongd (current_zhongd_customers)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='中高端客户量质构效指标数据表';

-- 字段对应关系说明
/*
数据类型选择说明：
1. 客户数量字段：使用 BIGINT 类型，支持大数据量
2. 收入金额字段：使用 DECIMAL(15,2)，保证精度，支持万元级别
3. 比率百分比字段：使用 DECIMAL(5,2)，支持到小数点后两位
4. 单价类指标：使用 DECIMAL(10,2)，适合TARPU、DOU等指标
5. 索引设计：基于常用查询条件（地市+月份、收入、客户数）建立索引

字段命名规则：
- 使用英文命名，避免中文字段名
- 统一使用下划线分隔
- 保持语义清晰和一致性
*/