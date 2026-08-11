from pathlib import Path
import random

import pandas as pd
from faker import Faker


fake = Faker("pt_BR")

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"


def generate_customers(quantity: int) -> pd.DataFrame:
    customers = []

    for customer_id in range(1, quantity + 1):
        customers.append(
            {
                "id": customer_id,
                "nome": fake.name(),
                "email": fake.email(),
                "cidade": fake.city(),
                "estado": fake.estado_sigla(),
                "data_cadastro": fake.date_between(
                    start_date="-2y",
                    end_date="today",
                ),
            }
        )

    return pd.DataFrame(customers)


def generate_products(quantity: int) -> pd.DataFrame:
    categories = [
        "Eletrônicos",
        "Informática",
        "Celulares",
        "Casa",
        "Esportes",
        "Moda",
        "Livros",
    ]

    products = []

    for product_id in range(1, quantity + 1):
        products.append(
            {
                "id": product_id,
                "nome": fake.catch_phrase(),
                "categoria": random.choice(categories),
                "preco": round(random.uniform(20, 5000), 2),
                "estoque": random.randint(0, 500),
            }
        )

    return pd.DataFrame(products)


def generate_orders(
    quantity: int,
    customer_quantity: int,
    product_quantity: int,
) -> pd.DataFrame:

    statuses = [
        "aprovado",
        "cancelado",
        "processando",
        "enviado",
        "entregue",
    ]

    orders = []

    for order_id in range(1, quantity + 1):
        orders.append(
            {
                "id": order_id,
                "cliente_id": random.randint(
                    1,
                    customer_quantity,
                ),
                "produto_id": random.randint(
                    1,
                    product_quantity,
                ),
                "quantidade": random.randint(1, 5),
                "data_pedido": fake.date_between(
                    start_date="-1y",
                    end_date="today",
                ),
                "status": random.choice(statuses),
            }
        )

    return pd.DataFrame(orders)


def main():
    print("Iniciando geração dos dados...")

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    customer_quantity = 10_000
    product_quantity = 50_000
    order_quantity = 1_000_000

    customers = generate_customers(customer_quantity)

    products = generate_products(product_quantity)

    orders = generate_orders(
        order_quantity,
        customer_quantity,
        product_quantity,
    )

    customers.to_csv(
        RAW_DIR / "customers.csv",
        index=False,
    )

    products.to_csv(
        RAW_DIR / "products.csv",
        index=False,
    )

    orders.to_csv(
        RAW_DIR / "orders.csv",
        index=False,
    )

    print("Dados gerados com sucesso!")
    print(f"Clientes: {len(customers):,}")
    print(f"Produtos: {len(products):,}")
    print(f"Pedidos: {len(orders):,}")


if __name__ == "__main__":
    main()