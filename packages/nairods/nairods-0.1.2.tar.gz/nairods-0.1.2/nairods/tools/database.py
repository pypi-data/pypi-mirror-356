# 文件名：database.py
# 作者：nairoads
# 日期：2025-06-18 15:22:37
# 描述：PostgreSQL 数据库操作工具

import pandas as pd
import psycopg2
from .file import YamlUtils
from typing import Any

class PostgresUtils:
    """
    PostgreSQL 数据库操作工具
    """
    def __init__(self, pg_config_path: str):
        self.pg_config_path = pg_config_path
        self.config = self.read_pg_config()
        self.host = self.config.get("host")
        self.port = self.config.get("port")
        self.database = self.config.get("database")
        self.user = self.config.get("username")
        self.password = self.config.get("password")

    def read_pg_config(self) -> dict:
        """
        读取pg配置
        :return: 配置字典
        """
        yml = YamlUtils(self.pg_config_path)
        res_yml = yml.read_yaml()
        pg = res_yml['pg']
        return pg

    def get_pg_version(self) -> Any:
        """
        查询pg版本号
        :return: 版本信息
        """
        conn = psycopg2.connect(
            host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()
        return version

    def select_data_sql(self, sql_query: str) -> Any:
        """
        sql语句查询
        :param sql_query:  请求的sql
        :return: 查询的数据
        """
        conn = psycopg2.connect(
            host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
        cur = conn.cursor()
        cur.execute(sql_query)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    def select_data_pd(self, sql_query: str) -> pd.DataFrame:
        """
        sql语句查询，返回DataFrame
        :param sql_query:  请求的sql
        :return: 查询的数据DataFrame
        """
        conn = psycopg2.connect(
            host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
        df = pd.read_sql(sql_query, conn)
        conn.close()
        return df

__all__ = ["PostgresUtils"] 