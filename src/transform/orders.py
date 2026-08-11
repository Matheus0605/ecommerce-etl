import pandas as pd


class OrderTransformer:

    def transform(
        self,
        orders: pd.DataFrame,
        customers: pd.DataFrame,
        products: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:

        df = orders.copy()

        quarantine = []

        # ----------------------------------------
        # Regra 1: cliente deve existir
        # ----------------------------------------

        valid_customers = set(
            customers["id"]
        )

        invalid_customer = ~df[
            "cliente_id"
        ].isin(valid_customers)

        customer_quarantine = df.loc[
            invalid_customer
        ].copy()

        if not customer_quarantine.empty:

            customer_quarantine[
                "quarantine_reason"
            ] = "customer_not_found"

            quarantine.append(
                customer_quarantine
            )

        df = df.loc[
            ~invalid_customer
        ].copy()

        # ----------------------------------------
        # Regra 2: quantidade > 0
        # ----------------------------------------

        invalid_quantity = (
            df["quantidade"] <= 0
        )

        quantity_quarantine = df.loc[
            invalid_quantity
        ].copy()

        if not quantity_quarantine.empty:

            quantity_quarantine[
                "quarantine_reason"
            ] = "invalid_quantity"

            quarantine.append(
                quantity_quarantine
            )

        df = df.loc[
            ~invalid_quantity
        ].copy()

        # ----------------------------------------
        # Regra 3: produto deve existir
        # ----------------------------------------

        product_prices = products[
            ["id", "preco"]
        ]

        df = df.merge(
            product_prices,
            left_on="produto_id",
            right_on="id",
            how="left",
            suffixes=("", "_produto"),
        )

        invalid_product = df[
            "preco"
        ].isna()

        product_quarantine = df.loc[
            invalid_product
        ].copy()

        if not product_quarantine.empty:

            product_quarantine[
                "quarantine_reason"
            ] = "product_not_found"

            quarantine.append(
                product_quarantine
            )

        df = df.loc[
            ~invalid_product
        ].copy()

        # ----------------------------------------
        # Calcular valor total
        # ----------------------------------------

        df["preco_unitario"] = df["preco"]

        df["valor_total"] = (
            df["quantidade"]
            * df["preco_unitario"]
        )

        df = df.drop(
            columns=["preco"]
        )

        # ----------------------------------------
        # Quarantine final
        # ----------------------------------------

        if quarantine:

            quarantine_df = pd.concat(
                quarantine,
                ignore_index=True,
            )

        else:

            quarantine_df = pd.DataFrame()

        return df, quarantine_df