import os
import random
import string
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from contextlib import suppress
from pathlib import Path

from amsdal_utils.config.data_models.amsdal_config import AmsdalConfig
from amsdal_utils.config.data_models.connection_config import ConnectionConfig
from amsdal_utils.config.data_models.repository_config import RepositoryConfig
from amsdal_utils.config.data_models.resources_config import ResourcesConfig
from amsdal_utils.config.manager import AmsdalConfigManager

from amsdal_data.aliases.db import POSTGRES_HISTORICAL_ALIAS
from amsdal_data.aliases.db import POSTGRES_HISTORICAL_ASYNC_ALIAS
from amsdal_data.aliases.db import POSTGRES_STATE_ALIAS
from amsdal_data.aliases.db import POSTGRES_STATE_ASYNC_ALIAS
from amsdal_data.aliases.db import SQLITE_ALIAS
from amsdal_data.aliases.db import SQLITE_HISTORICAL_ALIAS
from amsdal_data.aliases.db import SQLITE_HISTORICAL_ASYNC_ALIAS
from amsdal_data.aliases.db import SQLITE_STATE_ASYNC_ALIAS
from amsdal_data.connections.db_alias_map import CONNECTION_BACKEND_ALIASES

PG_TEST_HOST = os.getenv('PG_TEST_HOST', '127.0.0.1')
PG_TEST_PORT = os.getenv('PG_TEST_PORT', '5432')
PG_TEST_USER = os.getenv('PG_TEST_USER', 'postgres')
PG_TEST_PASSWORD = os.getenv('PG_TEST_PASSWORD', 'example')


def build_config(
    lakehouse_backend: str,
    lakehouse_credentials: dict[str, str],
    state_backend: str | None = None,
    state_credentials: dict[str, str] | None = None,
    *,
    is_async_mode: bool = False,
) -> AmsdalConfig:
    connections = {
        'lakehouse': ConnectionConfig(
            name='lakehouse',
            backend=lakehouse_backend,
            credentials=lakehouse_credentials,
        ),
    }

    if state_backend and state_credentials is not None:
        connections['state'] = ConnectionConfig(
            name='state',
            backend=state_backend,
            credentials=state_credentials,
        )

    return AmsdalConfig(
        application_name='local',
        async_mode=is_async_mode,
        connections=connections,
        resources_config=ResourcesConfig(
            lakehouse='lakehouse',
            lock='lakehouse',
            repository=RepositoryConfig(
                default='state' if state_backend else 'lakehouse',
            ),
        ),
    )


def create_postgres_database(database: str) -> None:
    import psycopg

    conn = psycopg.connect(
        host=PG_TEST_HOST,
        port=PG_TEST_PORT,
        user=PG_TEST_USER,
        password=PG_TEST_PASSWORD,
        autocommit=True,
    )
    cur = conn.cursor()

    with suppress(psycopg.errors.DuplicateDatabase):
        cur.execute(f'CREATE DATABASE "{database}"')

    cur.close()
    conn.close()


def drop_postgres_database(database: str) -> None:
    import psycopg

    conn = psycopg.connect(
        host=PG_TEST_HOST,
        port=PG_TEST_PORT,
        user=PG_TEST_USER,
        password=PG_TEST_PASSWORD,
        autocommit=True,
    )
    cur = conn.cursor()

    with suppress(psycopg.errors.DuplicateDatabase):
        cur.execute(f'DROP DATABASE "{database}"')

    cur.close()
    conn.close()


@contextmanager
def temp_dir(*, use_temp_dir: bool = True) -> Iterator[str]:
    tmp_dir = None

    if use_temp_dir:
        tmp_dir = '.tmp'
        Path(tmp_dir).mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(dir=tmp_dir) as directory:
        yield directory


@contextmanager
def sqlite_lakehouse_only_config() -> Iterator[AmsdalConfig]:
    with temp_dir() as tmp_dir:
        config = build_config(
            lakehouse_backend=CONNECTION_BACKEND_ALIASES[SQLITE_HISTORICAL_ALIAS],
            lakehouse_credentials={
                'db_path': f'{tmp_dir}/amsdal_historical.sqlite3',
            },
        )
        AmsdalConfigManager().set_config(config)

        try:
            yield config
        finally:
            AmsdalConfigManager.invalidate()


@contextmanager
def sqlite_async_lakehouse_only_config() -> Iterator[AmsdalConfig]:
    with temp_dir() as tmp_dir:
        config = build_config(
            lakehouse_backend=CONNECTION_BACKEND_ALIASES[SQLITE_HISTORICAL_ASYNC_ALIAS],
            lakehouse_credentials={
                'db_path': f'{tmp_dir}/amsdal_historical.sqlite3',
            },
            is_async_mode=True,
        )
        AmsdalConfigManager().set_config(config)

        try:
            yield config
        finally:
            AmsdalConfigManager.invalidate()


@contextmanager
def sqlite_config() -> Iterator[AmsdalConfig]:
    with temp_dir() as tmp_dir:
        config = build_config(
            lakehouse_backend=CONNECTION_BACKEND_ALIASES[SQLITE_HISTORICAL_ALIAS],
            lakehouse_credentials={
                'db_path': f'{tmp_dir}/amsdal_historical.sqlite3',
            },
            state_backend=CONNECTION_BACKEND_ALIASES[SQLITE_ALIAS],
            state_credentials={
                'db_path': f'{tmp_dir}/amsdal_state.sqlite3',
            },
        )
        AmsdalConfigManager().set_config(config)

        try:
            yield config
        finally:
            AmsdalConfigManager.invalidate()


@contextmanager
def sqlite_async_config() -> Iterator[AmsdalConfig]:
    with temp_dir() as tmp_dir:
        config = build_config(
            lakehouse_backend=CONNECTION_BACKEND_ALIASES[SQLITE_HISTORICAL_ASYNC_ALIAS],
            lakehouse_credentials={
                'db_path': f'{tmp_dir}/amsdal_historical.sqlite3',
            },
            state_backend=CONNECTION_BACKEND_ALIASES[SQLITE_STATE_ASYNC_ALIAS],
            state_credentials={
                'db_path': f'{tmp_dir}/amsdal_state.sqlite3',
            },
            is_async_mode=True,
        )
        AmsdalConfigManager().set_config(config)

        try:
            yield config
        finally:
            AmsdalConfigManager.invalidate()


@contextmanager
def postgres_config() -> Iterator[AmsdalConfig]:
    lakehouse_database = ''.join(random.sample(string.ascii_letters, 16))
    state_database = ''.join(random.sample(string.ascii_letters, 16))

    config = build_config(
        lakehouse_backend=CONNECTION_BACKEND_ALIASES[POSTGRES_HISTORICAL_ALIAS],
        lakehouse_credentials={
            'dsn': f'postgresql://{PG_TEST_USER}:{PG_TEST_PASSWORD}@{PG_TEST_HOST}:{PG_TEST_PORT}/{lakehouse_database}',
        },
        state_backend=CONNECTION_BACKEND_ALIASES[POSTGRES_STATE_ALIAS],
        state_credentials={
            'dsn': f'postgresql://{PG_TEST_USER}:{PG_TEST_PASSWORD}@{PG_TEST_HOST}:{PG_TEST_PORT}/{state_database}',
        },
    )
    AmsdalConfigManager().set_config(config)
    create_postgres_database(lakehouse_database)
    create_postgres_database(state_database)

    try:
        yield config
    finally:
        AmsdalConfigManager.invalidate()
        drop_postgres_database(lakehouse_database)
        drop_postgres_database(state_database)


@contextmanager
def postgres_async_config() -> Iterator[AmsdalConfig]:
    lakehouse_database = ''.join(random.sample(string.ascii_letters, 16))
    state_database = ''.join(random.sample(string.ascii_letters, 16))

    config = build_config(
        lakehouse_backend=CONNECTION_BACKEND_ALIASES[POSTGRES_HISTORICAL_ASYNC_ALIAS],
        lakehouse_credentials={
            'dsn': f'postgresql://{PG_TEST_USER}:{PG_TEST_PASSWORD}@{PG_TEST_HOST}:{PG_TEST_PORT}/{lakehouse_database}',
        },
        state_backend=CONNECTION_BACKEND_ALIASES[POSTGRES_STATE_ASYNC_ALIAS],
        state_credentials={
            'dsn': f'postgresql://{PG_TEST_USER}:{PG_TEST_PASSWORD}@{PG_TEST_HOST}:{PG_TEST_PORT}/{state_database}',
        },
        is_async_mode=True,
    )
    AmsdalConfigManager().set_config(config)
    create_postgres_database(lakehouse_database)
    create_postgres_database(state_database)

    try:
        yield config
    finally:
        AmsdalConfigManager.invalidate()
        drop_postgres_database(lakehouse_database)
        drop_postgres_database(state_database)
