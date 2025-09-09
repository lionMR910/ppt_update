#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库配置和连接模块

提供数据库连接的配置和管理功能
"""

import sqlite3
import logging

try:
    import pymysql
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False
from typing import Dict, Any, Optional
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class DatabaseConfig:
    """数据库配置"""
    db_type: str  # 'sqlite', 'mysql', 'postgresql' 等
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    file_path: Optional[str] = None  # 用于 SQLite
    charset: str = 'utf8mb4'
    
    def __post_init__(self):
        """初始化后验证配置"""
        if self.db_type == 'sqlite' and not self.file_path:
            raise ValueError("SQLite 数据库需要指定 file_path")
        elif self.db_type == 'mysql' and not all([self.host, self.database]):
            raise ValueError("MySQL 数据库需要指定 host 和 database")


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, config: DatabaseConfig):
        """
        初始化数据库管理器
        
        Args:
            config: 数据库配置
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    @contextmanager
    def get_connection(self):
        """
        获取数据库连接（上下文管理器）
        
        Yields:
            数据库连接对象
        """
        connection = None
        try:
            connection = self._create_connection()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            self.logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            if connection:
                connection.close()
    
    def _create_connection(self):
        """
        创建数据库连接
        
        Returns:
            数据库连接对象
        """
        if self.config.db_type == 'sqlite':
            return self._create_sqlite_connection()
        elif self.config.db_type == 'mysql':
            return self._create_mysql_connection()
        else:
            raise ValueError(f"不支持的数据库类型: {self.config.db_type}")
    
    def _create_sqlite_connection(self):
        """创建 SQLite 连接"""
        try:
            connection = sqlite3.connect(self.config.file_path)
            connection.row_factory = sqlite3.Row  # 启用字典式访问
            self.logger.debug(f"SQLite 连接成功: {self.config.file_path}")
            return connection
        except Exception as e:
            self.logger.error(f"SQLite 连接失败: {e}")
            raise
    
    def _create_mysql_connection(self):
        """创建 MySQL 连接"""
        if not PYMYSQL_AVAILABLE:
            raise ImportError("PyMySQL 未安装，无法连接 MySQL 数据库")
        
        try:
            connection = pymysql.connect(
                host=self.config.host,
                port=self.config.port or 3306,
                user=self.config.username,
                password=self.config.password,
                database=self.config.database,
                charset=self.config.charset,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.logger.debug(f"MySQL 连接成功: {self.config.host}:{self.config.port}")
            return connection
        except Exception as e:
            self.logger.error(f"MySQL 连接失败: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        测试数据库连接
        
        Returns:
            连接是否成功
        """
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                if self.config.db_type == 'sqlite':
                    cursor.execute("SELECT 1")
                elif self.config.db_type == 'mysql':
                    cursor.execute("SELECT 1")
                cursor.fetchone()
                self.logger.info("数据库连接测试成功")
                return True
        except Exception as e:
            self.logger.error(f"数据库连接测试失败: {e}")
            return False
    
    def execute_query(self, sql: str, params: tuple = None) -> list:
        """
        执行查询SQL
        
        Args:
            sql: SQL语句
            params: 参数元组
            
        Returns:
            查询结果列表
        """
        with self.get_connection() as connection:
            cursor = connection.cursor()
            
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            if self.config.db_type == 'sqlite':
                # SQLite 返回 Row 对象，转换为字典
                results = [dict(row) for row in cursor.fetchall()]
            else:
                # MySQL 已经配置为返回字典
                results = cursor.fetchall()
                
            return results
    
    def execute_non_query(self, sql: str, params: tuple = None) -> int:
        """
        执行非查询SQL（INSERT, UPDATE, DELETE）
        
        Args:
            sql: SQL语句
            params: 参数元组
            
        Returns:
            受影响的行数
        """
        with self.get_connection() as connection:
            cursor = connection.cursor()
            
            if params:
                affected_rows = cursor.execute(sql, params)
            else:
                affected_rows = cursor.execute(sql)
                
            connection.commit()
            return affected_rows


# 默认配置
DEFAULT_CONFIGS = {
    'mysql_prod': DatabaseConfig(
        db_type='mysql',
        host='10.68.111.11',
        port=9030,
        database='chatbi',
        username='root',
        password='radar_360'
    )
}


def get_database_manager(config_name: str = 'mysql_prod') -> DatabaseManager:
    """
    获取数据库管理器实例
    
    Args:
        config_name: 配置名称
        
    Returns:
        数据库管理器实例
    """
    if config_name not in DEFAULT_CONFIGS:
        raise ValueError(f"未找到配置: {config_name}")
    
    config = DEFAULT_CONFIGS[config_name]
    return DatabaseManager(config)


def main():
    """测试函数"""
    logging.basicConfig(level=logging.INFO)
    
    # 测试 MySQL 连接
    mysql_manager = get_database_manager('mysql_prod')
    
    if mysql_manager.test_connection():
        print("MySQL 连接测试成功")
    else:
        print("MySQL 连接测试失败")


if __name__ == "__main__":
    main()