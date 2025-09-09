#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KPI PPT 命令行工具

提供命令行界面来处理带有KPI参数的PPT文件
"""

import argparse
import logging
import sys
import os
from datetime import datetime
from typing import Optional

try:
    from .enhanced_ppt_processor import EnhancedPPTProcessor
    from .database_config import DatabaseManager, DatabaseConfig, get_database_manager
except ImportError:
    from enhanced_ppt_processor import EnhancedPPTProcessor
    from database_config import DatabaseManager, DatabaseConfig, get_database_manager


def setup_logging(verbose: bool = False):
    """设置日志配置"""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                f'kpi_ppt_log_{datetime.now().strftime("%Y%m%d")}.log',
                encoding='utf-8'
            )
        ]
    )


def validate_month(month_str: str) -> bool:
    """
    验证月份参数格式
    
    Args:
        month_str: 月份字符串
        
    Returns:
        是否有效
    """
    import re
    
    if not re.match(r'^\d{6}$', month_str):
        return False
    
    try:
        year = int(month_str[:4])
        month = int(month_str[4:])
        
        if month < 1 or month > 12:
            return False
        
        if year < 2020 or year > 2030:
            return False
        
        return True
        
    except ValueError:
        return False


def generate_output_path(template_path: str, custom_output: Optional[str] = None) -> str:
    """
    生成输出文件路径
    
    Args:
        template_path: 模板文件路径
        custom_output: 自定义输出路径
        
    Returns:
        输出文件路径
    """
    if custom_output:
        return custom_output
    
    # 自动生成输出路径
    base_name = os.path.splitext(os.path.basename(template_path))[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.dirname(template_path)
    
    return os.path.join(output_dir, f"{base_name}_kpi_updated_{timestamp}.pptx")


def process_ppt_with_kpi(
    template_path: str,
    month: str,
    output_path: Optional[str] = None,
    db_config: Optional[str] = None,
    verbose: bool = False,
    analysis_id: int = 1,
    sql_ids: list = None
) -> bool:
    """
    处理带有KPI参数的PPT文件
    
    Args:
        template_path: PPT模板文件路径
        month: 月份参数 (YYYYMM)
        output_path: 输出文件路径，可选
        db_config: 数据库配置名称，可选
        verbose: 是否显示详细信息
        analysis_id: 分析配置ID，1=全球通"量质构效"分析，2=中高端"量质构效"分析
        sql_ids: 指定的分析任务SQL ID列表，为空则处理所有任务
        
    Returns:
        处理是否成功
    """
    logger = logging.getLogger(__name__)
    
    try:
        # 1. 验证输入参数
        if not os.path.exists(template_path):
            logger.error(f"模板文件不存在: {template_path}")
            return False
        
        if not validate_month(month):
            logger.error(f"月份参数格式错误: {month} (应为YYYYMM格式)")
            return False
        
        # 2. 设置数据库管理器
        db_manager = None
        if db_config:
            try:
                db_manager = get_database_manager(db_config)
                if not db_manager.test_connection():
                    logger.error(f"数据库连接失败: {db_config}")
                    return False
            except Exception as e:
                logger.error(f"数据库配置错误: {e}")
                return False
        
        # 3. 初始化PPT处理器
        logger.info(f"开始处理PPT: {template_path}")
        logger.info(f"月份参数: {month}")
        if sql_ids:
            logger.info(f"指定处理SQL ID: {sql_ids}")
        else:
            logger.info("处理所有可用的分析任务")
        
        processor = EnhancedPPTProcessor(template_path, db_manager, analysis_id, sql_ids)
        
        # 4. 加载模板
        if not processor.load_template():
            logger.error("PPT模板加载失败")
            return False
        
        # 5. 执行替换处理
        logger.info("开始KPI参数替换...")
        results = processor.process_complete_replacement(month)
        
        # 6. 生成并显示报告
        report = processor.generate_replacement_report(results)
        logger.info("替换完成，结果报告:")
        print(report)
        
        # 7. 保存结果
        final_output_path = generate_output_path(template_path, output_path)
        logger.info(f"保存PPT到: {final_output_path}")
        
        if processor.save_presentation(final_output_path):
            logger.info("PPT保存成功")
            print(f"\n✅ 处理完成！输出文件: {final_output_path}")
            return True
        else:
            logger.error("PPT保存失败")
            return False
        
    except Exception as e:
        logger.error(f"处理过程中发生错误: {e}")
        return False


def main():
    """主函数 - 命令行入口"""
    parser = argparse.ArgumentParser(
        description="PPT KPI参数替换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 基本用法（默认全球通分析）
  python src/kpi_ppt_command.py -t file/model.pptx -m 202507
  
  # 指定输出文件
  python src/kpi_ppt_command.py -t file/model.pptx -m 202507 -o report_202507.pptx
  
  # 使用中高端分析配置
  python src/kpi_ppt_command.py -t file/model.pptx -m 202507 -a 2
  
  # 指定单个分析任务
  python src/kpi_ppt_command.py -t file/model.pptx -m 202507 --sql-id 5
  
  # 指定多个分析任务
  python src/kpi_ppt_command.py -t file/model.pptx -m 202507 --sql-id 1 2 3
  
  # 指定任务+中高端分析配置
  python src/kpi_ppt_command.py -t file/model.pptx -m 202507 --sql-id 5 -a 2
  
  # 指定数据库配置
  python src/kpi_ppt_command.py -t file/model.pptx -m 202507 --db-config mysql_prod
  
  # 详细模式
  python src/kpi_ppt_command.py -t file/model.pptx -m 202507 -v

参数说明:
  - 月份参数格式为YYYYMM，如202507表示2025年7月
  - KPI占位符格式为{{kpi_X_Y}}，X为SQL ID，Y为列索引
  - 支持SQLite和MySQL数据库连接
        """
    )
    
    # 必需参数
    parser.add_argument(
        '-t', '--template',
        required=True,
        help='PPT模板文件路径'
    )
    
    parser.add_argument(
        '-m', '--month',
        required=True,
        help='月份参数 (YYYYMM格式，如202507)'
    )
    
    # 可选参数
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径 (不指定则自动生成)'
    )
    
    parser.add_argument(
        '--db-config',
        choices=['mysql_prod'],
        default='mysql_prod',
        help='数据库配置名称 (默认: mysql_prod)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    
    parser.add_argument(
        '-a', '--analysis-id',
        type=int,
        default=1,
        help='分析配置ID，1=全球通"量质构效"分析，2=中高端"量质构效"分析 (默认: 1)'
    )
    
    parser.add_argument(
        '--sql-id', '--id',
        type=int,
        nargs='*',
        help='指定的分析任务SQL ID，支持单个或多个ID，如: --sql-id 5 或 --sql-id 1 2 3'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='KPI PPT Processor v1.0'
    )
    
    # 解析参数
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.verbose)
    
    # 执行处理
    success = process_ppt_with_kpi(
        template_path=args.template,
        month=args.month,
        output_path=args.output,
        db_config=args.db_config,
        verbose=args.verbose,
        analysis_id=args.analysis_id,
        sql_ids=args.sql_id
    )
    
    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()