from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"


def inject_customer_errors() -> None:
    path = RAW_DIR / "customers.csv"

    customers = pd.read_csv(path)

    # 50 clientes terão e-mail nulo
    customers.loc[
        customers.sample(50, random_state=42).index,
        "email",
    ] = None

    # 20 clientes serão duplicados
    duplicates = customers.sample(
        20,
        random_state=42,
    )

    customers = pd.concat(
        [customers, duplicates],
        ignore_index=True,
    )

    customers.to_csv(
        path,
        index=False,
    )

    print("Problemas inseridos em customers.csv")


def inject_product_errors() -> None:
    path = RAW_DIR / "products.csv"

    products = pd.read_csv(path)

    # 50 produtos terão preço inválido
    products.loc[
        products.sample(50, random_state=42).index,
        "preco",
    ] = -10

    # 50 produtos terão estoque inválido
    products.loc[
        products.sample(50, random_state=99).index,
        "estoque",
    ] = -5

    products.to_csv(
        path,
        index=False,
    )

    print("Problemas inseridos em products.csv")


def inject_order_errors() -> None:
    path = RAW_DIR / "orders.csv"

    orders = pd.read_csv(path)

    # 100 pedidos terão quantidade inválida
    orders.loc[
        orders.sample(100, random_state=42).index,
        "quantidade",
    ] = 0

    # 100 pedidos terão cliente inexistente
    orders.loc[
        orders.sample(100, random_state=99).index,
        "cliente_id",
    ] = 999999

    orders.to_csv(
        path,
        index=False,
    )

    print("Problemas inseridos em orders.csv")


def main():
    inject_customer_errors()
    inject_product_errors()
    inject_order_errors()

    print("\nDados inconsistentes inseridos com sucesso.")


if __name__ == "__main__":
    main()