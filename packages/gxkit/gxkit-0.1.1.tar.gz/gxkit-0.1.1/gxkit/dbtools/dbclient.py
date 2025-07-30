"""
dbclient - DB客户端工厂函数
Version: 0.1.1
"""
from typing import Union, Literal, TYPE_CHECKING
from gxkit.core.loader import try_import_dbtools

if TYPE_CHECKING:
    from gxkit_dbtools.client.mysql_client import MySQLClient
    from gxkit_dbtools.client.clickhouse_client import ClickHouseClient
    from gxkit_dbtools.client.iotdb_client import IoTDBClient

try:
    from gxkit_dbtools.client.mysql_client import MySQLClient
    from gxkit_dbtools.client.clickhouse_client import ClickHouseClient
    from gxkit_dbtools.client.iotdb_client import IoTDBClient
except ImportError:
    _dbtools = try_import_dbtools()
    MySQLClient = _dbtools.MySQLClient
    ClickHouseClient = _dbtools.ClickHouseClient
    IoTDBClient = _dbtools.IoTDBClient


def dbclient(db_type: Literal["mysql", "clickhouse", "iotdb"], host: str, port: int, user: str, password: str,
             database: str = None, **kwargs) -> Union[MySQLClient, ClickHouseClient, IoTDBClient]:
    if db_type == "mysql":
        return MySQLClient(
            host=host, port=port, user=user, password=password, database=database, **kwargs
        )
    elif db_type == "clickhouse":
        return ClickHouseClient(
            host=host, port=port, user=user, password=password, database=database, **kwargs
        )
    elif db_type == "iotdb":
        return IoTDBClient(
            host=host, port=port, user=user, password=password, **kwargs
        )
    else:
        raise ValueError(f"[dbtools.dbclient] Unknown client type: {db_type}")
