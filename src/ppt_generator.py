#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT报告生成器
整合数据处理和PPT生成的完整流程
"""

import argparse
import logging
import sys
import time
from pathlib import Path
import pymysql

from month_processor import MonthProcessor
from database import DatabaseManager
from ai_analyzer import AIAnalyzer
from config import MODEL_CONFIG
from ppt_processor import PPTProcessor
from config import DB_CONFIG

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PPTReportGenerator:
    """PPT报告生成器"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.month_processor = MonthProcessor()
        self.ai_analyzer = AIAnalyzer()  # 使用新的AI分析器（包含验证功能）
        self.replacement_data = {}
        
    def generate_report(self, template_file: str, output_file: str, month_str: str, sql_ids: list = None, analysis_id: int = 1, execute_sql: bool = False):
        """
        生成PPT报告
        
        Args:
            template_file: PPT模板文件路径
            output_file: 输出PPT文件路径
            month_str: 月份参数，格式为YYYYMM
            sql_ids: 指定的SQL ID列表，为空则处理所有任务
            analysis_id: 分析配置ID，1=全球通"量质构效"分析，2=中高端"量质构效"分析
            execute_sql: 是否实际执行SQL
        """
        try:
            logger.info(f"🚀 开始生成PPT报告: {output_file}")
            logger.info(f"📅 处理月份: {month_str}")
            
            # 1. 处理月份参数
            op_month, last_op_month = self.month_processor.parse_month(month_str)
            logger.info(f"✅ 月份参数: {op_month} / 上月: {last_op_month}")
            
            # 2. 连接数据库
            logger.info("🔗 连接数据库...")
            self.db_manager.connect()
            
            # 3. 获取分析任务
            if sql_ids:
                logger.info(f"🎯 获取指定任务: {sql_ids} (分析配置ID: {analysis_id})")
                tasks = self._get_specific_tasks(sql_ids, analysis_id)
            else:
                logger.info(f"📋 获取所有有效任务 (分析配置ID: {analysis_id})...")
                tasks = self._get_all_valid_tasks(analysis_id)
            
            logger.info(f"📊 找到 {len(tasks)} 个分析任务")
            
            # 4. 处理每个任务并生成分析内容
            self.replacement_data = {}
            for i, task in enumerate(tasks, 1):
                task_id = task['anaylsis_sql_id']
                task_name = task['anaylsis_name']
                sql_template = task['anaylsis_sql_test']
                
                logger.info(f"--- 处理任务 {i}/{len(tasks)}: {task_name} (ID: {task_id}) ---")
                
                if not sql_template or sql_template.strip().upper() == 'NULL':
                    logger.warning(f"⚠️ 任务 {task_id} 的SQL为空，跳过")
                    continue
                
                # 替换SQL中的月份变量
                processed_sql = self.month_processor.replace_sql_variables(
                    sql_template, op_month, last_op_month
                )
                
                # 如果是执行SQL模式，显示SQL并执行
                if execute_sql:
                    logger.info(f"📝 处理后的SQL:")
                    logger.info("-" * 60)
                    logger.info(processed_sql)
                    logger.info("-" * 60)
                    
                    # 执行SQL并显示结果
                    success = self._execute_sql(processed_sql)
                    if not success:
                        logger.warning(f"⚠️ 任务 {task_id} SQL执行失败")
                    continue
                
                # 执行SQL获取数据
                logger.info(f"📝 执行SQL查询...")
                try:
                    data = self.db_manager.execute_analysis_sql(processed_sql)
                    if data.empty:
                        logger.warning(f"⚠️ 任务 {task_id} 查询结果为空")
                        continue
                    
                    # 格式化数据用于AI分析
                    formatted_data = self.db_manager.format_data_for_analysis(data)
                    
                    # 调用AI分析（使用新的分析器，包含验证功能）
                    logger.info(f"🤖 AI分析中...")
                    
                    # 调试：打印输入数据和排序结果
                    logger.info(f"📊 调试信息 - 任务ID: {task_id}")
                    logger.info(f"📊 输入数据格式: {type(formatted_data)}")
                    if isinstance(formatted_data, str):
                        logger.info(f"📊 输入数据长度: {len(formatted_data)} 字符")
                        logger.info(f"📊 输入数据预览: {formatted_data[:200]}...")
                    else:
                        logger.info(f"📊 输入数据: {formatted_data}")
                    
                    # 获取排序结果用于调试
                    from analysis_data_text_order import parse_and_sort_data
                    sort_results = parse_and_sort_data(formatted_data)
                    logger.info(f"📊 排序结果调试:")
                    logger.info("=" * 60)
                    logger.info(f"{sort_results}")
                    logger.info("=" * 60)
                    
                    # 构建任务信息
                    task_info = {
                        'anaylsis_sql_id': task_id,
                        'anaylsis_name': task_name,
                        'op_month': op_month
                    }
                    
                    # 使用新的AI分析器（自动包含验证和修正功能）
                    analysis_result = self.ai_analyzer.analyze_data(task_info, formatted_data)
                    
                    # 清理分析结果
                    cleaned_result = self._clean_analysis_result(analysis_result)
                    
                    # 存储到替换数据中
                    placeholder = f"{{{{analysis_text{task_id}}}}}"
                    self.replacement_data[placeholder] = cleaned_result
                    
                    logger.info(f"✅ 任务 {task_id} 分析完成")
                    logger.info(f"📄 生成内容长度: {len(cleaned_result)} 字符")
                    
                except Exception as e:
                    logger.error(f"❌ 任务 {task_id} 处理失败: {str(e)}")
                    continue
            
            # 5. 关闭数据库连接
            if self.db_manager.connection:
                self.db_manager.disconnect()
            
            # 6. 如果是执行SQL模式，跳过PPT生成
            if execute_sql:
                logger.info("✅ SQL执行模式完成，未生成PPT")
                return True
            
            # 7. 生成PPT报告
            logger.info(f"📑 生成PPT报告...")
            logger.info(f"📂 模板文件: {template_file}")
            logger.info(f"💾 输出文件: {output_file}")
            logger.info(f"🔄 替换数据项: {len(self.replacement_data)} 个")
            
            # 创建PPT处理器并设置替换数据
            ppt_processor = PPTProcessor(template_file, sql_ids)
            ppt_processor.replacement_data = self.replacement_data
            
            # 处理PPT
            result = ppt_processor.process(output_file)
            
            if result:  # process返回bool值
                logger.info(f"🎉 PPT报告生成成功!")
                logger.info(f"📁 文件保存至: {output_file}")
            else:
                logger.error(f"❌ PPT生成失败")
                return False
                
            return True
            
        except Exception as e:
            import traceback
            logger.error(f"❌ 报告生成失败: {str(e)}")
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            try:
                if hasattr(self, 'db_manager') and self.db_manager.connection:
                    self.db_manager.disconnect()
            except:
                pass  # 忽略重复关闭错误
            return False
    
    def _get_all_valid_tasks(self, analysis_id: int = 1):
        """获取所有有效的分析任务（有非空SQL的任务）"""
        try:
            cursor = self.db_manager.connection.cursor(pymysql.cursors.DictCursor)
            query = """
            SELECT anaylsis_sql_id, anaylsis_name, anaylsis_sql_test, op_month
            FROM anaylsis_deploy_ppt_def
            WHERE anaylsis_sql_test IS NOT NULL 
              AND anaylsis_sql_test != '' 
              AND UPPER(anaylsis_sql_test) != 'NULL'
              AND anaylsis_id = %s
            ORDER BY anaylsis_sql_id
            """
            cursor.execute(query, (analysis_id,))
            
            tasks = cursor.fetchall()
            cursor.close()
            return tasks
            
        except Exception as e:
            logger.error(f"获取分析任务失败: {str(e)}")
            return []
    
    def _get_specific_tasks(self, sql_ids: list, analysis_id: int = 1):
        """根据SQL ID获取指定的分析任务"""
        try:
            cursor = self.db_manager.connection.cursor(pymysql.cursors.DictCursor)
            placeholders = ','.join(['%s'] * len(sql_ids))
            query = f"""
            SELECT anaylsis_sql_id, anaylsis_name, anaylsis_sql_test, op_month
            FROM anaylsis_deploy_ppt_def
            WHERE anaylsis_sql_id IN ({placeholders})
              AND anaylsis_id = %s
            ORDER BY anaylsis_sql_id
            """
            cursor.execute(query, sql_ids + [analysis_id])
            
            tasks = cursor.fetchall()
            cursor.close()
            return tasks
            
        except Exception as e:
            logger.error(f"获取指定分析任务失败: {str(e)}")
            return []
    
    def process_sql_template(self, sql_template: str, month_str: str, execute: bool = False):
        """
        处理SQL模板，执行月份参数替换
        
        Args:
            sql_template: SQL模板
            month_str: 月份字符串
            execute: 是否实际执行SQL
            
        Returns:
            处理是否成功
        """
        try:
            logger.info(f"🗓️ 处理SQL模板，月份参数: {month_str}")
            logger.info(f"📝 原始SQL模板:")
            logger.info(sql_template[:200] + "..." if len(sql_template) > 200 else sql_template)
            
            # 连接数据库
            logger.info("🔗 连接数据库...")
            self.db_manager.connect()
            
            # 处理月份参数
            result = self.month_processor.process_month_command(month_str, sql_template)
            
            if result['status'] != 'success':
                logger.error(f"❌ 月份处理失败: {result['error']}")
                return False
            
            logger.info(f"✅ 当前月份: {result['op_month']}")
            logger.info(f"✅ 上个月份: {result['last_op_month']}")
            logger.info("\n📝 处理后的SQL:")
            logger.info("-" * 60)
            logger.info(result['processed_sql'])
            logger.info("-" * 60)
            
            if execute:
                logger.info("\n🚀 执行SQL...")
                return self._execute_sql(result['processed_sql'])
            else:
                logger.info("\n💡 提示: 使用 --execute 参数来实际执行SQL")
                return True
                
        except Exception as e:
            logger.error(f"❌ 处理SQL模板时出错: {str(e)}")
            return False
        finally:
            try:
                if hasattr(self, 'db_manager'):
                    self.db_manager.disconnect()
            except:
                pass  # 忽略重复关闭错误
    
    def _execute_sql(self, sql: str):
        """
        执行SQL并显示结果
        
        Args:
            sql: 要执行的SQL
            
        Returns:
            执行是否成功
        """
        try:
            import pandas as pd
            
            # 使用数据库管理器执行SQL
            df = self.db_manager.execute_analysis_sql(sql)
            
            if df is not None and not df.empty:
                logger.info(f"✅ SQL执行成功，返回 {len(df)} 行数据")
                logger.info("\n📊 查询结果预览 (前5行):")
                logger.info("-" * 60)
                logger.info(df.head().to_string())
                logger.info("-" * 60)
                return True
            elif df is not None and df.empty:
                logger.info("✅ SQL执行成功，但返回空结果集")
                return True
            else:
                logger.error("❌ SQL执行失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ 执行SQL时出错: {str(e)}")
            return False
    
    def _clean_analysis_result(self, result: str) -> str:
        """清理AI分析结果，移除think标签和多余换行"""
        import re
        
        # 移除 <think>...</think> 标签及其内容
        result = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL)
        
        # 移除多余的空行
        result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)
        
        # 去除首尾空白
        result = result.strip()
        
        return result

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="PPT报告生成器 - 整合数据处理和PPT生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 生成完整PPT报告（处理所有任务，默认全球通分析）
  python src/ppt_generator.py -t file/model.pptx -o file/ppt_report_202507.pptx -m 202507
  
  # 指定特定任务生成报告
  python src/ppt_generator.py -t file/model.pptx -o file/ppt_report_202507.pptx -m 202507 --sql-id 5
  
  # 使用中高端分析配置
  python src/ppt_generator.py -t file/model.pptx -o file/ppt_report_202507.pptx -m 202507 -a 2
  
  # 指定多个任务
  python src/ppt_generator.py -t file/model.pptx -o file/ppt_report_202507.pptx -m 202507 --sql-id 1 2 3
  
  # 执行SQL模式 - 处理SQL模板（不生成PPT）
  python src/ppt_generator.py -t file/model.pptx -m 202507 -s "SELECT * FROM table WHERE month = {op_month}"
  
  # 从文件读取SQL并执行
  python src/ppt_generator.py -t file/model.pptx -m 202507 -f sql_template.sql --execute
  
  # 处理分析任务的SQL（类似month_command功能）
  python src/ppt_generator.py -t file/model.pptx -m 202507 --sql-id 5 --execute
        """
    )
    
    parser.add_argument('--template', '-t', required=True,
                        help='PPT模板文件路径')
    parser.add_argument('--output', '-o',
                        help='输出PPT文件路径（生成PPT时必需）')
    parser.add_argument('--month', '-m', required=True,
                        help='月份参数，格式为YYYYMM，如202507')
    parser.add_argument('--sql-id', '--id', type=int, nargs='*',
                        help='指定的分析任务SQL ID，支持单个或多个ID')
    parser.add_argument('--analysis-id', '-a', type=int, default=1,
                        help='分析配置ID，1=全球通"量质构效"分析，2=中高端"量质构效"分析 (默认: 1)')
    parser.add_argument('--execute', '-e', action='store_true',
                        help='实际执行SQL（默认只显示处理结果和生成PPT）')
    parser.add_argument('--sql', '-s', 
                        help='SQL模板，包含{op_month}和{last_op_month}变量，仅处理SQL不生成PPT')
    parser.add_argument('--file', '-f',
                        help='从文件读取SQL模板，仅处理SQL不生成PPT')
    
    args = parser.parse_args()
    
    # 判断处理模式
    sql_mode = args.sql or args.file
    ppt_mode = not sql_mode
    
    # 参数验证
    if ppt_mode:
        # PPT生成模式需要模板和输出文件
        if not args.output:
            logger.error("❌ PPT生成模式需要指定输出文件路径 (-o/--output)")
            sys.exit(1)
        
        if not Path(args.template).exists():
            logger.error(f"❌ 模板文件不存在: {args.template}")
            sys.exit(1)
        
        # 创建输出目录
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.file and not Path(args.file).exists():
        logger.error(f"❌ SQL文件不存在: {args.file}")
        sys.exit(1)
    
    # 创建生成器
    generator = PPTReportGenerator()
    
    if sql_mode:
        # SQL处理模式
        if args.sql:
            # 直接处理SQL模板
            success = generator.process_sql_template(args.sql, args.month, args.execute)
        elif args.file:
            # 从文件读取SQL模板
            with open(args.file, 'r', encoding='utf-8') as f:
                sql_template = f.read()
            success = generator.process_sql_template(sql_template, args.month, args.execute)
    else:
        # PPT生成模式
        success = generator.generate_report(
            template_file=args.template,
            output_file=args.output,
            month_str=args.month,
            sql_ids=args.sql_id,
            analysis_id=args.analysis_id,
            execute_sql=args.execute
        )
    
    if success:
        logger.info("🎯 任务完成!")
        sys.exit(0)
    else:
        logger.error("💥 任务失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()