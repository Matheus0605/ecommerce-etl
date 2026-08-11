import pandas as pd

from src.transform.orders import OrderTransformer


def test_should_calculate_order_total():

    orders = pd.DataFrame(
        {
            "id": [1],
            "cliente_id": [10],
            "produto_id": [100],
            "quantidade": [2],
            "data_pedido": ["2026-08-10"],
            "status": ["aprovado"],
        }
    )

    customers = pd.DataFrame(
        {
            "id": [10],
        }
    )

    products = pd.DataFrame(
        {
            "id": [100],
            "preco": [150.00],
        }
    )

    transformer = OrderTransformer()

    clean, quarantine = transformer.transform(
        orders,
        customers,
        products,
    )

    assert len(clean) == 1
    assert len(quarantine) == 0

    assert clean.iloc[0]["preco_unitario"] == 150.00
    assert clean.iloc[0]["valor_total"] == 300.00


def test_should_quarantine_missing_customer():

    orders = pd.DataFrame(
        {
            "id": [1],
            "cliente_id": [999],
            "produto_id": [100],
            "quantidade": [2],
            "data_pedido": ["2026-08-10"],
            "status": ["aprovado"],
        }
    )

    customers = pd.DataFrame(
        {
            "id": [10],
        }
    )

    products = pd.DataFrame(
        {
            "id": [100],
            "preco": [150.00],
        }
    )

    transformer = OrderTransformer()

    clean, quarantine = transformer.transform(
        orders,
        customers,
        products,
    )

    assert len(clean) == 0
    assert len(quarantine) == 1

    assert (
        quarantine.iloc[0]["quarantine_reason"]
        == "customer_not_found"
    )


def test_should_quarantine_invalid_quantity():

    orders = pd.DataFrame(
        {
            "id": [1],
            "cliente_id": [10],
            "produto_id": [100],
            "quantidade": [0],
            "data_pedido": ["2026-08-10"],
            "status": ["aprovado"],
        }
    )

    customers = pd.DataFrame(
        {
            "id": [10],
        }
    )

    products = pd.DataFrame(
        {
            "id": [100],
            "preco": [150.00],
        }
    )

    transformer = OrderTransformer()

    clean, quarantine = transformer.transform(
        orders,
        customers,
        products,
    )

    assert len(clean) == 0
    assert len(quarantine) == 1

    assert (
        quarantine.iloc[0]["quarantine_reason"]
        == "invalid_quantity"
    )