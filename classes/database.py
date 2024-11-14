import pymysql
import dbutils.pooled_db
import pymysql.cursors
import pymysql.connections
from interfaces import ConnectionPoolInterface
from typing import Callable


class ConnectionPool(ConnectionPoolInterface):
    def __init__(self, host: str, user: str, password: str, database: str, port: int) -> None:
        self.pool = dbutils.pooled_db.PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=2,
            maxcached=5,
            blocking=True,
            maxusage=None,
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            cursorclass=pymysql.cursors.DictCursor
        )


    class ReturnedSql:
        def __init__(self, sqlres: list[dict], rowcount: int, close: Callable) -> None:
            self.sqlres = sqlres
            self.rowcount = rowcount
            self.close = close


        def __enter__(self):
            return self


        def __exit__(self, *exc) -> None:
            self.close()


    def _connect(self) -> (pymysql.connections.Connection):
        return self.pool.connection()


    def _disconnect(self, conn: pymysql.connections.Connection):
        if conn:
            conn.close()


    def runsql(self, sql: str) -> int:
        r = 0
        conn = self._connect()
        with conn.cursor() as cursor:
            cursor: pymysql.cursors.DictCursor
            cursor.execute(sql)
            conn.commit()
            r = cursor.rowcount
        self._disconnect(conn)
        return r


    def select(self, sql: str) -> ReturnedSql:
        result = []
        conn = self._connect()
        with conn.cursor() as cursor:
            cursor: pymysql.cursors.DictCursor
            cursor.execute(sql)
            result = self.ReturnedSql(cursor.fetchall(), cursor.rowcount, lambda: self._disconnect(conn))
            return result
