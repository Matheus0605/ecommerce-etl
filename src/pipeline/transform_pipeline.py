from pathlib import Path
import os
import logging

from src.extract.csv_extractor import CSVExtractor
from src.transform.customers import CustomerTransformer
from src.transform.products import ProductTransformer
from src.transform.orders import OrderTransformer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data" / "raw")))


def main():

    logger.info("=" * 60)
    logger.info("INICIANDO PIPELINE DE TRANSFORMAÇÃO")
    logger.info("=" * 60)

    extractor = CSVExtractor(RAW_DIR)

    # ----------------------------------------
    # EXTRACT
    # ----------------------------------------

    logger.info("[1/3] Extraindo dados...")

    customers = extractor.extract("customers.csv")

    products = extractor.extract("products.csv")

    orders = extractor.extract("orders.csv")

    logger.info(f"Customers: {len(customers):,}")
    logger.info(f"Products: {len(products):,}")
    logger.info(f"Orders: {len(orders):,}")

    # ----------------------------------------
    # TRANSFORM CUSTOMERS
    # ----------------------------------------

    logger.info("[2/3] Transformando customers...")

    customer_transformer = CustomerTransformer()

    customers_clean, customers_quarantine = (
        customer_transformer.transform(customers)
    )

    logger.info(f"Customers válidos: {len(customers_clean):,}")
    logger.info(f"Customers quarantine: {len(customers_quarantine):,}")

    # ----------------------------------------
    # TRANSFORM PRODUCTS
    # ----------------------------------------

    logger.info("Transformando products...")

    product_transformer = ProductTransformer()

    products_clean, products_quarantine = (
        product_transformer.transform(products)
    )

    logger.info(f"Products válidos: {len(products_clean):,}")
    logger.info(f"Products quarantine: {len(products_quarantine):,}")

    # ----------------------------------------
    # TRANSFORM ORDERS
    # ----------------------------------------

    logger.info("Transformando orders...")

    order_transformer = OrderTransformer()

    orders_clean, orders_quarantine = (
        order_transformer.transform(
            orders,
            customers_clean,
            products_clean,
        )
    )

    logger.info(f"Orders válidos: {len(orders_clean):,}")
    logger.info(f"Orders quarantine: {len(orders_quarantine):,}")

    if not orders_quarantine.empty:

        logger.info("\nMotivos de quarantine:")

        logger.info(
            orders_quarantine["quarantine_reason"].value_counts().to_string()
        )

    logger.info("\n" + "=" * 60)
    logger.info("PIPELINE FINALIZADO")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
