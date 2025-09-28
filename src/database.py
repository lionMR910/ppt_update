# 数据库操作模块

import pymysql
import pandas as pd
from typing import List, Dict, Any, Optional
from config import DB_CONFIG, SQL_TIMEOUT


class DatabaseManager:
    def __init__(self):
        self.connection = None
        
    def connect(self) -> bool:
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database'],
                charset=DB_CONFIG['charset'],
                autocommit=False
            )
            print("✓ 数据库连接成功")
            return True
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            print("✓ 数据库连接已关闭")
    
    def get_analysis_tasks(self) -> List[Dict[str, Any]]:
        """获取待分析的任务列表"""
        try:
            sql = """
            SELECT anaylsis_sql_id, anaylsis_id, anaylsis_name, 
                   anaylsis_lev1_name, anaylsis_lev2_name, 
                   anaylsis_sql_test, op_month
            FROM anaylsis_deploy_ppt_def 
            WHERE sql_flag = 1 
            ORDER BY anaylsis_sql_id
            """
            
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                tasks = cursor.fetchall()
                
            print(f"✓ 获取到 {len(tasks)} 个待分析任务")
            return tasks
            
        except Exception as e:
            print(f"❌ 获取分析任务失败: {e}")
            return []
    
    def execute_analysis_sql(self, sql: str) -> Optional[pd.DataFrame]:
        """执行分析SQL并返回结果"""
        try:
            # 安全检查：只允许SELECT查询
            if not sql.upper().strip().startswith('SELECT'):
                raise ValueError("只允许执行SELECT查询")
            
            # 清理SQL语句：移除末尾的分号和多余空白字符
            sql = sql.rstrip().rstrip(';').rstrip()
            
            # 执行查询（使用警告抑制）
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df = pd.read_sql(sql, self.connection)
            print(f"✓ SQL执行成功，返回 {len(df)} 行数据")
            return df
            
        except Exception as e:
            print(f"❌ SQL执行失败: {e}")
            return None
    
    def update_analysis_result(self, task_id: int, analysis_text: str) -> bool:
        """更新分析结论"""
        try:
            sql = """
            UPDATE anaylsis_deploy_ppt_def 
            SET anaylsis_text = %s 
            WHERE anaylsis_sql_id = %s
            """
            
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (analysis_text, task_id))
                self.connection.commit()
                
            print(f"✓ 任务 {task_id} 分析结论更新成功")
            return True
            
        except Exception as e:
            print(f"❌ 更新分析结论失败: {e}")
            self.connection.rollback()
            return False
    
    def format_data_for_analysis(self, df: pd.DataFrame) -> str:
        """格式化数据用于AI分析，输出制表符分隔的表格格式"""
        if df is None or df.empty:
            return "无数据"
        
        # 限制显示的行数和列数，适应analysis_data_text函数的需求
        max_rows = min(50, len(df))
        max_cols = min(10, len(df.columns))
        
        # 截取数据
        display_df = df.iloc[:max_rows, :max_cols]
        
        # 生成制表符分隔的表格格式
        formatted_lines = []
        
        # 添加表头
        headers = display_df.columns.tolist()
        formatted_lines.append('\t'.join(headers))
        
        # 添加数据行
        for _, row in display_df.iterrows():
            # 格式化每一行的数据
            formatted_row = []
            for col in headers:
                value = row[col]
                if pd.isna(value):
                    formatted_row.append('')
                elif isinstance(value, (int, float)):
                    # 数值类型保留适当的精度
                    if isinstance(value, float) and value != int(value):
                        formatted_row.append(f"{value:.2f}")
                    else:
                        formatted_row.append(str(int(value)))
                else:
                    formatted_row.append(str(value))
            formatted_lines.append('\t'.join(formatted_row))
        
        # 组合成最终格式
        table_content = '\n'.join(formatted_lines)
        
        # 添加简单的数据描述
        result = f"""数据分析表格

{table_content}

数据说明：共{len(df)}行数据，{len(df.columns)}个指标"""
        
        return result