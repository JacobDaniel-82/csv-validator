import sys
import pandas as pd

REQUIRED_COLUMNS = ["id", "name", "age", "email"]
EMAIL_PATTERN = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"


def load_csv(path):
    # read everything as string so bad values like "abc" don't break the column type
    df = pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""])
    # treat whitespace-only cells as missing too
    return df.replace(r"^\s*$", pd.NA, regex=True)


def check_required_columns(df, required):
    return [col for col in required if col not in df.columns]


# ---- RULES: each returns a boolean Series, True = bad row ----

def find_missing_values(df):
    return df.isna().any(axis=1)


def find_duplicates(df):
    # keep="first" -> first copy is valid, later copies are flagged
    return df.duplicated(keep="first")


def find_bad_age(df):
    age = pd.to_numeric(df["age"], errors="coerce")
    not_a_number = df["age"].notna() & age.isna()   # "abc", "N/A", "twenty"
    out_of_range = (age < 0) | (age > 120)
    return not_a_number | out_of_range


def find_bad_email(df):
    has_value = df["email"].notna()
    return has_value & ~df["email"].str.match(EMAIL_PATTERN, na=False)


# the engine: add a new rule by writing a function + adding one line here
RULES = {
    "missing_value": find_missing_values,
    "duplicate": find_duplicates,
    "bad_age": find_bad_age,
    "bad_email": find_bad_email,
}


def split_records(df):
    masks = pd.DataFrame({name: rule(df) for name, rule in RULES.items()})
    invalid_mask = masks.any(axis=1)

    valid_df = df[~invalid_mask]
    invalid_df = df[invalid_mask].copy()

    reasons = masks.apply(lambda row: ", ".join(row.index[row]), axis=1)
    invalid_df["reasons"] = reasons[invalid_mask]

    return valid_df, invalid_df, masks


def print_summary(total, valid, invalid, masks):
    print(f"Total rows:   {total}")
    print(f"Valid rows:   {valid}")
    print(f"Invalid rows: {invalid}")
    print("\nBreakdown (a row can fail multiple rules):")
    for name in masks.columns:
        print(f"  {name}: {masks[name].sum()}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sample.csv"
    df = load_csv(path)

    missing_cols = check_required_columns(df, REQUIRED_COLUMNS)
    if missing_cols:
        print(f"Missing required columns: {missing_cols}")
        return

    valid_df, invalid_df, masks = split_records(df)
    valid_df.to_csv("valid.csv", index=False)
    invalid_df.to_csv("invalid.csv", index=False)
    print_summary(len(df), len(valid_df), len(invalid_df), masks)


if __name__ == "__main__":
    main()