import pandas as pd

from src.transform.customers import CustomerTransformer


def test_should_keep_valid_customers():

    customers = pd.DataFrame(
        {
            "id": [1, 2],
            "nome": ["João", "Maria"],
            "email": [
                "joao@email.com",
                "maria@email.com",
            ],
            "cidade": ["São Paulo", "Santos"],
            "estado": ["SP", "SP"],
            "data_cadastro": [
                "2026-01-01",
                "2026-01-02",
            ],
        }
    )

    transformer = CustomerTransformer()

    clean, quarantine = transformer.transform(
        customers
    )

    assert len(clean) == 2
    assert len(quarantine) == 0


def test_should_quarantine_missing_email():

    customers = pd.DataFrame(
        {
            "id": [1, 2],
            "nome": ["João", "Maria"],
            "email": [
                None,
                "maria@email.com",
            ],
            "cidade": ["São Paulo", "Santos"],
            "estado": ["SP", "SP"],
            "data_cadastro": [
                "2026-01-01",
                "2026-01-02",
            ],
        }
    )

    transformer = CustomerTransformer()

    clean, quarantine = transformer.transform(
        customers
    )

    assert len(clean) == 1
    assert len(quarantine) == 1

    assert quarantine.iloc[0]["id"] == 1
    assert (
        quarantine.iloc[0]["quarantine_reason"]
        == "email_missing"
    )


def test_should_quarantine_duplicate_id():

    customers = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "nome": [
                "João",
                "João Silva",
                "Maria",
            ],
            "email": [
                "joao@email.com",
                "joao2@email.com",
                "maria@email.com",
            ],
            "cidade": [
                "São Paulo",
                "Santos",
                "Campinas",
            ],
            "estado": [
                "SP",
                "SP",
                "SP",
            ],
            "data_cadastro": [
                "2026-01-01",
                "2026-01-03",
                "2026-01-02",
            ],
        }
    )

    transformer = CustomerTransformer()

    clean, quarantine = transformer.transform(
        customers
    )

    assert len(clean) == 2
    assert len(quarantine) == 1

    assert quarantine.iloc[0]["quarantine_reason"] == (
        "duplicate_id"
    )