from pathlib import Path
import os
import json
try:
    from prefect import flow, task
    _PREFECT_AVAILABLE = True
except Exception:
    # Prefect not available or incompatible in this environment — fallback to
    # no-op decorators so the script can run synchronously without Prefect.
    _PREFECT_AVAILABLE = False

    def task(fn=None, **kwargs):
        if fn is None:
            def _decorator(f):
                return f
            return _decorator
        return fn

    def flow(fn=None, **kwargs):
        if fn is None:
            def _decorator(f):
                return f
            return _decorator
        return fn
from src.utils.logging_config import configure_logging
import logging
from src.extract.csv_extractor import CSVExtractor
from src.transform.customers import CustomerTransformer
from src.transform.products import ProductTransformer
from src.transform.orders import OrderTransformer
from src.load.postgres_loader import get_engine, load_dataframe
from src.models.dim_models import create_all_tables

configure_logging()
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data" / "raw")))
SILVER_DIR = Path(os.getenv("SILVER_DIR", str(BASE_DIR / "data" / "silver")))
GOLD_DIR = Path(os.getenv("GOLD_DIR", str(BASE_DIR / "data" / "gold")))
METRICS_DIR = Path(os.getenv("METRICS_DIR", str(BASE_DIR / "data" / "metrics")))


@task
def extract_task():
    extractor = CSVExtractor(RAW_DIR)
    customers = extractor.extract("customers.csv")
    products = extractor.extract("products.csv")
    orders = extractor.extract("orders.csv")
    return customers, products, orders


@task
def transform_task(customers, products, orders):
    # Customers
    customer_transformer = CustomerTransformer()
    customers_clean, customers_quarantine = customer_transformer.transform(customers)

    # Products
    product_transformer = ProductTransformer()
    products_clean, products_quarantine = product_transformer.transform(products)

    # Orders
    order_transformer = OrderTransformer()
    orders_clean, orders_quarantine = order_transformer.transform(orders, customers_clean, products_clean)

    return {
        "customers_clean": customers_clean,
        "customers_quarantine": customers_quarantine,
        "products_clean": products_clean,
        "products_quarantine": products_quarantine,
        "orders_clean": orders_clean,
        "orders_quarantine": orders_quarantine,
    }


@task
def write_silver_task(artifacts: dict):
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    artifacts["customers_clean"].to_parquet(SILVER_DIR / "customers.parquet", index=False)
    artifacts["products_clean"].to_parquet(SILVER_DIR / "products.parquet", index=False)
    artifacts["orders_clean"].to_parquet(SILVER_DIR / "orders.parquet", index=False)
    return True


@task
def create_dim_and_load_task(artifacts: dict):
    try:
        engine = get_engine()
        # create tables if not exist
        create_all_tables(engine)

        # load dimension tables and fact table
        # for dims we convert column names accordingly
        dim_customers = artifacts["customers_clean"].rename(columns={"id": "customer_id"})
        dim_products = artifacts["products_clean"].rename(columns={"id": "product_id", "preco": "price"})

        fact_orders = artifacts["orders_clean"].rename(
            columns={"id": "order_id", "cliente_id": "customer_id", "produto_id": "product_id", "quantidade": "quantity", "preco_unitario": "unit_price", "valor_total": "total_price", "data_pedido": "order_date"}
        )

        # write dims (replace for idempotency)
        load_dataframe("dim_customers", dim_customers, engine=engine, if_exists="replace")
        load_dataframe("dim_products", dim_products, engine=engine, if_exists="replace")
        load_dataframe("fact_orders", fact_orders, engine=engine, if_exists="replace")

        return True

    except Exception as exc:
        # Likely the database is not available — log and continue so the ETL
        # can run end-to-end for local testing without a Postgres instance.
        logger.warning("Skipping Postgres load due to error: %s", exc)
        return False


@task
def write_metrics_task(artifacts: dict):
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    metrics = {
        "customers_total": len(artifacts["customers_clean"]) + len(artifacts["customers_quarantine"]),
        "customers_valid": len(artifacts["customers_clean"]),
        "customers_quarantine": len(artifacts["customers_quarantine"]),
        "products_total": len(artifacts["products_clean"]) + len(artifacts["products_quarantine"]),
        "products_valid": len(artifacts["products_clean"]),
        "products_quarantine": len(artifacts["products_quarantine"]),
        "orders_total": len(artifacts["orders_clean"]) + len(artifacts["orders_quarantine"]),
        "orders_valid": len(artifacts["orders_clean"]),
        "orders_quarantine": len(artifacts["orders_quarantine"]),
    }

    metrics_path = METRICS_DIR / "quality_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    logger.info("Wrote metrics to %s", metrics_path)
    return metrics_path


@flow
def etl_flow():
    logger.info("Starting ETL flow")
    customers, products, orders = extract_task()
    artifacts = transform_task(customers, products, orders)
    write_silver_task(artifacts)
    create_dim_and_load_task(artifacts)
    metrics_path = write_metrics_task(artifacts)
    logger.info("ETL flow finished, metrics at %s", metrics_path)


if __name__ == "__main__":
    etl_flow()
