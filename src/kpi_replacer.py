#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KPI参数替换模块

用于处理PPT中的KPI参数，从数据库获取数据并替换相应的占位符。
参数格式：{{kpi_1_1}} {{kpi_1_2}} 等，其中第一个数字为anaylsis_sql_id，第二个数字为列索引。
"""

import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import re
try:
    from .database_config import DatabaseManager, DatabaseConfig
except ImportError:
    from database_config import DatabaseManager, DatabaseConfig


@dataclass
class KpiData:
    """KPI数据结构"""
    sql_id: int
    analysis_id: int
    analysis_name: str
    level1_name: str
    level2_name: str
    sql_test: str
    top_sql_test: str
    op_month: str
    sql_flag: int


class KpiReplacer:
    """KPI参数替换器"""
    
    def __init__(self, db_manager: DatabaseManager = None, analysis_id: int = 1, sql_ids: list = None):
        """
        初始化KPI替换器
        
        Args:
            db_manager: 数据库管理器实例
            analysis_id: 分析配置ID，1=全球通"量质构效"分析，2=中高端"量质构效"分析
            sql_ids: 指定的分析任务SQL ID列表，为空则处理所有任务
        """
        self.db_manager = db_manager
        self.analysis_id = analysis_id
        self.sql_ids = sql_ids
        self.logger = logging.getLogger(__name__)
        
        if not self.db_manager:
            # 使用默认配置
            try:
                from .database_config import get_database_manager
            except ImportError:
                from database_config import get_database_manager
            self.db_manager = get_database_manager('mysql_prod')
    
    def get_analysis_data(self) -> List[KpiData]:
        """
        从数据库获取分析数据
            
        Returns:
            KpiData对象列表
        """
        # 构建查询条件
        if self.sql_ids:
            # 指定SQL ID的查询
            id_placeholders = ','.join(['%s'] * len(self.sql_ids))
            query = f"""
            SELECT 
                anaylsis_sql_id,
                anaylsis_id,
                anaylsis_name,
                anaylsis_lev1_name,
                anaylsis_lev2_name,
                anaylsis_sql_test,
                top_sql_test,
                op_month,
                sql_flag
            FROM anaylsis_deploy_ppt_def
            WHERE sql_flag = 1 AND anaylsis_id = %s AND anaylsis_sql_id IN ({id_placeholders})
            ORDER BY anaylsis_sql_id
            """
            query_params = [self.analysis_id] + self.sql_ids
        else:
            # 获取所有任务的查询
            query = """
            SELECT 
                anaylsis_sql_id,
                anaylsis_id,
                anaylsis_name,
                anaylsis_lev1_name,
                anaylsis_lev2_name,
                anaylsis_sql_test,
                top_sql_test,
                op_month,
                sql_flag
            FROM anaylsis_deploy_ppt_def
            WHERE sql_flag = 1 AND anaylsis_id = %s
            ORDER BY anaylsis_sql_id
            """
            query_params = (self.analysis_id,)
        
        try:
            rows = self.db_manager.execute_query(query, query_params)
            
            kpi_data_list = []
            for row in rows:
                kpi_data = KpiData(
                    sql_id=row['anaylsis_sql_id'],
                    analysis_id=row['anaylsis_id'],
                    analysis_name=row['anaylsis_name'],
                    level1_name=row['anaylsis_lev1_name'],
                    level2_name=row['anaylsis_lev2_name'],
                    sql_test=row['anaylsis_sql_test'],
                    top_sql_test=row['top_sql_test'],
                    op_month=row['op_month'],
                    sql_flag=row['sql_flag']
                )
                kpi_data_list.append(kpi_data)
                
            self.logger.info(f"成功获取 {len(kpi_data_list)} 条分析数据")
            return kpi_data_list
            
        except Exception as e:
            self.logger.error(f"获取分析数据失败: {e}")
            raise
    
    def replace_month_parameters(self, sql: str, current_month: str) -> str:
        """
        替换SQL中的月份参数
        
        Args:
            sql: 原始SQL语句
            current_month: 当前月份，格式为YYYYMM
            
        Returns:
            替换后的SQL语句
        """
        # 计算上个月
        year = int(current_month[:4])
        month = int(current_month[4:])
        
        if month == 1:
            last_year = year - 1
            last_month = 12
        else:
            last_year = year
            last_month = month - 1
            
        last_month_str = f"{last_year:04d}{last_month:02d}"
        
        # 替换月份参数
        # 根据实际的SQL模板格式进行调整
        # 处理各种可能的占位符格式
        # 注意：这里只替换占位符本身，不添加引号，因为模板中可能已经包含引号
        sql = sql.replace('{op_month}', current_month)
        sql = sql.replace('{last_op_month}', last_month_str)
        sql = sql.replace('{last_month}', last_month_str)
        
        # 移除错误的硬编码替换逻辑
        # 原来的错误代码：
        # sql = sql.replace("''202507''", f"'{current_month}'")  # 这是错误的！
        # sql = sql.replace("''202506''", f"'{last_month_str}'")  # 这是错误的！
        
        # 处理其他可能的月份占位符格式
        import re
        # 注意：移除了硬编码的月份替换，避免错误替换
        
        # 处理表名中的月份后缀，如 anaylsis_qqt_lzgx_st_mm
        # 这里需要根据实际的表名规则进行调整
        
        self.logger.debug(f"月份参数替换完成: 当前月份={current_month}, 上个月份={last_month_str}")
        self.logger.debug(f"替换后的SQL预览: {sql[:200]}...")
        return sql
    
    def execute_sql_query(self, sql: str) -> List[Dict]:
        """
        执行SQL查询
        
        Args:
            sql: SQL语句
            
        Returns:
            查询结果列表
        """
        try:
            self.logger.debug(f"执行SQL查询: {sql}")
            results = self.db_manager.execute_query(sql)
            
            self.logger.info(f"查询完成，返回 {len(results)} 行数据")
            return results
            
        except Exception as e:
            self.logger.error(f"SQL查询失败: {e}")
            raise
    
    def extract_kpi_placeholders(self, text: str) -> List[Tuple[str, int, int]]:
        """
        提取文本中的KPI占位符
        
        Args:
            text: 要搜索的文本
            
        Returns:
            包含 (完整占位符, sql_id, 列索引) 的元组列表
        """
        # 匹配格式: {{kpi_数字_数字}}
        pattern = r'\{\{kpi_(\d+)_(\d+)\}\}'
        matches = re.findall(pattern, text)
        
        placeholders = []
        for match in re.finditer(pattern, text):
            full_placeholder = match.group(0)
            sql_id = int(match.group(1))
            column_index = int(match.group(2))
            placeholders.append((full_placeholder, sql_id, column_index))
        
        return placeholders
    
    def get_kpi_values(self, current_month: str) -> Dict[Tuple[int, int], Any]:
        """
        获取所有KPI值
        
        Args:
            current_month: 当前月份，格式为YYYYMM
            
        Returns:
            字典，键为(sql_id, column_index)，值为对应的数据
        """
        kpi_values = {}
        
        # 获取分析数据
        analysis_data_list = self.get_analysis_data()
        
        for kpi_data in analysis_data_list:
            # 替换月份参数
            processed_sql = self.replace_month_parameters(
                kpi_data.top_sql_test, 
                current_month
            )
            
            # 执行SQL查询
            try:
                results = self.execute_sql_query(processed_sql)
                
                if results and len(results) > 0:
                    # 假设查询结果只有一行数据
                    row_data = results[0]
                    
                    # 将每一列的数据存储到字典中
                    if isinstance(row_data, dict):
                        # 字典格式，按照列名顺序
                        for col_index, value in enumerate(row_data.values(), 1):
                            key = (kpi_data.sql_id, col_index)
                            kpi_values[key] = value
                            
                            self.logger.debug(
                                f"KPI数据: sql_id={kpi_data.sql_id}, "
                                f"column={col_index}, value={value}"
                            )
                    else:
                        # 元组格式
                        for col_index, value in enumerate(row_data, 1):
                            key = (kpi_data.sql_id, col_index)
                            kpi_values[key] = value
                            
                            self.logger.debug(
                                f"KPI数据: sql_id={kpi_data.sql_id}, "
                                f"column={col_index}, value={value}"
                            )
                
            except Exception as e:
                self.logger.error(
                    f"处理 sql_id={kpi_data.sql_id} 时出错: {e}"
                )
                continue
        
        return kpi_values
    
    def replace_kpi_in_text(self, text: str, current_month: str) -> str:
        """
        替换文本中的KPI占位符
        
        Args:
            text: 包含KPI占位符的文本
            current_month: 当前月份，格式为YYYYMM
            
        Returns:
            替换后的文本
        """
        # 提取所有KPI占位符
        placeholders = self.extract_kpi_placeholders(text)
        
        if not placeholders:
            self.logger.info("未找到KPI占位符")
            return text
        
        # 获取所有KPI值
        kpi_values = self.get_kpi_values(current_month)
        
        # 进行替换
        result_text = text
        replaced_count = 0
        
        for full_placeholder, sql_id, column_index in placeholders:
            key = (sql_id, column_index)
            
            if key in kpi_values:
                value = kpi_values[key]
                result_text = result_text.replace(full_placeholder, str(value))
                replaced_count += 1
                
                self.logger.info(
                    f"替换成功: {full_placeholder} -> {value}"
                )
            else:
                self.logger.warning(
                    f"未找到对应的KPI数据: {full_placeholder} "
                    f"(sql_id={sql_id}, column={column_index})"
                )
        
        self.logger.info(f"KPI参数替换完成，共替换 {replaced_count} 个占位符")
        return result_text


def main():
    """测试函数"""
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 测试KPI替换功能
    replacer = KpiReplacer()
    
    # 示例文本
    test_text = """
    分析报告：
    本月全球通客户收入为 {{kpi_1_1}} 亿元，
    较上月减少 {{kpi_1_2}} 万元。
    拍照全球通客户收入为 {{kpi_1_3}} 亿元，
    较上月减少 {{kpi_1_4}} 万元。
    
    客户数据：
    全球通客户数为 {{kpi_2_1}} 万户，
    白金及以上客户为 {{kpi_2_2}} 万户。
    """
    
    try:
        # 替换KPI参数
        result = replacer.replace_kpi_in_text(test_text, "202507")
        print("替换结果:")
        print(result)
        
    except Exception as e:
        logging.error(f"测试失败: {e}")


if __name__ == "__main__":
    main()