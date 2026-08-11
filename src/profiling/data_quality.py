from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"


def check_referential_integrity(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
) -> None:

    invalid_customers = ~orders["cliente_id"].isin(
        customers["id"]
    )

    invalid_products = ~orders["produto_id"].isin(
        products["id"]
    )

    print("\n" + "=" * 60)
    print("INTEGRIDADE REFERENCIAL")
    print("=" * 60)

    print(
        f"Pedidos com cliente inexistente: "
        f"{invalid_customers.sum():,}"
    )

    print(
        f"Pedidos com produto inexistente: "
        f"{invalid_products.sum():,}"
    )


def check_business_rules(
    products: pd.DataFrame,
    orders: pd.DataFrame,
) -> None:

    print("\n" + "=" * 60)
    print("REGRAS DE NEGÓCIO")
    print("=" * 60)

    invalid_prices = products["preco"] <= 0
    invalid_stock = products["estoque"] < 0
    invalid_quantity = orders["quantidade"] <= 0

    print(
        f"Produtos com preço inválido: "
        f"{invalid_prices.sum():,}"
    )

    print(
        f"Produtos com estoque inválido: "
        f"{invalid_stock.sum():,}"
    )

    print(
        f"Pedidos com quantidade inválida: "
        f"{invalid_quantity.sum():,}"
    )


def main():

    customers = pd.read_csv(
        RAW_DIR / "customers.csv"
    )

    products = pd.read_csv(
        RAW_DIR / "products.csv"
    )

    orders = pd.read_csv(
        RAW_DIR / "orders.csv"
    )

    check_referential_integrity(
        orders,
        customers,
        products,
    )

    check_business_rules(
        products,
        orders,
    )


if __name__ == "__main__":
    main()