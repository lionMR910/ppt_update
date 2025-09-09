#!/usr/bin/env python3
"""
月份命令行工具 - 处理月份参数和执行SQL替换
"""

import argparse
import sys
import os
from month_processor import MonthProcessor
from database import DatabaseManager


class MonthCommand:
    def __init__(self):
        """初始化月份命令"""
        self.processor = MonthProcessor()
        self.db_manager = DatabaseManager()
    
    def execute_sql_with_month(self, sql_template: str, month_str: str, execute: bool = False):
        """
        使用月份参数执行SQL
        
        Args:
            sql_template: SQL模板
            month_str: 月份字符串
            execute: 是否实际执行SQL
        """
        print(f"🗓️  处理月份参数: {month_str}")
        
        # 处理月份
        result = self.processor.process_month_command(month_str, sql_template)
        
        if result['status'] != 'success':
            print(f"❌ 月份处理失败: {result['error']}")
            return False
        
        print(f"✅ 当前月份: {result['op_month']}")
        print(f"✅ 上个月份: {result['last_op_month']}")
        print("\n📝 处理后的SQL:")
        print("-" * 60)
        print(result['processed_sql'])
        print("-" * 60)
        
        if execute:
            print("\n🚀 执行SQL...")
            return self._execute_sql(result['processed_sql'])
        else:
            print("\n💡 提示: 使用 --execute 参数来实际执行SQL")
            return True
    
    def _execute_sql(self, sql: str):
        """执行SQL语句"""
        try:
            if not self.db_manager.connect():
                print("❌ 数据库连接失败")
                return False
            
            # 执行SQL
            df = self.db_manager.execute_analysis_sql(sql)
            
            if df is not None:
                print(f"✅ SQL执行成功，返回 {len(df)} 行数据")
                
                # 显示前几行数据
                if len(df) > 0:
                    print("\n📊 前5行数据预览:")
                    print(df.head().to_string())
                else:
                    print("📊 查询结果为空")
                
                return True
            else:
                print("❌ SQL执行失败")
                return False
                
        except Exception as e:
            print(f"❌ 执行SQL时出错: {e}")
            return False
        finally:
            self.db_manager.disconnect()
    
    def process_analysis_tasks_with_month(self, month_str: str, execute: bool = False, sql_ids: list = None, analysis_id: int = 1):
        """
        处理分析任务中的月份参数
        
        Args:
            month_str: 月份字符串
            execute: 是否实际执行
            sql_ids: 指定的SQL ID列表，如果为None则处理所有任务
            analysis_id: 分析配置ID，1=全球通"量质构效"分析，2=中高端"量质构效"分析
        """
        if sql_ids:
            print(f"🔄 处理指定分析任务的月份参数: {month_str}, SQL IDs: {sql_ids} (分析配置ID: {analysis_id})")
        else:
            print(f"🔄 处理所有分析任务的月份参数: {month_str} (分析配置ID: {analysis_id})")
        
        try:
            if not self.db_manager.connect():
                print("❌ 数据库连接失败")
                return False
            
            # 获取分析任务
            if sql_ids:
                tasks = self._get_specific_tasks(sql_ids, analysis_id)
            else:
                tasks = self._get_all_analysis_tasks(analysis_id)
            
            if not tasks:
                if sql_ids:
                    print(f"⚠️ 没有找到指定ID的分析任务: {sql_ids}")
                else:
                    print("⚠️ 没有找到分析任务")
                return False
            
            print(f"📋 找到 {len(tasks)} 个分析任务")
            
            # 处理每个任务
            for i, task in enumerate(tasks, 1):
                task_id = task['anaylsis_sql_id']
                task_name = task['anaylsis_name']
                sql_template = task['anaylsis_sql_test']
                
                print(f"\n--- 任务 {i}/{len(tasks)}: {task_name} (ID: {task_id}) ---")
                
                if not sql_template:
                    print("⚠️ SQL模板为空，跳过")
                    continue
                
                # 检查是否包含月份变量
                if '{op_month}' not in sql_template and '{last_op_month}' not in sql_template:
                    print("ℹ️ SQL中未找到月份变量，跳过")
                    continue
                
                # 处理月份参数
                result = self.processor.process_month_command(month_str, sql_template)
                
                if result['status'] != 'success':
                    print(f"❌ 月份处理失败: {result['error']}")
                    continue
                
                print(f"✅ 月份参数: {result['op_month']} / 上月: {result['last_op_month']}")
                print("📝 处理后的SQL:")
                print(result['processed_sql'][:200] + "..." if len(result['processed_sql']) > 200 else result['processed_sql'])
                
                if execute:
                    # 执行SQL
                    df = self.db_manager.execute_analysis_sql(result['processed_sql'])
                    if df is not None:
                        print(f"✅ 执行成功，返回 {len(df)} 行数据")
                    else:
                        print("❌ 执行失败")
            
            return True
            
        except Exception as e:
            print(f"❌ 处理分析任务时出错: {e}")
            return False
        finally:
            self.db_manager.disconnect()
    
    def _get_specific_tasks(self, sql_ids: list, analysis_id: int = 1):
        """
        获取指定ID的分析任务
        
        Args:
            sql_ids: SQL ID列表
            analysis_id: 分析配置ID
            
        Returns:
            list: 任务列表
        """
        try:
            # 构建SQL查询
            id_placeholders = ','.join(['%s'] * len(sql_ids))
            sql = f"""
            SELECT anaylsis_sql_id, anaylsis_id, anaylsis_name, 
                   anaylsis_lev1_name, anaylsis_lev2_name, 
                   anaylsis_sql_test, op_month
            FROM anaylsis_deploy_ppt_def 
            WHERE anaylsis_sql_id IN ({id_placeholders}) AND anaylsis_id = %s
            ORDER BY anaylsis_sql_id
            """
            
            import pymysql.cursors
            with self.db_manager.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, sql_ids + [analysis_id])
                tasks = cursor.fetchall()
                
            print(f"✓ 通过ID查询到 {len(tasks)} 个任务")
            return tasks
            
        except Exception as e:
            print(f"❌ 查询指定任务失败: {e}")
            return []
    
    def _get_all_analysis_tasks(self, analysis_id: int = 1):
        """
        获取所有分析任务
        
        Args:
            analysis_id: 分析配置ID
            
        Returns:
            list: 任务列表
        """
        try:
            sql = """
            SELECT anaylsis_sql_id, anaylsis_id, anaylsis_name, 
                   anaylsis_lev1_name, anaylsis_lev2_name, 
                   anaylsis_sql_test, op_month
            FROM anaylsis_deploy_ppt_def 
            WHERE anaylsis_id = %s
            ORDER BY anaylsis_sql_id
            """
            
            import pymysql.cursors
            with self.db_manager.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, (analysis_id,))
                tasks = cursor.fetchall()
                
            print(f"✓ 查询到 {len(tasks)} 个分析任务")
            return tasks
            
        except Exception as e:
            print(f"❌ 查询分析任务失败: {e}")
            return []


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='月份参数处理命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s --month 202507 --sql "SELECT * FROM table WHERE month = {op_month}"
  %(prog)s --month 202507 --tasks
  %(prog)s --month 202507 --tasks --execute
  %(prog)s --month 202507 --tasks --sql-id 5
  %(prog)s --month 202507 --tasks --sql-id 1 2 3 --execute
  %(prog)s --month 202507 --tasks --sql-id 5 -a 2
        """
    )
    
    parser.add_argument(
        '--month', '-m',
        required=True,
        help='月份参数，格式为YYYYMM，如202507'
    )
    
    parser.add_argument(
        '--sql', '-s',
        help='SQL模板，包含{op_month}和{last_op_month}变量'
    )
    
    parser.add_argument(
        '--tasks', '-t',
        action='store_true',
        help='处理数据库中的分析任务'
    )
    
    parser.add_argument(
        '--execute', '-e',
        action='store_true',
        help='实际执行SQL（默认只显示处理结果）'
    )
    
    parser.add_argument(
        '--file', '-f',
        help='从文件读取SQL模板'
    )
    
    parser.add_argument(
        '--sql-id', '--id',
        type=int,
        nargs='+',
        help='指定的分析任务SQL ID，支持单个或多个ID，如: --sql-id 1 或 --sql-id 1 2 3'
    )
    
    parser.add_argument(
        '--analysis-id', '-a',
        type=int,
        default=1,
        help='分析配置ID，1=全球通"量质构效"分析，2=中高端"量质构效"分析 (默认: 1)'
    )
    
    args = parser.parse_args()
    
    # 创建命令处理器
    command = MonthCommand()
    
    print("🗓️ 月份参数处理工具")
    print("=" * 50)
    
    try:
        if args.tasks:
            # 处理分析任务
            success = command.process_analysis_tasks_with_month(args.month, args.execute, args.sql_id, args.analysis_id)
        elif args.sql:
            # 处理单个SQL
            success = command.execute_sql_with_month(args.sql, args.month, args.execute)
        elif args.file:
            # 从文件读取SQL
            if not os.path.exists(args.file):
                print(f"❌ 文件不存在: {args.file}")
                sys.exit(1)
            
            with open(args.file, 'r', encoding='utf-8') as f:
                sql_template = f.read()
            
            success = command.execute_sql_with_month(sql_template, args.month, args.execute)
        else:
            # 只处理月份参数
            processor = MonthProcessor()
            result = processor.process_month_command(args.month)
            
            if result['status'] == 'success':
                print(f"✅ 当前月份: {result['op_month']}")
                print(f"✅ 上个月份: {result['last_op_month']}")
                print(f"📊 月份信息: {result['month_info']}")
                success = True
            else:
                print(f"❌ 处理失败: {result['error']}")
                success = False
        
        if success:
            print("\n🎉 处理完成！")
        else:
            print("\n💥 处理失败！")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()