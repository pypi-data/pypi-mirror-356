import pandas as pd
from uk_public_services_imputation.data import DATA_FOLDER


def validate_input_df(df: pd.DataFrame):
    """
    Validate the input dataframe to ensure it contains all required columns.

    Args:
        df (pd.DataFrame): The input dataframe to validate.
    """
    required_columns = [
        "age",
        "gender",
        "household_weight",
        "region",
        "household_id",
        "is_adult",
        "is_child",
        "is_SP_age",
        "dla",
        "pip",
        "household_count_people",
        "hbai_household_net_income",
        "equiv_hbai_household_net_income",
        "count_primary_education",
        "count_secondary_education",
        "count_further_education",
    ]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Required column '{col}' missing from input dataframe"
            )
    return df


def impute_public_services(df: pd.DataFrame):
    """
    Impute public services based on the input dataframe.

    Args:
        df (pd.DataFrame): The input dataframe containing demographic data.

    Returns:
        pd.DataFrame: The dataframe with imputed public services data.
    """
    df.to_csv(DATA_FOLDER / "data.csv", index=False)
    # Import here to avoid circular imports
    from uk_public_services_imputation.nhs.impute_nhs_consumption import (
        main as nhs_main,
    )

    nhs_main()

    from uk_public_services_imputation.etb.impute_services import (
        main as etb_main,
    )

    etb_main()

    return pd.read_csv(DATA_FOLDER / "data.csv")
