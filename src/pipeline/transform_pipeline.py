from pathlib import Path

from src.extract.csv_extractor import CSVExtractor
from src.transform.customers import CustomerTransformer
from src.transform.products import ProductTransformer
from src.transform.orders import OrderTransformer


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"


def main():

    print("=" * 60)
    print("INICIANDO PIPELINE DE TRANSFORMAÇÃO")
    print("=" * 60)

    extractor = CSVExtractor(RAW_DIR)

    # ----------------------------------------
    # EXTRACT
    # ----------------------------------------

    print("\n[1/3] Extraindo dados...")

    customers = extractor.extract(
        "customers.csv"
    )

    products = extractor.extract(
        "products.csv"
    )

    orders = extractor.extract(
        "orders.csv"
    )

    print(
        f"Customers: {len(customers):,}"
    )

    print(
        f"Products: {len(products):,}"
    )

    print(
        f"Orders: {len(orders):,}"
    )

    # ----------------------------------------
    # TRANSFORM CUSTOMERS
    # ----------------------------------------

    print("\n[2/3] Transformando customers...")

    customer_transformer = CustomerTransformer()

    customers_clean, customers_quarantine = (
        customer_transformer.transform(
            customers
        )
    )

    print(
        f"Customers válidos: "
        f"{len(customers_clean):,}"
    )

    print(
        f"Customers quarantine: "
        f"{len(customers_quarantine):,}"
    )

    # ----------------------------------------
    # TRANSFORM PRODUCTS
    # ----------------------------------------

    print("\nTransformando products...")

    product_transformer = ProductTransformer()

    products_clean, products_quarantine = (
        product_transformer.transform(
            products
        )
    )

    print(
        f"Products válidos: "
        f"{len(products_clean):,}"
    )

    print(
        f"Products quarantine: "
        f"{len(products_quarantine):,}"
    )

    # ----------------------------------------
    # TRANSFORM ORDERS
    # ----------------------------------------

    print("\nTransformando orders...")

    order_transformer = OrderTransformer()

    orders_clean, orders_quarantine = (
        order_transformer.transform(
            orders,
            customers_clean,
            products_clean,
        )
    )

    print(
        f"Orders válidos: "
        f"{len(orders_clean):,}"
    )

    print(
        f"Orders quarantine: "
        f"{len(orders_quarantine):,}"
    )

    if not orders_quarantine.empty:

        print("\nMotivos de quarantine:")

        print(
            orders_quarantine[
                "quarantine_reason"
            ]
            .value_counts()
            .to_string()
        )

    print("\n" + "=" * 60)
    print("PIPELINE FINALIZADO")
    print("=" * 60)


if __name__ == "__main__":
    main()