-- 根据数据表格严格按照表头顺序创建MySQL建表语句
-- 表名：全球通量质构效指标数据表

CREATE TABLE global_tongyi_metrics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    
    -- 严格按照表头顺序定义字段
    city_name VARCHAR(50) NOT NULL COMMENT '地市',
    total_customers BIGINT COMMENT '出账客户户数',
    active_customers BIGINT COMMENT '通信客户户数', 
    mobile_internet_customers BIGINT COMMENT '手机上网客户户数',
    g5_terminal_customers BIGINT COMMENT '5G终端客户户数',
    g5_network_customers BIGINT COMMENT '5G网络客户户数',
    traffic_exceed_customers BIGINT COMMENT '流量超出客户户数',
    traffic_exceed_count BIGINT COMMENT '流量超出客户户数超',
    voice_customers BIGINT COMMENT '语音客户户数',
    voice_exceed_customers BIGINT COMMENT '语音客户户数超',
    photo_global_customers BIGINT COMMENT '拍照全球通客户户数',
    photo_global_exceed BIGINT COMMENT '拍照全球通客户超出户数',
    photo_global_transfer_in BIGINT COMMENT '拍照全球通转入户数',
    photo_global_transfer_out BIGINT COMMENT '拍照全球通转出户数',
    photo_global_revenue DECIMAL(15,2) COMMENT '拍照全球通收入-元',
    penetration_rate DECIMAL(5,2) COMMENT '渗透率%',
    traffic_customers_ratio DECIMAL(5,2) COMMENT '流量客户占比%',
    iot_customers BIGINT COMMENT '10088接装客户数',
    contract_customers BIGINT COMMENT '合约客户数',
    contract_ratio DECIMAL(5,2) COMMENT '合约(含套餐)占比%',
    package_customers BIGINT COMMENT '套餐客户数',
    package_new_customers BIGINT COMMENT '套餐新客户数',
    package_upgrade_customers BIGINT COMMENT '套餐升级客户数',
    package_maintain_customers BIGINT COMMENT '套餐维系客户数',
    
    -- 套餐实收各档位 (单位：元)
    package_revenue_0_10 DECIMAL(15,2) COMMENT '套餐实收0-10元',
    package_revenue_10_30 DECIMAL(15,2) COMMENT '套餐实收(10,30)元', 
    package_revenue_30_50 DECIMAL(15,2) COMMENT '套餐实收(30,50)元',
    package_revenue_50_80 DECIMAL(15,2) COMMENT '套餐实收(50,80)元',
    package_revenue_80_100 DECIMAL(15,2) COMMENT '套餐实收(80,100)元',
    package_revenue_100_150 DECIMAL(15,2) COMMENT '套餐实收(100,150)元',
    package_revenue_150_200 DECIMAL(15,2) COMMENT '套餐实收(150,200)元',
    package_revenue_200_300 DECIMAL(15,2) COMMENT '套餐实收(200,300)元',
    package_revenue_300_above DECIMAL(15,2) COMMENT '套餐实收300元以上',
    
    -- 时间戳
    op_month INT COMMENT '操作月份',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX idx_city_month (city_name, op_month),
    INDEX idx_op_month (op_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='全球通量质构效指标数据表';

-- 创建表的详细说明
/*
字段对应关系：
1. 地市 -> city_name
2. 出账客户户数 -> total_customers
3. 通信客户户数 -> active_customers
4. 手机上网客户户数 -> mobile_internet_customers
5. 5G终端客户户数 -> g5_terminal_customers
6. 5G网络客户户数 -> g5_network_customers
7. 流量超出客户户数 -> traffic_exceed_customers
8. 流量超出客户户数超 -> traffic_exceed_count
9. 语音客户户数 -> voice_customers
10. 语音客户户数超 -> voice_exceed_customers
11. 拍照全球通客户户数 -> photo_global_customers
12. 拍照全球通客户超出户数 -> photo_global_exceed
13. 拍照全球通转入户数 -> photo_global_transfer_in
14. 拍照全球通转出户数 -> photo_global_transfer_out
15. 拍照全球通收入-元 -> photo_global_revenue
16. 渗透率% -> penetration_rate
17. 流量客户占比% -> traffic_customers_ratio
18. 10088接装客户数 -> iot_customers
19. 合约客户数 -> contract_customers
20. 合约(含套餐)占比% -> contract_ratio
21. 套餐客户数 -> package_customers
22. 套餐新客户数 -> package_new_customers
23. 套餐升级客户数 -> package_upgrade_customers
24. 套餐维系客户数 -> package_maintain_customers
25-33. 套餐实收各档位 -> package_revenue_xxx
*/

-- 插入示例数据 (基于表格数据)
INSERT INTO global_tongyi_metrics (
    city_name, total_customers, active_customers, mobile_internet_customers,
    g5_terminal_customers, g5_network_customers, traffic_exceed_customers, traffic_exceed_count,
    voice_customers, voice_exceed_customers, photo_global_customers, photo_global_exceed,
    photo_global_transfer_in, photo_global_transfer_out, photo_global_revenue, penetration_rate, traffic_customers_ratio,
    iot_customers, contract_customers, contract_ratio, package_customers, package_new_customers,
    package_upgrade_customers, package_maintain_customers, package_revenue_0_10, package_revenue_10_30, package_revenue_30_50,
    package_revenue_50_80, package_revenue_80_100, package_revenue_100_150, package_revenue_150_200, package_revenue_200_300,
    package_revenue_300_above, op_month
) VALUES (
    '沈阳', 1318363, 1316519, 1288543, 
    1108158, 1034048, 131174, 49, 
    965200, 24, 11496, 1491,
    2377, 1.18, 1.43, 49.98, 911313,
    98535, 79558, 88.97, 8177, 60759,
    228250, 114338, 307217, 260109, 191104,
    166839, 45456, 5893, 202507
);