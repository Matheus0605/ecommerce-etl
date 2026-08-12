from pathlib import Path

from src.extract.csv_extractor import CSVExtractor


def test_extract_customers():

    data_path = Path("data/raw")

    extractor = CSVExtractor(data_path)

    customers = extractor.extract(
        "customers.csv"
    )

    assert len(customers) == 1_000
    assert "id" in customers.columns
    assert "email" in customers.columns