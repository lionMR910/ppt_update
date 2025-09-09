-- MySQL Create Table Statement based on the provided data structure
-- Table: Global Tongyi Quality Metrics

CREATE TABLE global_tongyi_metrics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Primary Key ID',
    
    -- Fields in strict order according to table header
    city_name VARCHAR(50) NOT NULL COMMENT 'City Name',
    total_customers BIGINT COMMENT 'Total billing customers',
    active_customers BIGINT COMMENT 'Active communication customers', 
    mobile_internet_customers BIGINT COMMENT 'Mobile internet customers',
    g5_terminal_customers BIGINT COMMENT '5G terminal customers',
    g5_network_customers BIGINT COMMENT '5G network customers',
    traffic_exceed_customers BIGINT COMMENT 'Traffic exceed customers',
    traffic_exceed_count BIGINT COMMENT 'Traffic exceed count',
    voice_customers BIGINT COMMENT 'Voice customers',
    voice_exceed_customers BIGINT COMMENT 'Voice exceed customers',
    photo_global_customers BIGINT COMMENT 'Photo Global customers',
    photo_global_exceed BIGINT COMMENT 'Photo Global exceed customers',
    photo_global_transfer_in BIGINT COMMENT 'Photo Global transfer in',
    photo_global_transfer_out BIGINT COMMENT 'Photo Global transfer out',
    photo_global_revenue DECIMAL(15,2) COMMENT 'Photo Global revenue (Yuan)',
    penetration_rate DECIMAL(5,2) COMMENT 'Penetration rate (%)',
    traffic_customers_ratio DECIMAL(5,2) COMMENT 'Traffic customers ratio (%)',
    iot_customers BIGINT COMMENT '10088 installation customers',
    contract_customers BIGINT COMMENT 'Contract customers',
    contract_ratio DECIMAL(5,2) COMMENT 'Contract (including package) ratio (%)',
    package_customers BIGINT COMMENT 'Package customers',
    package_new_customers BIGINT COMMENT 'New package customers',
    package_upgrade_customers BIGINT COMMENT 'Package upgrade customers',
    package_maintain_customers BIGINT COMMENT 'Package maintenance customers',
    
    -- Package revenue by tiers (Yuan)
    package_revenue_0_10 DECIMAL(15,2) COMMENT 'Package revenue 0-10 Yuan',
    package_revenue_10_30 DECIMAL(15,2) COMMENT 'Package revenue (10,30) Yuan', 
    package_revenue_30_50 DECIMAL(15,2) COMMENT 'Package revenue (30,50) Yuan',
    package_revenue_50_80 DECIMAL(15,2) COMMENT 'Package revenue (50,80) Yuan',
    package_revenue_80_100 DECIMAL(15,2) COMMENT 'Package revenue (80,100) Yuan',
    package_revenue_100_150 DECIMAL(15,2) COMMENT 'Package revenue (100,150) Yuan',
    package_revenue_150_200 DECIMAL(15,2) COMMENT 'Package revenue (150,200) Yuan',
    package_revenue_200_300 DECIMAL(15,2) COMMENT 'Package revenue (200,300) Yuan',
    package_revenue_300_above DECIMAL(15,2) COMMENT 'Package revenue 300+ Yuan',
    
    -- Timestamps
    op_month INT COMMENT 'Operation month',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Created time',
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Updated time',
    
    -- Indexes
    INDEX idx_city_month (city_name, op_month),
    INDEX idx_op_month (op_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Global Tongyi Quality Metrics Table';

-- Field mapping reference:
/*
Column Order from Header:
1. 地市 (City) -> city_name
2. 出账客户户数 (Total billing customers) -> total_customers
3. 通信客户户数 (Communication customers) -> active_customers
4. 手机上网客户户数 (Mobile internet customers) -> mobile_internet_customers
5. 5G终端客户户数 (5G terminal customers) -> g5_terminal_customers
6. 5G网络客户户数 (5G network customers) -> g5_network_customers
7. 流量超出客户户数 (Traffic exceed customers) -> traffic_exceed_customers
8. 流量超出客户户数超 (Traffic exceed count) -> traffic_exceed_count
9. 语音客户户数 (Voice customers) -> voice_customers
10. 语音客户户数超 (Voice exceed customers) -> voice_exceed_customers
11. 拍照全球通客户户数 (Photo Global customers) -> photo_global_customers
12. 拍照全球通客户超出户数 (Photo Global exceed) -> photo_global_exceed
13. 拍照全球通转入户数 (Photo Global transfer in) -> photo_global_transfer_in
14. 拍照全球通转出户数 (Photo Global transfer out) -> photo_global_transfer_out
15. 拍照全球通收入-元 (Photo Global revenue) -> photo_global_revenue
16. 渗透率% (Penetration rate) -> penetration_rate
17. 流量客户占比% (Traffic customers ratio) -> traffic_customers_ratio
18. 10088接装客户数 (10088 installation customers) -> iot_customers
19. 合约客户数 (Contract customers) -> contract_customers
20. 合约(含套餐)占比% (Contract ratio) -> contract_ratio
21. 套餐客户数 (Package customers) -> package_customers
22. 套餐新客户数 (New package customers) -> package_new_customers
23. 套餐升级客户数 (Package upgrade customers) -> package_upgrade_customers
24. 套餐维系客户数 (Package maintenance customers) -> package_maintain_customers
25-33. 套餐实收各档位 (Package revenue tiers) -> package_revenue_xxx
*/

-- Sample data insertion (based on first row - Shenyang)
INSERT INTO global_tongyi_metrics (
    city_name, total_customers, active_customers, mobile_internet_customers,
    g5_terminal_customers, g5_network_customers, traffic_exceed_customers, traffic_exceed_count,
    voice_customers, voice_exceed_customers, photo_global_customers, photo_global_exceed,
    photo_global_transfer_in, photo_global_transfer_out, photo_global_revenue, 
    penetration_rate, traffic_customers_ratio, iot_customers, contract_customers, contract_ratio, 
    package_customers, package_new_customers, package_upgrade_customers, package_maintain_customers, 
    package_revenue_0_10, package_revenue_10_30, package_revenue_30_50, package_revenue_50_80, 
    package_revenue_80_100, package_revenue_100_150, package_revenue_150_200, 
    package_revenue_200_300, package_revenue_300_above, op_month
) VALUES (
    'Shenyang', 1318363, 1316519, 1288543, 
    1108158, 1034048, 131174, 49, 
    965200, 24, 11496, 1491,
    2377, 1.18, 1.43, 49.98, 911313,
    98535, 79558, 88.97, 8177, 60759,
    228250, 114338, 307217.0, 260109.0, 191104.0,
    166839.0, 45456.0, 5893.0, 4.3, 202507
);