import pandas as pd

from src.transform.products import ProductTransformer


def test_should_keep_valid_products():

    products = pd.DataFrame(
        {
            "id": [1, 2],
            "nome": ["Notebook", "Mouse"],
            "categoria": ["Informática", "Informática"],
            "preco": [3500.00, 100.00],
            "estoque": [10, 50],
        }
    )

    transformer = ProductTransformer()

    clean, quarantine = transformer.transform(
        products
    )

    assert len(clean) == 2
    assert len(quarantine) == 0


def test_should_quarantine_invalid_price():

    products = pd.DataFrame(
        {
            "id": [1, 2],
            "nome": ["Notebook", "Mouse"],
            "categoria": ["Informática", "Informática"],
            "preco": [-100.00, 100.00],
            "estoque": [10, 50],
        }
    )

    transformer = ProductTransformer()

    clean, quarantine = transformer.transform(
        products
    )

    assert len(clean) == 1
    assert len(quarantine) == 1

    assert quarantine.iloc[0]["id"] == 1
    assert (
        quarantine.iloc[0]["quarantine_reason"]
        == "invalid_price"
    )


def test_should_quarantine_invalid_stock():

    products = pd.DataFrame(
        {
            "id": [1, 2],
            "nome": ["Notebook", "Mouse"],
            "categoria": ["Informática", "Informática"],
            "preco": [3500.00, 100.00],
            "estoque": [-5, 50],
        }
    )

    transformer = ProductTransformer()

    clean, quarantine = transformer.transform(
        products
    )

    assert len(clean) == 1
    assert len(quarantine) == 1

    assert quarantine.iloc[0]["id"] == 1
    assert (
        quarantine.iloc[0]["quarantine_reason"]
        == "invalid_stock"
    )