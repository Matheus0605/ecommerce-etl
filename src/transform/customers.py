import pandas as pd


class CustomerTransformer:

    def transform(
        self,
        customers: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:

        df = customers.copy()

        quarantine = []

        # ----------------------------------------
        # Regra 1: email obrigatório
        # ----------------------------------------

        missing_email = df["email"].isna()

        email_quarantine = df.loc[
            missing_email
        ].copy()

        if not email_quarantine.empty:
            email_quarantine[
                "quarantine_reason"
            ] = "email_missing"

            quarantine.append(
                email_quarantine
            )

        df = df.loc[
            ~missing_email
        ].copy()

        # ----------------------------------------
        # Regra 2: ID deve ser único
        # ----------------------------------------

        duplicated_id = df["id"].duplicated(
            keep="first"
        )

        duplicate_quarantine = df.loc[
            duplicated_id
        ].copy()

        if not duplicate_quarantine.empty:
            duplicate_quarantine[
                "quarantine_reason"
            ] = "duplicate_id"

            quarantine.append(
                duplicate_quarantine
            )

        df = df.loc[
            ~duplicated_id
        ].copy()

        # ----------------------------------------
        # Quarantine final
        # ----------------------------------------

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