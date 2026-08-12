from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
import os
import logging

logger = logging.getLogger(__name__)


def get_engine() -> Engine:
    """Create SQLAlchemy engine using env vars with sensible defaults."""
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "etl_dw")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    logger.info("Creating engine for %s", url)
    engine = create_engine(url)
    return engine


def load_dataframe(table_name: str, df, engine: Engine = None, if_exists: str = "append"):
    """Load a pandas DataFrame into Postgres using to_sql.

    This is a simple approach suitable for demo / ETL loading. For large volumes
    consider COPY FROM or chunked loads.
    """
    if engine is None:
        engine = get_engine()

    try:
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, method="multi")
        logger.info("Loaded %d rows into %s", len(df), table_name)
    except SQLAlchemyError as exc:
        logger.exception("Failed to load table %s: %s", table_name, exc)
        raise


def execute_sql(sql: str, engine: Engine = None):
    if engine is None:
        engine = get_engine()

    with engine.begin() as conn:
        conn.execute(sql)

