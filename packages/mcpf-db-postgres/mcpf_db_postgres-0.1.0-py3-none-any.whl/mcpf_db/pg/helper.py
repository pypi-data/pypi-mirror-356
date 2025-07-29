from typing import Any, Optional

import psycopg2.sql as sql
from mcpf_db.db.types import DbColumn, DbConfig
from sqlalchemy.engine import make_url
from sqlalchemy.engine.url import URL


def _get_value_from_dict(d: Optional[dict[str, Any]], key: str, default: Any = None) -> Any:
    """
    Retrieves a value from a dictionary using a specified key.

    Args:
        d (dict): The dictionary to search. Can be None.
        key (str): The key to look for in the dictionary.
        default (Any): The default value to return if the key is not found or the value is None. Defaults to None.

    Returns:
        Any: The value associated with the key, or the default value if the key is not found or the value is None.
    """
    return d[key] if d is not None and key in d and d[key] is not None else default


def postgres_config_from_url(
    url: Optional[str] = None, db_config_overrides: Optional[dict[str, Any]] = None
) -> DbConfig:
    """
    Converts a PostgreSQL connection URL into a DbConfig object.

    This function parses the given PostgreSQL connection URL and constructs
    a DbConfig object containing the connection details. Optionally, specific
    connection parameters can be overridden using the `db_config_overrides` dictionary.

    Args:
        url (str): The PostgreSQL connection URL to parse. (Optional)
        db_config_overrides (Optional[dict[str, Any]]): A dictionary of overrides for
            specific connection parameters. Supported keys are:
            - "driver": Overrides the driver name.
            - "host": Overrides the host value.
            - "database": Overrides the database name.
            - "user": Overrides the username.
            - "password": Overrides the password.
            - "port": Overrides the port number.

    Returns:
        DbConfig: An object containing the parsed and overridden connection details.

    Raises:
        ValueError: If the provided URL is invalid or cannot be parsed.
    """

    parsed_url = make_url(url) if url is not None else URL.create("")
    db_config = DbConfig(
        driver=_get_value_from_dict(db_config_overrides, "driver", parsed_url.drivername),
        host=_get_value_from_dict(db_config_overrides, "host", parsed_url.host),
        database=_get_value_from_dict(db_config_overrides, "database", parsed_url.database),
        user=_get_value_from_dict(db_config_overrides, "user", parsed_url.username),
        password=_get_value_from_dict(db_config_overrides, "password", parsed_url.password),
        port=_get_value_from_dict(db_config_overrides, "port", parsed_url.port),
    )
    return db_config


def postgres_update_url_from_config(url: Optional[str], db_config: DbConfig) -> str:
    """
    Updates a PostgreSQL connection URL with the provided DbConfig object.

    This function takes a PostgreSQL connection URL and a DbConfig object,
    and updates the URL with the connection details from the DbConfig.

    Args:
        url (str): The PostgreSQL connection URL to update. If omitted, a new URL will be created.
        db_config (DbConfig): The DbConfig object containing the connection details.

    Returns:
        str: The updated PostgreSQL connection URL.
    """
    parsed_url = make_url(url) if url else URL.create(db_config.driver)
    updated_url = parsed_url.set(
        drivername=db_config.driver,
        host=db_config.host,
        database=db_config.database,
        username=db_config.user,
        password=db_config.password,
        port=db_config.port,
    )
    return str(updated_url)


def column_to_sql(column: DbColumn) -> sql.SQL:
    """
    Convert a DbColumn object to a SQL representation.

    Args:
        column (DbColumn): The DbColumn object to convert.

    Returns:
        sql.SQL: A SQL representation of the column.
    """
    column_sql = sql.SQL("{} {}").format(sql.Identifier(column.name), sql.Identifier(column.type))
    if column.min is not None and column.max is not None:
        column_sql += sql.SQL("({},{})").format(sql.Literal(column.min), sql.Literal(column.max))
    elif column.max is not None:
        column_sql += sql.SQL("({})").format(sql.Literal(column.max))
    elif column.min is not None:
        column_sql += sql.SQL("({},)").format(sql.Literal(column.min))
    if not column.nullable:
        column_sql += sql.SQL(" NOT NULL")
    if column.default is not None:
        column_sql += sql.SQL(" DEFAULT {}").format(sql.Literal(column.default))
    return column_sql


def create_db_table_if_not_exists(conn, table_name: str, columns: dict[str, DbColumn], verbose: bool = False) -> None:
    """Creates database table if not exists

    Args:

    Returns:
    """

    datastructure = sql.SQL(",").join([column_to_sql(column) for column in columns.values()])

    try:
        cursor = conn.cursor()
        q = sql.SQL("SELECT COUNT(*) FROM information_schema.tables where table_name = {table_name};").format(
            table_name=sql.Literal(table_name),
        )
        cursor.execute(q, table_name)
        if cursor.fetchone()[0] == 0:
            if verbose:
                print("Creating Table...")
            q = sql.SQL("CREATE TABLE {table_name} ({datastructure});").format(
                table_name=sql.Identifier(table_name), datastructure=datastructure
            )
            cursor.execute(q)
        else:
            if verbose:
                print("Table already exists.")
        conn.commit()
    finally:
        cursor.close()
