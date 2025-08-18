import pandas as _pd

from sqlalchemy import (
    MetaData as _MetaData, 
    Table as _Table
)
from sqlalchemy.dialects.postgresql.base import (
    DOUBLE_PRECISION as _DOUBLE_PRECISION
)
from sqlalchemy.sql.sqltypes import (
    INTEGER as _INTEGER,
    VARCHAR as _VARCHAR,
    TIMESTAMP as _TIMESTAMP,
    FLOAT as _FLOAT,
    DATE as _DATE,
)
from datetime import datetime as _dt


class Dtype:
    def __init__(self, sqltypes, dtype) -> None:
        self.sqltypes = sqltypes
        self.dtype = dtype


INT64 = Dtype((_INTEGER), 'Int64')

FLOAT64 = Dtype((_FLOAT, _DOUBLE_PRECISION), 'float64')

STRING = Dtype((_VARCHAR), 'string')

DATETIME64 = Dtype((_TIMESTAMP), 'datetime64')

DATE = Dtype((_DATE), 'date')

_TYPES = [INT64, FLOAT64, STRING, DATETIME64, DATE]

def dtype(t):
    for _t in _TYPES:
        if isinstance(t, _t.sqltypes):
            return _t.dtype

    raise ValueError(type(t))


def dtypes_columns(conn, table, schema):
    metadata = _MetaData()
    table_info = _Table(table, metadata, autoload_with=conn, schema=schema)

    return {
        value.name: dtype(value.type)
        for value in table_info.columns
    }


def df_header(conn, table, schema):
    type_columns = dtypes_columns(conn, table, schema)

    template = {
        INT64.dtype: [-1, -2, -3],
        FLOAT64.dtype: [-1, -2, -3],
        STRING.dtype: ['Não Informado', 'Não Aplicável', 'Desconhecido'],
        DATETIME64.dtype: [_dt(1900, 1, 1), _dt(1900, 1, 2), _dt(1900, 1, 3)],
        DATE.dtype: [_dt(1900, 1, 1), _dt(1900, 1, 2), _dt(1900, 1, 3)],
    }

    return _pd.DataFrame({k: template.get(d) for k, d in type_columns.items()})
