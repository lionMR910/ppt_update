#!/usr/bin/env python3
"""
月份触发命令 - 简化的月份参数处理触发器
"""

import sys
from month_processor import MonthProcessor


def trigger_month_command(month_str: str):
    """
    触发月份命令处理
    
    Args:
        month_str: 月份字符串，格式为YYYYMM
    """
    print(f"🚀 触发月份命令: {month_str}")
    
    processor = MonthProcessor()
    
    # 解析月份参数
    try:
        op_month, last_op_month = processor.parse_month(month_str)
        
        print(f"✅ 当前月份参数: {op_month}")
        print(f"✅ 上个月份参数: {last_op_month}")
        
        # 返回参数供其他模块使用
        return {
            'op_month': op_month,
            'last_op_month': last_op_month,
            'success': True
        }
        
    except Exception as e:
        print(f"❌ 月份参数处理失败: {e}")
        return {
            'op_month': None,
            'last_op_month': None,
            'success': False,
            'error': str(e)
        }


def replace_sql_with_month(sql_template: str, month_str: str) -> str:
    """
    使用月份参数替换SQL模板中的变量
    
    Args:
        sql_template: SQL模板
        month_str: 月份字符串
        
    Returns:
        str: 替换后的SQL
    """
    processor = MonthProcessor()
    
    try:
        op_month, last_op_month = processor.parse_month(month_str)
        return processor.replace_sql_variables(sql_template, op_month, last_op_month)
    except Exception as e:
        print(f"❌ SQL替换失败: {e}")
        return sql_template


def trigger_with_sql_ids(month_str: str, sql_ids: list, execute: bool = False):
    """
    使用SQL ID列表触发月份命令
    
    Args:
        month_str: 月份字符串
        sql_ids: SQL ID列表
        execute: 是否执行SQL
    """
    from month_command import MonthCommand
    
    command = MonthCommand()
    return command.process_analysis_tasks_with_month(month_str, execute, sql_ids)


def main():
    """主函数 - 命令行调用"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python trigger_month.py <月份参数>")
        print("  python trigger_month.py <月份参数> <SQL模板>")
        print("  python trigger_month.py <月份参数> --sql-id <ID1> [ID2] [ID3]...")
        print("示例:")
        print("  python trigger_month.py 202507")
        print("  python trigger_month.py 202507 'SELECT * WHERE month = {op_month}'")
        print("  python trigger_month.py 202507 --sql-id 1 2 3")
        sys.exit(1)
    
    month_str = sys.argv[1]
    
    # 检查是否有SQL ID参数
    if len(sys.argv) > 2 and sys.argv[2] == '--sql-id':
        if len(sys.argv) < 4:
            print("❌ --sql-id 参数后需要提供至少一个ID")
            sys.exit(1)
        
        # 解析SQL ID列表
        try:
            sql_ids = [int(id_str) for id_str in sys.argv[3:]]
            print(f"🎯 处理指定SQL ID: {sql_ids}")
            
            success = trigger_with_sql_ids(month_str, sql_ids, execute=False)
            if not success:
                sys.exit(1)
        except ValueError:
            print("❌ SQL ID必须为整数")
            sys.exit(1)
    else:
        # 原有逻辑
        result = trigger_month_command(month_str)
        
        if not result['success']:
            sys.exit(1)
        
        # 如果提供了SQL模板参数
        if len(sys.argv) > 2:
            sql_template = sys.argv[2]
            processed_sql = replace_sql_with_month(sql_template, month_str)
            print(f"\n📝 处理后的SQL:")
            print(processed_sql)


if __name__ == "__main__":
    main()