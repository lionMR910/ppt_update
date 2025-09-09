#!/usr/bin/env python3
"""
PPT数据生成器 - 从数据库动态生成PPT替换内容
"""

from typing import Dict, Optional
import pymysql.cursors
from database import DatabaseManager
from analysis_data_text_order import analysis_data_text
from config import MODEL_CONFIG


class PPTDataGenerator:
    def __init__(self, use_all_tasks=False, sql_ids=None):
        """
        初始化PPT数据生成器
        
        Args:
            use_all_tasks: 是否使用所有有SQL的任务（忽略sql_flag）
            sql_ids: 指定的分析任务SQL ID列表，为空则处理所有任务
        """
        self.db_manager = DatabaseManager()
        self.api_key = MODEL_CONFIG.get('api_key', '')
        self.use_all_tasks = use_all_tasks
        self.sql_ids = sql_ids
        
    def connect_database(self) -> bool:
        """连接数据库"""
        return self.db_manager.connect()
        
    def disconnect_database(self):
        """断开数据库连接"""
        self.db_manager.disconnect()
        
    def generate_replacement_data(self) -> Dict[str, str]:
        """
        生成PPT替换数据
        
        Returns:
            Dict[str, str]: 占位符到替换内容的映射
        """
        replacement_data = {}
        
        try:
            # 获取分析任务
            if self.sql_ids:
                # 如果指定了sql_ids，只获取指定的任务
                tasks = self._get_specific_tasks(self.sql_ids)
                print(f"🎯 处理指定任务: {self.sql_ids}")
            elif self.use_all_tasks:
                tasks = self._get_all_valid_tasks()
            else:
                tasks = self.db_manager.get_analysis_tasks()
            
            if not tasks:
                print("⚠️ 没有找到可用的分析任务")
                return {}
                
            print(f"📋 找到 {len(tasks)} 个分析任务")
            
            # 处理每个任务
            for task in tasks:
                task_id = task['anaylsis_sql_id']
                task_name = task['anaylsis_name']
                sql = task['anaylsis_sql_test']
                
                print(f"\n🔄 处理任务 {task_id}: {task_name}")
                
                if not sql or not sql.strip():
                    print(f"⚠️ 任务 {task_id} 的SQL为空，跳过")
                    continue
                
                # 执行SQL获取数据
                print("📊 执行SQL查询...")
                data_df = self.db_manager.execute_analysis_sql(sql)
                
                if data_df is None or data_df.empty:
                    print(f"❌ 任务 {task_id} 数据获取失败，跳过")
                    continue
                
                # 格式化数据用于分析
                chart_data = self.db_manager.format_data_for_analysis(data_df)
                
                # 生成用户输入问题（基于任务名称）
                user_input = f"请分析{task_name}的数据情况"
                
                # 调用AI分析
                print("🤖 正在进行AI分析...")
                try:
                    analysis_result = analysis_data_text(
                        api_key=self.api_key,
                        user_input=user_input,
                        conversation_uid=f"ppt_task_{task_id}",
                        chart_obj=chart_data
                    )
                    
                    if analysis_result:
                        # 清理分析结果，移除思考过程
                        cleaned_result = self._clean_analysis_result(analysis_result)
                        
                        # 根据task_id确定对应的占位符
                        placeholder_key = f"{{{{analysis_text{task_id}}}}}"
                        replacement_data[placeholder_key] = cleaned_result
                        
                        print(f"✅ 任务 {task_id} 分析完成")
                        print(f"📝 生成内容长度: {len(cleaned_result)} 字符")
                        
                        # 注意：数据库表中没有anaylsis_text列，暂时不保存到数据库
                    else:
                        print(f"❌ 任务 {task_id} AI分析失败")
                        
                except Exception as e:
                    print(f"❌ 任务 {task_id} 分析出错: {e}")
                    continue
            
            print(f"\n📊 数据生成完成，共生成 {len(replacement_data)} 项替换内容")
            print(f"📋 替换项: {list(replacement_data.keys())}")
            
            return replacement_data
            
        except Exception as e:
            print(f"❌ 生成替换数据时出错: {e}")
            return {}
    
    def get_analysis_preview(self, task_id: int) -> Optional[str]:
        """
        获取指定任务的分析预览（用于调试）
        
        Args:
            task_id: 任务ID
            
        Returns:
            str: 分析结果预览
        """
        try:
            tasks = self.db_manager.get_analysis_tasks()
            target_task = None
            
            for task in tasks:
                if task['anaylsis_sql_id'] == task_id:
                    target_task = task
                    break
            
            if not target_task:
                return f"未找到任务ID为 {task_id} 的任务"
            
            sql = target_task['anaylsis_sql_test']
            if not sql:
                return f"任务 {task_id} 的SQL为空"
            
            # 执行SQL
            data_df = self.db_manager.execute_analysis_sql(sql)
            if data_df is None:
                return f"任务 {task_id} SQL执行失败"
            
            # 返回数据预览
            preview = f"""任务 {task_id} 数据预览:
任务名称: {target_task['anaylsis_name']}
数据行数: {len(data_df)}
数据列数: {len(data_df.columns)}
数据列名: {', '.join(data_df.columns.tolist())}

前5行数据:
{data_df.head().to_string()}"""
            
            return preview
            
        except Exception as e:
            return f"获取预览失败: {e}"
    
    def _get_all_valid_tasks(self):
        """获取所有有有效SQL的任务（忽略sql_flag）"""
        try:
            sql = """
            SELECT anaylsis_sql_id, anaylsis_id, anaylsis_name, 
                   anaylsis_lev1_name, anaylsis_lev2_name, 
                   anaylsis_sql_test, op_month
            FROM anaylsis_deploy_ppt_def 
            WHERE anaylsis_sql_test IS NOT NULL 
              AND anaylsis_sql_test != ''
              AND TRIM(anaylsis_sql_test) != ''
            ORDER BY anaylsis_sql_id
            """
            
            with self.db_manager.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                tasks = cursor.fetchall()
                
            print(f"✓ 获取到 {len(tasks)} 个有效任务（忽略sql_flag）")
            return tasks
            
        except Exception as e:
            print(f"❌ 获取所有有效任务失败: {e}")
            return []
    
    def _get_specific_tasks(self, sql_ids: list):
        """获取指定SQL ID的任务"""
        try:
            if not sql_ids:
                return []
                
            placeholders = ','.join(['%s'] * len(sql_ids))
            sql = f"""
            SELECT anaylsis_sql_id, anaylsis_id, anaylsis_name, 
                   anaylsis_lev1_name, anaylsis_lev2_name, 
                   anaylsis_sql_test, op_month
            FROM anaylsis_deploy_ppt_def 
            WHERE anaylsis_sql_id IN ({placeholders})
              AND anaylsis_sql_test IS NOT NULL 
              AND anaylsis_sql_test != ''
              AND TRIM(anaylsis_sql_test) != ''
            ORDER BY anaylsis_sql_id
            """
            
            with self.db_manager.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, sql_ids)
                tasks = cursor.fetchall()
                
            print(f"✓ 获取到 {len(tasks)} 个指定任务 (IDs: {sql_ids})")
            return tasks
            
        except Exception as e:
            print(f"❌ 获取指定任务失败: {e}")
            return []
    
    def _clean_analysis_result(self, result: str) -> str:
        """
        清理AI分析结果，移除思考过程和不需要的标签
        
        Args:
            result: 原始分析结果
            
        Returns:
            str: 清理后的分析结果
        """
        import re
        
        # 移除<think>...</think>标签及其内容
        cleaned = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL)
        
        # 移除多余的空行
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
        
        # 去除首尾空白
        cleaned = cleaned.strip()
        
        return cleaned


def main():
    """测试函数"""
    generator = PPTDataGenerator(use_all_tasks=True)
    
    if not generator.connect_database():
        print("❌ 数据库连接失败")
        return
    
    try:
        # 生成替换数据
        replacement_data = generator.generate_replacement_data()
        
        print(f"\n🎯 最终生成的替换数据:")
        for key, value in replacement_data.items():
            print(f"{key}: {value[:100]}..." if len(value) > 100 else f"{key}: {value}")
            
    finally:
        generator.disconnect_database()


if __name__ == "__main__":
    main()