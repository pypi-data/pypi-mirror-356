"""
Module: mcpf_db.pg

This module provides functionality to interact with PostgreSQL and TimescaleDB databases. 
It includes utilities for writing pandas DataFrames and CSV files into database tables 
using SQLAlchemy and psycopg2.

Functions:
    - timescale_df_write(data: dict[str, Any]) -> dict[str, Any]:
        Writes a pandas DataFrame into a TimescaleDB database table.

    - postgres_csv_write(data: dict[str, Any]) -> dict[str, Any]:
        Copies a CSV file into a PostgreSQL table using the COPY command.

    - df_to_filelike_to_postgres(data: dict[str, Any]) -> dict[str, Any]:
        Copies a pandas DataFrame into a PostgreSQL table using a file-like object 
        and the COPY command.

Dependencies:
    - mcpf_core.core.routines: Provides utility functions for metadata handling and 
      database configuration retrieval.
    - mcpf_core.func.constants: Contains constants used throughout the module.
    - psycopg2: PostgreSQL database adapter for Python.
    - sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
    - mcpf_db.db.types.DbColumn: Represents column specifications for database tables.
    - mcpf_db.pg.helper: Helper functions for PostgreSQL configuration and table creation.

Usage:
    The module provides three main functions for interacting with PostgreSQL and TimescaleDB:
    - `timescale_df_write`: Writes a pandas DataFrame to a TimescaleDB table.
    - `postgres_csv_write`: Copies data from a CSV file to a PostgreSQL table.
    - `df_to_filelike_to_postgres`: Copies data from a pandas DataFrame to a PostgreSQL table 
      using a file-like object.

Examples:
    Writing a pandas DataFrame to a TimescaleDB table:
    ```yaml
input_path: &base_dir '.'
output_path: *base_dir
entry_point: 'main_p'
database_configs:
  - type: timescale
    url: "postgresql://username:password@the-timescale:5432/thedatabase"

imports:
  - testfunc
  - mcpf_db.pg
pipelines:
  - main_p:
      - set_df:
          - with_index: false
      - timescale_df_write:
          - table: 'simulation_data'

    ```

Notes:
    - The `output` argument is not implemented in any of the functions and will raise a 
      [NotImplementedError](http://_vscodecontentref_/0) if provided.
    - The `quiet` argument suppresses output messages when set to `True`.
    - Column specifications for [df_to_filelike_to_postgres](http://_vscodecontentref_/1) must follow the format 
      `columns_<column_name>_<property>`.

"""

from io import StringIO
from typing import Any

import mcpf_core.core.routines as routines
import mcpf_core.func.constants as constants
import psycopg2
from mcpf_db.db.types import DbColumn
from sqlalchemy import create_engine

import mcpf_db.pg.helper as helper


def timescale_df_write(data: dict[str, Any]) -> dict[str, Any]:
    """
    It writes its pandas dataframe input into timescale database.
    Yaml args:
        'input':            it is a label in "data", which identifies the input data
                            (given in terms of pandas dataframe),
                            by default it is the value identified with the label
                            constants.DEFAULT_IO_DATA_LABEL (if it is a string)
        'db_config':        the key of the database configuration in the config file.
                            Default is 'timescale'.
        'schema':
        'table':

    Returns in data:
        'output':   Not implemented yet!
                    it should be  a label in 'data' which identifies the output
                    (the content of the input pandas dataframe in pandas dataframe),
                    by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    meta = routines.get_meta_data(data)
    arg = {
        "input": constants.DEFAULT_IO_DATA_LABEL,
        "db_config": "timescale",
        "schema": "public",
        "table": "",
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    db_conf = routines.get_db_config(meta, arg["db_config"])
    db_config = helper.postgres_config_from_url(db_conf.get("url", None), db_conf)
    db_url = helper.postgres_update_url_from_config(db_conf.get("url", None), db_config)

    with create_engine(db_url).connect() as con:
        data[arg["input"]].to_sql(
            name=arg["table"],
            con=con,
            schema=arg["schema"],
            if_exists="append",
            index=False,
        )

    # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data


def postgres_csv_write(data: dict[str, Any]) -> dict[str, Any]:
    """
    Copy a CSV file into a PostgreSQL table using the COPY command.
    Yaml args:
                'input':            it is a label in "data", which contains the input file
                                    path,
                                    by default it is the value identified with the label
                                    constants.DEFAULT_IO_DATA_LABEL (if it is a string)
                'db_config':        the key of the database configuration in the config file.
                                    Default is 'postgres'.
                'csv_file_path':    the path to the CSV file to be copied (overrides 'input').
                'schema':           the schema in which the table is located. Default is 'public'.
                'table':            the name of the table to which the data will be copied.
                                    This is a required argument.
                'quiet':           if True, suppresses output messages. Default is False.

            Returns in data:
                'output':   Not implemented yet!
                            it should be  a label in 'data' which identifies the output
                            (the content of the input pandas dataframe in pandas dataframe),
                            by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    meta = routines.get_meta_data(data)
    arg = {
        "input": constants.DEFAULT_IO_DATA_LABEL,
        "db_config": "postgres",
        "csv_file_path": "",
        "schema": "public",
        "table": "",
        "quiet": False,
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]

    if "output" in arg:
        raise NotImplementedError("output is not implemented yet!")

    csv_file_path = arg["csv_file_path"] if "csv_file_path" in arg and arg["csv_file_path"] else data[arg["input"]]

    # Establishing the connection to the database

    db_conf = routines.get_db_config(meta, arg["db_config"])

    table_name = arg["table"]
    db_config = helper.postgres_config_from_url(db_conf.get("url", None), db_conf)

    conn = psycopg2.connect(
        host=db_config.host,
        database=db_config.database,
        user=db_config.user,
        password=db_config.password,
        port=db_config.port,
    )

    with conn:
        # Create a cursor object
        with conn.cursor() as cursor:
            try:
                with open(csv_file_path, "r") as f:
                    sql = psycopg2.sql.SQL("COPY {table_name} FROM STDIN WITH CSV HEADER").format(
                        table_name=psycopg2.sql.Identifier(table_name)
                    )
                    cursor.copy_expert(sql, f)
                # Commit the transaction to make sure the changes are saved
                conn.commit()
                if not arg["quiet"]:
                    print(f"Data from {csv_file_path} has been copied to {table_name}")

            except Exception as e:
                # If something goes wrong, roll back the transaction
                conn.rollback()
                if not arg["quiet"]:
                    print(f"Error occurred: {e}")

    routines.set_meta_in_data(data, meta)
    return data


def df_to_filelike_to_postgres(data: dict[str, Any]) -> dict[str, Any]:
    """
    Copy a df via a Filelike object into a PostgreSQL table using the COPY command.
    Yaml args:
                'input':            it is a label in "data", which identifies the input data
                                    (given in terms of pandas dataframe),
                                    by default it is the value identified with the label
                                    constants.DEFAULT_IO_DATA_LABEL (if it is a string)
                'db_config':        the key of the database configuration in the config file.
                                    Default is 'postgres'.
                'schema':           the schema in which the table is located. Default is 'public'.
                'table':            the name of the table to which the data will be copied.
                                    This is a required argument.
                'columns_<column_name>_<property>':  column specifications for the table.
                                    The properties can be:
                                    - type: the data type of the column
                                    - min: the minimum precision value allowed for the column if applicable (pptional)
                                    - max: the maximum precision value allowed for the column or the length (optional)
                                    - nullable: indicates whether the column can contain NULL values (optional, default is True)
                                    - default: the default value for the column (optional)
                'quiet':           if True, suppresses output messages. Default is False.

            Returns in data:
                'output':   Not implemented yet!
                            it should be  a label in 'data' which identifies the output
                            (the content of the input pandas dataframe in pandas dataframe),
                            by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    meta = routines.get_meta_data(data)
    arg = {
        "input": constants.DEFAULT_IO_DATA_LABEL,
        "db_config": "postgres",
        "schema": "public",
        "table": "",
        "quiet": False,
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]

    if "output" in arg:
        raise NotImplementedError("output is not implemented yet!")

    db_conf = routines.get_db_config(meta, arg["db_config"])

    table_name = arg["table"]
    db_config = helper.postgres_config_from_url(db_conf.get("url", None), db_conf)

    columns: dict[str, DbColumn] = dict()
    for key, spec in arg.items():
        if key.startswith("columns_"):
            column_key = key[8:]
            # if column_key.endswith("_name"):
            #    column_key = column_key[:-5]
            #    dbcol = columns.get(column_key, DbColumn(name=column_key, type=""))
            #    columns[column_key] = dbcol
            if column_key.endswith("_type"):
                column_key = column_key[:-5]
                dbcol = columns.get(column_key, DbColumn(name=column_key, type=""))
                dbcol.type = spec
                columns[column_key] = dbcol
            elif column_key.endswith("_min"):
                column_key = column_key[:-4]
                dbcol = columns.get(column_key, DbColumn(name=column_key, type=""))
                dbcol.min = int(spec)
                columns[column_key] = dbcol
            elif column_key.endswith("_max"):
                column_key = column_key[:-4]
                dbcol = columns.get(column_key, DbColumn(name=column_key, type=""))
                dbcol.max = int(spec)
                columns[column_key] = dbcol
            elif column_key.endswith("_nullable"):
                column_key = column_key[:-9]
                dbcol = columns.get(column_key, DbColumn(name=column_key, type=""))
                dbcol.nullable = bool(spec)
                columns[column_key] = dbcol
            elif column_key.endswith("_default"):
                column_key = column_key[:-7]
                dbcol = columns.get(column_key, DbColumn(name=column_key, type=""))
                dbcol.default = spec
                columns[column_key] = dbcol
            else:
                raise KeyError(
                    f"Unknown column specification key: {key}. Expected format: 'columns_<column_name>_<property>'."
                )

    temp_csv_obejct = StringIO()
    df = data[arg["input"]]
    df.to_csv(temp_csv_obejct, index=False)
    temp_csv_obejct.seek(0)

    conn = psycopg2.connect(
        host=db_config.host,
        database=db_config.database,
        user=db_config.user,
        password=db_config.password,
        port=db_config.port,
    )

    try:
        with conn:
            if len(columns) > 0:
                helper.create_db_table_if_not_exists(conn, table_name, columns, not arg["quiet"])

                csv_columns = columns.keys()
                # Create a cursor object
                with conn.cursor() as cursor:
                    sql = psycopg2.sql.SQL("COPY {table_name} ({column_name}) FROM STDIN WITH CSV HEADER").format(
                        table_name=psycopg2.sql.Identifier(table_name),
                        column_name=psycopg2.sql.SQL(", ").join(map(psycopg2.sql.Identifier, csv_columns)),
                    )
                    cursor.copy_expert(sql, temp_csv_obejct)

            else:
                # Create a cursor object
                with conn.cursor() as cursor:
                    sql = psycopg2.sql.SQL("COPY {table_name} FROM STDIN WITH CSV HEADER").format(
                        table_name=psycopg2.sql.Identifier(table_name)
                    )
                    cursor.copy_expert(sql, temp_csv_obejct)

            # Commit the transaction to make sure the changes are saved
            conn.commit()
            if not arg["quiet"]:
                print(f"Data from dataframe has been copied to {table_name}")
    except Exception as e:
        # If something goes wrong, roll back the transaction
        conn.rollback()
        if not arg["quiet"]:
            print(f"Error occurred: {e}")

    routines.set_meta_in_data(data, meta)
    return data
