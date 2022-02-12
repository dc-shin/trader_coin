from enum import Enum
from pickle import FALSE

from numpy import empty
from Singleton import Singleton
import sqlite3
import pandas as pd

class OrderType(Enum):
    ASC = 0 # 오름차순
    DESC = 1 # 내림차순

    @staticmethod
    def toString(type):
        return ('ASC' if type == OrderType.ASC else 'DESC')


class DatabaseManager(Singleton):
    def __init__(self):
        self.conn = sqlite3.connect(self.get_db_dir_path() + self.get_db_file_name())

    def __del__(self):
        self.conn.close()

    def get_db_dir_path(self):
        return './Database/'

    def get_db_file_name(self):
        return 'upbit.db'

    def existTable(self, table_name):
        cursor = self.conn.execute(
            """
            SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{}'
            """
            .format(table_name))
        return cursor.fetchall()[0][0] > 0

    def insert(self, table_name, data_frame):
        ##push the dataframe to sql 
        data_frame.to_sql(table_name, self.conn, if_exists='append')
        self.conn.commit()

    def select(self, table_name, count=0, order_col_name='', order=OrderType.ASC, index_col_name=''):
        if not self.existTable(table_name):
            return pd.DataFrame()

        sql_order = '' if not order_col_name else 'order by {} {}'.format(order_col_name, OrderType.toString(order))
        sql_limit = '' if count <= 0 else 'limit {}'.format(count)

        df = pd.read_sql_query(
            """
            select * from {} {} {}
            """
            .format(table_name, sql_order, sql_limit)
            , self.conn
        )

        if index_col_name:
            df.set_index(index_col_name, inplace=True)

        return df