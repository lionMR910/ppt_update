#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据库初始化脚本

创建测试数据库和示例数据，用于KPI替换功能的测试
"""

import sqlite3
import os
import logging
from datetime import datetime


def create_test_database(db_path: str = "data/test.db"):
    """
    创建测试数据库和表结构
    
    Args:
        db_path: 数据库文件路径
    """
    logger = logging.getLogger(__name__)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        # 连接数据库
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # 创建表结构
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS anaylsis_deploy_ppt_def (
            anaylsis_sql_id INTEGER PRIMARY KEY,
            anaylsis_id INTEGER,
            anaylsis_name TEXT,
            anaylsis_lev1_name TEXT,
            anaylsis_lev2_name TEXT,
            anaylsis_sql_test TEXT,
            top_sql_test TEXT,
            op_month TEXT,
            sql_flag INTEGER
        )
        """
        
        cursor.execute(create_table_sql)
        
        # 插入示例数据
        sample_data = [
            (
                1,  # anaylsis_sql_id
                1,  # anaylsis_id
                "全球通\"量质构效\"分析",  # anaylsis_name
                "量（1/8）",  # anaylsis_lev1_name
                "全球通客户收入情况",  # anaylsis_lev2_name
                """SELECT 
  a.city_name AS '地市',
  a.qqt_amt AS '本月全球通客户收入(万元)',
  a.pzqqt_amt AS '本月拍照全球通客户收入(万元)',
  b.qqt_amt AS '上月全球通客户收入(万元)',
  b.pzqqt_amt AS '上月拍照全球通客户收入(万元)',
  (a.qqt_amt - b.qqt_amt) AS '全球通客户收入变化(万元)'
FROM anaylsis_qqt_lzgx_st_mm a, anaylsis_qqt_lzgx_st_mm b
WHERE a.op_month = {op_month} AND b.op_month = {last_op_month}""",  # anaylsis_sql_test
                """SELECT 
       5.8 as '全球通客户收入(亿元)',
       -101 as '较上月减少(万元)',
       5.5 as '拍照全球通客户收入(亿元)',
       -112 as '拍照较上月减少(万元)'""",  # top_sql_test
                "",  # op_month
                1   # sql_flag
            ),
            (
                2,  # anaylsis_sql_id
                1,  # anaylsis_id
                "全球通\"量质构效\"分析",  # anaylsis_name
                "量（2/8）",  # anaylsis_lev1_name
                "全球通客户分等级情况",  # anaylsis_lev2_name
                """SELECT
  city_name AS '地市',
  qqt_user_pka AS '全球通普卡客户数',
  qqt_user_yka AS '全球通银卡客户数', 
  qqt_user_jka AS '全球通金卡客户数',
  qqt_user_bjka AS '全球通白金卡客户数',
  qqt_user_zska AS '全球通钻石卡客户数'
FROM anaylsis_qqt_lzgx_st_mm
WHERE op_month = {op_month}""",  # anaylsis_sql_test
                """SELECT 
       156.7 as '全球通客户数(万户)',
       23.4 as '白金及以上客户(万户)',
       15.0 as '客户占比(%)',
       8.9 as '较上月增长(万户)'""",  # top_sql_test
                "",  # op_month
                1   # sql_flag
            ),
            (
                3,  # anaylsis_sql_id
                2,  # anaylsis_id
                "市场份额分析",  # anaylsis_name
                "份额（1/5）",  # anaylsis_lev1_name
                "移动用户市场份额",  # anaylsis_lev2_name
                """SELECT
  city_name AS '地市',
  mobile_users AS '移动用户数',
  market_share AS '市场份额'
FROM market_share_analysis
WHERE op_month = {op_month}""",  # anaylsis_sql_test
                """SELECT 
       892.5 as '移动用户数(万户)',
       45.6 as '市场份额(%)',
       2.1 as '较上月增长(%)',
       18.7 as '新增用户(万户)'""",  # top_sql_test
                "",  # op_month
                1   # sql_flag
            )
        ]
        
        # 清空现有数据
        cursor.execute("DELETE FROM anaylsis_deploy_ppt_def")
        
        # 插入示例数据
        insert_sql = """
        INSERT INTO anaylsis_deploy_ppt_def 
        (anaylsis_sql_id, anaylsis_id, anaylsis_name, anaylsis_lev1_name, 
         anaylsis_lev2_name, anaylsis_sql_test, top_sql_test, op_month, sql_flag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.executemany(insert_sql, sample_data)
        
        # 提交事务
        connection.commit()
        
        logger.info(f"测试数据库创建成功: {db_path}")
        logger.info(f"插入了 {len(sample_data)} 条示例数据")
        
        # 验证数据
        cursor.execute("SELECT COUNT(*) FROM anaylsis_deploy_ppt_def")
        count = cursor.fetchone()[0]
        logger.info(f"数据库中共有 {count} 条记录")
        
        return True
        
    except Exception as e:
        logger.error(f"创建测试数据库失败: {e}")
        return False
        
    finally:
        if connection:
            connection.close()


def verify_database(db_path: str = "data/test.db"):
    """
    验证数据库内容
    
    Args:
        db_path: 数据库文件路径
    """
    logger = logging.getLogger(__name__)
    
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # 查询所有数据
        cursor.execute("SELECT * FROM anaylsis_deploy_ppt_def ORDER BY anaylsis_sql_id")
        rows = cursor.fetchall()
        
        logger.info("数据库内容验证:")
        for row in rows:
            logger.info(f"ID: {row[0]}, 名称: {row[2]}, 等级: {row[3]}")
        
        return True
        
    except Exception as e:
        logger.error(f"数据库验证失败: {e}")
        return False
        
    finally:
        if connection:
            connection.close()


def create_sample_kpi_ppt():
    """
    创建包含KPI占位符的示例PPT文本内容
    """
    sample_content = """
# 全球通客户分析报告

## 收入分析
本月全球通客户收入为 {{kpi_1_1}} 亿元，较上月减少 {{kpi_1_2}} 万元。
拍照全球通客户收入为 {{kpi_1_3}} 亿元，较上月减少 {{kpi_1_4}} 万元。

## 客户规模分析  
全球通客户数为 {{kpi_2_1}} 万户，白金及以上客户为 {{kpi_2_2}} 万户。
客户占比为 {{kpi_2_3}}%，较上月增长 {{kpi_2_4}} 万户。

## 市场份额分析
移动用户数为 {{kpi_3_1}} 万户，市场份额为 {{kpi_3_2}}%。
较上月增长 {{kpi_3_3}}%，新增用户 {{kpi_3_4}} 万户。
    """
    
    logger = logging.getLogger(__name__)
    
    # 保存示例内容到文件
    os.makedirs("file", exist_ok=True)
    with open("file/sample_kpi_content.txt", "w", encoding="utf-8") as f:
        f.write(sample_content)
    
    logger.info("示例KPI内容已保存到 file/sample_kpi_content.txt")
    print("示例KPI内容:")
    print(sample_content)


def main():
    """主函数"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    print("🚀 初始化测试数据库...")
    
    # 1. 创建测试数据库
    if create_test_database():
        print("✅ 测试数据库创建成功")
    else:
        print("❌ 测试数据库创建失败")
        return
    
    # 2. 验证数据库
    if verify_database():
        print("✅ 数据库验证通过")
    else:
        print("❌ 数据库验证失败")
        return
    
    # 3. 创建示例KPI内容
    create_sample_kpi_ppt()
    print("✅ 示例内容创建完成")
    
    print("\n🎉 初始化完成！现在可以测试KPI替换功能了")
    print("\n测试命令示例:")
    print("python src/kpi_ppt_command.py -t file/ces.pptx -m 202507 -v")


if __name__ == "__main__":
    main()