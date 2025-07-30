from policyengine_uk import Microsimulation
import pandas as pd
from uk_public_services_imputation.data import DATA_FOLDER

folder = DATA_FOLDER


def create_efrs_input_dataset():
    sim = Microsimulation(
        dataset="hf://policyengine/policyengine-uk-data/enhanced_frs_2022_23.h5"
    )

    variables = [
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
    ]
    education = sim.calculate("current_education")

    df = sim.calculate_dataframe(variables)

    df["count_primary_education"] = education == "PRIMARY"
    df["count_secondary_education"] = education == "LOWER_SECONDARY"
    df["count_further_education"] = education.isin(
        ["UPPER_SECONDARY", "TERTIARY"]
    )
    df["hbai_household_net_income"] = (
        df["hbai_household_net_income"] / df["household_count_people"]
    )
    df["equiv_hbai_household_net_income"] = (
        df["equiv_hbai_household_net_income"] / df["household_count_people"]
    )

    data = pd.DataFrame(df)
    data.to_csv(folder / "data.csv", index=False)
    return data
