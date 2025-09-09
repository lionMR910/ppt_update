#!/usr/bin/env python3
"""
PPT模板文字替换程序
主程序入口 - 提供命令行界面
"""

import argparse
import sys
import os
import logging
from datetime import datetime
from colorama import init, Fore, Style
from ppt_processor import PPTProcessor
from config import FILE_CONFIG


# 初始化colorama用于彩色输出
init(autoreset=True)


def setup_logging(verbose: bool = False):
    """
    设置日志记录
    
    Args:
        verbose: 是否启用详细日志
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # 创建日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 文件处理器
    log_filename = f"ppt_replacer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # 配置根日志器
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return log_filename


def print_header():
    """打印程序头信息"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}PPT模板文字替换程序")
    print(f"{Fore.CYAN}版本: 1.0")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")


def print_success(message: str):
    """打印成功消息"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str):
    """打印错误消息"""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_warning(message: str):
    """打印警告消息"""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_info(message: str):
    """打印信息消息"""
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def validate_template_file(template_path: str) -> bool:
    """
    验证模板文件
    
    Args:
        template_path: 模板文件路径
        
    Returns:
        bool: 验证通过返回True
    """
    if not os.path.exists(template_path):
        print_error(f"模板文件不存在: {template_path}")
        return False
    
    if not template_path.lower().endswith(('.ppt', '.pptx')):
        print_error(f"不支持的文件格式: {template_path}")
        return False
    
    try:
        file_size = os.path.getsize(template_path)
        if file_size > 50 * 1024 * 1024:  # 50MB
            print_warning(f"文件较大 ({file_size / 1024 / 1024:.1f}MB)，处理可能较慢")
    except OSError:
        print_error(f"无法读取文件信息: {template_path}")
        return False
    
    return True


def generate_output_path(template_path: str, output_path: str = None) -> str:
    """
    生成输出文件路径
    
    Args:
        template_path: 模板文件路径
        output_path: 指定的输出路径
        
    Returns:
        str: 输出文件路径
    """
    if output_path:
        return output_path
    
    # 自动生成输出路径
    template_dir = os.path.dirname(template_path)
    template_name = os.path.splitext(os.path.basename(template_path))[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    output_filename = f"{template_name}{FILE_CONFIG['output_suffix']}_{timestamp}.pptx"
    return os.path.join(template_dir, output_filename)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='PPT模板文字替换程序',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s -t file/ces.pptx
  %(prog)s -t file/ces.pptx -o report_2024.pptx
  %(prog)s -t file/ces.pptx -v
        """
    )
    
    parser.add_argument(
        '-t', '--template',
        required=True,
        help='PPT模板文件路径'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径（可选，默认在模板目录生成带时间戳的文件）'
    )
    
    parser.add_argument(
        '-c', '--config',
        help='配置文件路径（可选，默认使用内置配置）'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细处理信息'
    )
    
    parser.add_argument(
        '--use-static',
        action='store_true',
        help='强制使用静态配置数据而不是数据库动态数据'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='PPT替换程序 v1.0'
    )
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 打印程序头
    print_header()
    
    # 设置日志
    log_file = setup_logging(args.verbose)
    
    if args.verbose:
        print_info(f"日志文件: {log_file}")
    
    try:
        # 验证模板文件
        print_info(f"验证模板文件: {args.template}")
        if not validate_template_file(args.template):
            sys.exit(1)
        
        print_success("模板文件验证通过")
        
        # 生成输出路径
        output_path = generate_output_path(args.template, args.output)
        print_info(f"输出文件路径: {output_path}")
        
        # 创建PPT处理器
        processor = PPTProcessor(args.template)
        
        # 如果指定使用静态数据，预先设置
        if args.use_static:
            from config import REPLACEMENT_DATA
            processor.replacement_data = REPLACEMENT_DATA
            print_info("强制使用静态配置数据")
        
        # 执行处理
        print_info("开始处理PPT文件...")
        
        if processor.process(output_path):
            print_success("PPT处理完成！")
            print_info(f"输出文件: {output_path}")
            
            # 验证输出文件
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print_info(f"输出文件大小: {file_size / 1024:.1f} KB")
            
        else:
            print_error("PPT处理失败")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print_warning("用户中断操作")
        sys.exit(1)
    
    except Exception as e:
        print_error(f"程序执行出错: {e}")
        logging.exception("程序异常")
        sys.exit(1)
    
    finally:
        if args.verbose:
            print_info("程序执行完成")


if __name__ == "__main__":
    main()