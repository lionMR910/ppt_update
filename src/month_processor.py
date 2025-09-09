#!/usr/bin/env python3
"""
月份参数处理器 - 处理月份参数和SQL变量替换
"""

import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class MonthProcessor:
    def __init__(self):
        """初始化月份处理器"""
        pass
    
    def parse_month(self, month_str: str) -> tuple:
        """
        解析月份字符串并计算上个月
        
        Args:
            month_str: 月份字符串，格式为YYYYMM，如202507
            
        Returns:
            tuple: (当前月份, 上个月份)
        """
        try:
            # 验证格式
            if not month_str.isdigit() or len(month_str) != 6:
                raise ValueError(f"月份格式错误，应为YYYYMM格式，实际: {month_str}")
            
            year = int(month_str[:4])
            month = int(month_str[4:])
            
            # 验证月份范围
            if month < 1 or month > 12:
                raise ValueError(f"月份应在1-12之间，实际: {month}")
            
            # 创建当前日期
            current_date = datetime(year, month, 1)
            
            # 计算上个月
            last_month_date = current_date - relativedelta(months=1)
            
            # 格式化返回
            current_month = month_str
            last_month = f"{last_month_date.year:04d}{last_month_date.month:02d}"
            
            return current_month, last_month
            
        except Exception as e:
            raise ValueError(f"解析月份失败: {e}")
    
    def replace_sql_variables(self, sql: str, op_month: str, last_op_month: str) -> str:
        """
        替换SQL中的月份变量
        
        Args:
            sql: 原始SQL语句
            op_month: 当前月份参数
            last_op_month: 上个月份参数
            
        Returns:
            str: 替换后的SQL语句
        """
        # 替换变量
        result_sql = sql.replace('{op_month}', op_month)
        result_sql = result_sql.replace('{last_op_month}', last_op_month)
        
        return result_sql
    
    def process_month_command(self, month_str: str, sql_template: str = None) -> dict:
        """
        处理月份命令的完整流程
        
        Args:
            month_str: 月份字符串
            sql_template: SQL模板（可选）
            
        Returns:
            dict: 处理结果
        """
        try:
            # 解析月份
            op_month, last_op_month = self.parse_month(month_str)
            
            result = {
                'status': 'success',
                'op_month': op_month,
                'last_op_month': last_op_month,
                'month_info': {
                    'current_year': op_month[:4],
                    'current_month': op_month[4:],
                    'last_year': last_op_month[:4],
                    'last_month': last_op_month[4:]
                }
            }
            
            # 如果提供了SQL模板，进行替换
            if sql_template:
                processed_sql = self.replace_sql_variables(sql_template, op_month, last_op_month)
                result['original_sql'] = sql_template
                result['processed_sql'] = processed_sql
            
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'op_month': None,
                'last_op_month': None
            }


def main():
    """测试函数"""
    processor = MonthProcessor()
    
    # 测试用例
    test_cases = [
        "202507",  # 正常情况
        "202501",  # 跨年情况
        "202512",  # 12月情况
        "202400",  # 错误月份
        "20250",   # 格式错误
    ]
    
    # SQL模板示例
    sql_template = """
    SELECT city_name, qqt_amt, pzqqt_amt 
    FROM anaylsis_qqt_lzgx_st_mm 
    WHERE op_month = {op_month}
      AND last_month = {last_op_month}
    ORDER BY qqt_amt DESC
    """
    
    print("=== 月份处理器测试 ===\n")
    
    for month_str in test_cases:
        print(f"测试月份: {month_str}")
        result = processor.process_month_command(month_str, sql_template)
        
        if result['status'] == 'success':
            print(f"  ✓ 当前月份: {result['op_month']}")
            print(f"  ✓ 上个月份: {result['last_op_month']}")
            print(f"  ✓ 年月信息: {result['month_info']}")
            if 'processed_sql' in result:
                print(f"  ✓ 处理后SQL:")
                print(f"    {result['processed_sql'].strip()}")
        else:
            print(f"  ✗ 错误: {result['error']}")
        
        print("-" * 50)


if __name__ == "__main__":
    main()