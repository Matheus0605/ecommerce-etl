from pathlib import Path

import pandas as pd


class CSVExtractor:

    def __init__(self, data_path: Path):
        self.data_path = data_path

    def extract(self, filename: str) -> pd.DataFrame:
        file_path = self.data_path / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {file_path}"
            )

        return pd.read_csv(file_path)