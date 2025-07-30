import pandas as pd
import numpy as np
import logging
from uk_public_services_imputation.input_data import create_efrs_input_dataset

from uk_public_services_imputation.data import DATA_FOLDER

folder = DATA_FOLDER


def create_nhs_usage_data(efrs: pd.DataFrame):
    # First, read the data

    nhs = pd.read_csv(folder / "nhs_consumption_by_age_gender.csv")

    # Clean age bounds

    def get_age_bounds(age_group: str):
        if age_group == "0 years":
            return 0, 1
        if age_group == "95 years or older":
            return 95, 120

        if "-" in age_group:
            lower, upper = age_group[:5].split("-")
            lower = int(lower.strip())
            upper = int(upper.strip())
            return lower, upper + 1

    nhs["Lower age"] = nhs["Age group"].apply(lambda x: get_age_bounds(x)[0])
    nhs["Upper age"] = nhs["Age group"].apply(lambda x: get_age_bounds(x)[1])

    nhs = nhs.drop(columns=["Age group"])

    index_cols = ["Lower age", "Upper age", "Gender", "Service"]

    # Get counts and total costs as columns
    nhs = nhs.pivot(
        index=index_cols,
        columns="Metric",
        values="Total",
    )

    # Roll 80+ into 80-85

    nhs = nhs.reset_index()

    over_80_values = (
        nhs[nhs["Lower age"] == 80].set_index(["Gender", "Service"])
        + nhs[nhs["Lower age"] > 80].groupby(["Gender", "Service"]).sum()
    ).reset_index()

    nhs[nhs["Lower age"] == 80][["Activity Count", "Total Cost"]] = (
        over_80_values[["Activity Count", "Total Cost"]]
    )
    nhs = nhs[nhs["Lower age"] <= 80]
    nhs[nhs["Lower age"] == 80]["Upper age"] = 120

    nhs["Spending per unit"] = nhs["Total Cost"] / nhs["Activity Count"]

    # Now add total number in demographic groups using PE

    nhs["Total people"] = np.ones_like(nhs["Total Cost"])

    for i in range(len(nhs)):
        row = nhs.iloc[i]
        count = efrs[efrs.age.between(row["Lower age"], row["Upper age"] - 1)][
            efrs.gender == row.Gender.upper()
        ].household_weight.values.sum()
        nhs.loc[i, "Total people"] = count

    nhs["Per-person average units"] = (
        nhs["Activity Count"] / nhs["Total people"]
    )
    nhs["Per-person average spending"] = (
        nhs["Total Cost"] / nhs["Total people"]
    )
    indirect_cost_adjustment_factor = (
        202e9 / nhs["Total Cost"].sum()
    )  # £202 billion 2025/26 budget

    nhs["Per-person average spending"] *= indirect_cost_adjustment_factor

    return nhs.pivot(
        index=["Lower age", "Upper age", "Gender"],
        columns="Service",
        values=["Per-person average units", "Per-person average spending"],
    ).reset_index()


def impute_nhs_usage(efrs: pd.DataFrame):
    nhs_usage = create_nhs_usage_data(efrs)
    visit_variables = [
        "a_and_e_visits",
        "admitted_patient_visits",
        "outpatient_visits",
    ]
    spending_variables = [
        "nhs_a_and_e_spending",
        "nhs_admitted_patient_spending",
        "nhs_outpatient_spending",
    ]

    variables = visit_variables + spending_variables

    for i, row in nhs_usage.iterrows():
        selection = efrs.age.between(row.values[0], row.values[1]) & (
            efrs.gender == row.values[2].upper()
        )
        for j, service in enumerate(row.values[3:]):
            efrs.loc[selection, variables[j]] = service

    efrs["nhs_visits"] = efrs[visit_variables].sum(axis=1)
    efrs["nhs_spending"] = efrs[spending_variables].sum(axis=1)

    return efrs


def main():
    # Create the EFRS input dataset
    logging.info("Creating EFRS input dataset...")
    if (folder / "data.csv").exists():
        efrs = pd.read_csv(folder / "data.csv")
    else:
        efrs = create_efrs_input_dataset()

    # Impute the NHS usage data into the EFRS dataset
    logging.info("Imputing NHS usage data into the EFRS dataset...")
    efrs = impute_nhs_usage(efrs)

    # Save the EFRS dataset to a CSV file
    logging.info("Saving EFRS dataset with NHS usage data...")
    efrs.to_csv(folder / "data.csv", index=False)


if __name__ == "__main__":
    main()
