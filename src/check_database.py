#!/usr/bin/env python3
"""
检查数据库中的分析任务数据
"""

from database import DatabaseManager
import pymysql.cursors


def check_database():
    db_manager = DatabaseManager()
    
    if not db_manager.connect():
        print("❌ 数据库连接失败")
        return
    
    try:
        print("🔍 检查数据库中的分析任务...")
        
        # 检查表结构
        sql = "DESCRIBE anaylsis_deploy_ppt_def"
        with db_manager.connection.cursor() as cursor:
            cursor.execute(sql)
            columns = cursor.fetchall()
            print(f"\n📋 表结构:")
            for col in columns:
                print(f"  {col}")
        
        # 检查所有记录
        sql = "SELECT anaylsis_sql_id, anaylsis_name, sql_flag, anaylsis_sql_test FROM anaylsis_deploy_ppt_def LIMIT 10"
        with db_manager.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            all_records = cursor.fetchall()
            
            print(f"\n📊 前10条记录:")
            for record in all_records:
                print(f"  ID: {record['anaylsis_sql_id']}, 名称: {record['anaylsis_name']}, sql_flag: {record['sql_flag']}")
                print(f"      SQL: {record['anaylsis_sql_test'][:100] if record['anaylsis_sql_test'] else 'NULL'}...")
                print()
        
        # 检查有sql_flag=1的记录
        sql = "SELECT COUNT(*) as count FROM anaylsis_deploy_ppt_def WHERE sql_flag = 1"
        with db_manager.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            print(f"🎯 sql_flag=1的记录数: {result['count']}")
            
        # 检查非空SQL的记录
        sql = "SELECT COUNT(*) as count FROM anaylsis_deploy_ppt_def WHERE anaylsis_sql_test IS NOT NULL AND anaylsis_sql_test != ''"
        with db_manager.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            print(f"📝 有非空SQL的记录数: {result['count']}")
        
        # 如果没有sql_flag=1的记录，检查是否有其他flag值
        sql = "SELECT sql_flag, COUNT(*) as count FROM anaylsis_deploy_ppt_def GROUP BY sql_flag"
        with db_manager.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            flag_counts = cursor.fetchall()
            print(f"\n🏷️ sql_flag值分布:")
            for row in flag_counts:
                print(f"  sql_flag={row['sql_flag']}: {row['count']}条记录")
                
    except Exception as e:
        print(f"❌ 检查数据库时出错: {e}")
    finally:
        db_manager.disconnect()


if __name__ == "__main__":
    check_database()