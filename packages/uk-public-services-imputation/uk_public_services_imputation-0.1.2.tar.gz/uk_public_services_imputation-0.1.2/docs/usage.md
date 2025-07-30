# How to use

This package can be reused for any data, not just PolicyEngine's Enhanced FRS. For example, you could provide your own set of households, and add NHS and ETB-containing public services to them. This page describes how to do this.

## Installation

First, install the package (after having installed Python 3.11) by running this command from the root of the repo:

```bash
pip install -e .
```

## Usage

This package is run with the command `./uk-public-services-imputation`. Running this command will:

1. Look in the `data/` folder for `data.csv`.
2. If it doesn't exist, it will download PolicyEngine's Enhanced FRS data. For this you *must* have set a `HUGGING_FACE_TOKEN` environment variable to a token that has access to the Hugging Face repo [here](https://huggingface.co/policyengine/policyengine-uk-data-private). Contact [hello@policyengine.org](mailto:hello@policyengine.org) if you would like access (you'll need to meet the UKDA requirements).
3. It will also look for `data/householdv2_1977-2021.tab` (the Effects of Taxes and Benefits data for 2021). If you've set `HUGGING_FACE_TOKEN`, this will be downloaded automatically. If not, you can also download it from the UKDA website, and put this tab file in the `data/` folder yourself.
3. It will then run all imputations on the data, and overwrite the results to `data/data.csv`.

## Imputing over custom data

To run over custom data, you will need these columns in your (person-level, a row for each person) `data.csv`:

- `age`: Age
- `gender`: Gender (`MALE` or `FEMALE`)
- `household_weight`: Household weight
- `region`: Region (e.g. `NORTH_EAST`, `NORTH_WEST`, etc.) Should be one of these: `['YORKSHIRE', 'NORTHERN_IRELAND', 'WALES' 'EAST_MIDLANDS', 'LONDON', 'SOUTH_EAST', 'EAST_OF_ENGLAND', 'SOUTH_WEST', 'NORTH_EAST', 'NORTH_WEST', 'WEST_MIDLANDS', 'SCOTLAND']`
- `household_id`: Household ID
- `is_adult`: Is an adult (true/false)
- `is_child`: Is a child (true/false)
- `is_SP_age`: Is State Pension age (true/false)
- `dla`: Disability Living Allowance (value per year)
- `pip`: Personal Independence Payment (value per year)
- `household_count_people`: Number of people in the household
- `hbai_household_net_income`: HBAI-definition dousehold net income (before housing costs)
- `count_primary_education`: Person is in primary education (true/false)
- `count_secondary_education`: Person is in secondary education (true/false)
- `count_further_education`: Person is in further education (true/false)

If you've done this correctly, run `./uk-public-services-imputation` and it will run the imputations on your data. The results will be saved to `data/data.csv` as before.
