import pandas as pd


class ProductTransformer:

    def transform(
        self,
        products: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:

        df = products.copy()

        quarantine = []

        # -----------------------------
        # Regra 1: preço deve ser > 0
        # -----------------------------

        invalid_price = df["preco"] <= 0

        price_quarantine = df.loc[
            invalid_price
        ].copy()

        if not price_quarantine.empty:
            price_quarantine[
                "quarantine_reason"
            ] = "invalid_price"

            quarantine.append(
                price_quarantine
            )

        df = df.loc[
            ~invalid_price
        ].copy()

        # -----------------------------
        # Regra 2: estoque >= 0
        # -----------------------------

        invalid_stock = df["estoque"] < 0

        stock_quarantine = df.loc[
            invalid_stock
        ].copy()

        if not stock_quarantine.empty:
            stock_quarantine[
                "quarantine_reason"
            ] = "invalid_stock"

            quarantine.append(
                stock_quarantine
            )

        df = df.loc[
            ~invalid_stock
        ].copy()

        # -----------------------------
        # Quarantine
        # -----------------------------

        if quarantine:

            quarantine_df = pd.concat(
                quarantine,
                ignore_index=True,
            )

        else:

            quarantine_df = pd.DataFrame(
                columns=[
                    *df.columns,
                    "quarantine_reason",
                ]
            )

        return df, quarantine_df