'''CUSTOMERS
----------------
Quantidade de registros
Quantidade de colunas
Tipos de dados
Valores nulos
Duplicidades


PRODUCTS
----------------
Quantidade de registros
Quantidade de colunas
Tipos de dados
Valores nulos
Duplicidades


ORDERS
----------------
Quantidade de registros
Quantidade de colunas
Tipos de dados
Valores nulos
Duplicidades'''

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"


def profile_dataframe(name: str, dataframe: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print(f"DATASET: {name}")
    print("=" * 60)

    print(f"Linhas: {len(dataframe):,}")
    print(f"Colunas: {len(dataframe.columns)}")

    print("\nTipos de dados:")
    print(dataframe.dtypes)

    print("\nValores nulos:")
    print(dataframe.isnull().sum())

    print(f"\nRegistros duplicados: {dataframe.duplicated().sum():,}")


def main():
    print("Iniciando Data Profiling...")

    customers = pd.read_csv(
        RAW_DIR / "customers.csv"
    )

    products = pd.read_csv(
        RAW_DIR / "products.csv"
    )

    orders = pd.read_csv(
        RAW_DIR / "orders.csv"
    )

    profile_dataframe(
        "CUSTOMERS",
        customers,
    )

    profile_dataframe(
        "PRODUCTS",
        products,
    )

    profile_dataframe(
        "ORDERS",
        orders,
    )


if __name__ == "__main__":
    main()