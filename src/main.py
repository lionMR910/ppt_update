#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析自动化程序
主程序入口
"""

import sys
import time
from datetime import datetime
from database import DatabaseManager
from ai_analyzer import AIAnalyzer


def print_header():
    """打印程序头信息"""
    print("=" * 60)
    print("数据分析自动化程序")
    print("版本: 1.0")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


def main():
    """主函数"""
    print_header()
    
    # 初始化组件
    db_manager = DatabaseManager()
    ai_analyzer = AIAnalyzer()
    
    try:
        # 1. 连接数据库
        print("\n🔗 正在连接数据库...")
        if not db_manager.connect():
            print("❌ 数据库连接失败，程序退出")
            return False
        
        # 2. 测试AI服务
        print("\n🤖 正在测试AI服务...")
        if not ai_analyzer.test_connection():
            print("❌ AI服务连接失败，程序退出")
            return False
        
        # 3. 获取分析任务
        print("\n📋 正在获取分析任务...")
        tasks = db_manager.get_analysis_tasks()
        
        if not tasks:
            print("ℹ️ 没有待分析的任务")
            return True
        
        # 4. 执行分析任务
        print(f"\n🚀 开始执行 {len(tasks)} 个分析任务...")
        
        success_count = 0
        failed_count = 0
        
        for i, task in enumerate(tasks, 1):
            print(f"\n--- 任务 {i}/{len(tasks)} ---")
            print(f"任务ID: {task['anaylsis_sql_id']}")
            print(f"任务名称: {task['anaylsis_name']}")
            print(f"分析月份: {task['op_month']}")
            
            try:
                # 执行SQL查询
                print("📊 执行SQL查询...")
                sql = task['anaylsis_sql_test']
                if not sql or not sql.strip():
                    print("⚠️ SQL语句为空，跳过此任务")
                    failed_count += 1
                    continue
                
                data_df = db_manager.execute_analysis_sql(sql)
                if data_df is None:
                    print("❌ SQL执行失败，跳过此任务")
                    failed_count += 1
                    continue
                
                # 格式化数据
                data_content = db_manager.format_data_for_analysis(data_df)
                
                # AI分析
                analysis_result = ai_analyzer.analyze_data(task, data_content)
                if not analysis_result:
                    print("❌ AI分析失败，跳过此任务")
                    failed_count += 1
                    continue
                
                # 更新分析结论
                print("💾 更新分析结论...")
                if db_manager.update_analysis_result(task['anaylsis_sql_id'], analysis_result):
                    print("✅ 任务完成")
                    success_count += 1
                else:
                    print("❌ 结论更新失败")
                    failed_count += 1
                
            except Exception as e:
                print(f"❌ 任务执行出错: {e}")
                failed_count += 1
                continue
        
        # 5. 输出执行结果
        print("\n" + "=" * 60)
        print("📊 执行结果统计:")
        print(f"总任务数: {len(tasks)}")
        print(f"成功: {success_count}")
        print(f"失败: {failed_count}")
        print(f"成功率: {success_count/len(tasks)*100:.1f}%")
        
        if success_count > 0:
            print("🎉 有任务执行成功！")
        
        return success_count > 0
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断程序执行")
        return False
        
    except Exception as e:
        print(f"\n❌ 程序执行异常: {e}")
        return False
        
    finally:
        # 清理资源
        print("\n🧹 清理资源...")
        db_manager.disconnect()
        print(f"程序结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(1)