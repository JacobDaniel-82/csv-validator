# CSV Data Validator

A small Python tool that reads a CSV file, validates each record against a set of rules, and splits the data into clean and rejected records.

## What it does

- Checks that all required columns exist (`id`, `name`, `age`, `email`)
- Flags rows that fail any rule and records the reason
- Writes `valid.csv` and `invalid.csv` (with a `reasons` column)
- Prints a summary with a per-rule breakdown

## Rules

| Rule | What it catches |
| --- | --- |
| missing_value | Any empty or whitespace-only cell |
| duplicate | Exact duplicate rows (first copy is kept) |
| bad_age | Non-numeric age, or age below 0 / above 120 |
| bad_email | Email not matching a basic `name@domain.tld` pattern |

A row can fail multiple rules, so the breakdown can add up to more than the invalid count.

## How it works

Each rule is a small function that returns a True/False mask (True = bad row). All rules are registered in the `RULES` dictionary, and `split_records` combines the masks. To add a new rule, write one function and add one line to `RULES`.

## Usage

```bash
pip install -r requirements.txt
python validator.py sample.csv
```

## Sample data

`sample.csv` is synthetic data (500 rows) with deliberately injected errors: missing values, invalid ages, duplicates, and malformed emails. Running the validator on `valid.csv` returns 0 invalid rows.

generate_data.py creates the synthetic sample.csv

## Tech

Python, pandas