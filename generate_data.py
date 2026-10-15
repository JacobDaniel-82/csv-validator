
import csv
import random

# Configuration
OUTPUT_FILE = "sample.csv"
NUM_ROWS = 500
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

# Sample Indian names
first_names = [
    "Aarav", "Aditya", "Arjun", "Rohan", "Rahul",
    "Vikram", "Karthik", "Arun", "Vijay", "Sanjay",
    "Priya", "Ananya", "Divya", "Sneha", "Kavya",
    "Meera", "Pooja", "Lakshmi", "Deepa", "Nisha",
    "Ishaan", "Siddharth", "Varun", "Akash", "Manoj",
    "Harish", "Keerthi", "Swathi", "Suresh", "Naveen"
]

last_names = [
    "Sharma", "Patel", "Kumar", "Reddy", "Iyer",
    "Nair", "Rao", "Singh", "Verma", "Gupta",
    "Menon", "Pillai", "Das", "Joshi", "Mishra",
    "Krishnan", "Chatterjee", "Bose", "Mehta", "Yadav"
]

# Approximate percentages of the 500 rows
counts = {
    "missing_age": round(NUM_ROWS * 0.05),       # 25
    "missing_name": round(NUM_ROWS * 0.05),      # 25
    "non_numeric_age": round(NUM_ROWS * 0.03),   # 15
    "invalid_age": round(NUM_ROWS * 0.03),       # 15
    "duplicate": round(NUM_ROWS * 0.04),         # 20
    "invalid_email": round(NUM_ROWS * 0.03),     # 15
}

# Generate clean baseline records
rows = []

for i in range(1, NUM_ROWS + 1):
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    age = random.randint(18, 80)

    # Produce a valid-looking email with a numeric suffix
    email_name = f"{first.lower()}.{last.lower()}{i}"
    email = f"{email_name}@gmail.com"

    rows.append({
        "id": i,
        "name": name,
        "age": age,
        "email": email
    })

# Track which row positions receive each type of issue.
# Assign disjoint positions to avoid accidentally overwriting
# one issue with another.
positions = list(range(NUM_ROWS))
random.shuffle(positions)

bad_positions = {}
start = 0

for issue, count in counts.items():
    bad_positions[issue] = positions[start:start + count]
    start += count

# Inject missing ages
for pos in bad_positions["missing_age"]:
    rows[pos]["age"] = ""

# Inject missing names
for pos in bad_positions["missing_name"]:
    rows[pos]["name"] = ""

# Inject non-numeric ages
non_numeric_values = ["abc", "twenty", "N/A"]
for pos in bad_positions["non_numeric_age"]:
    rows[pos]["age"] = random.choice(non_numeric_values)

# Inject invalid ages
for pos in bad_positions["invalid_age"]:
    rows[pos]["age"] = random.choice([
        random.randint(-50, -1),
        random.randint(121, 180)
    ])

# Inject invalid emails
invalid_email_values = [
    "missingatsign.gmail.com",
    "user@",
    "usergmail.com",
    "user name@gmail.com",
    "user@@gmail.com"
]

for pos in bad_positions["invalid_email"]:
    rows[pos]["email"] = random.choice(invalid_email_values)

# Inject exact duplicates of earlier rows.
# Copy the entire record, including its ID.
duplicate_positions = bad_positions["duplicate"]

for pos in duplicate_positions:
    # Select a row before this position so the duplicate
    # always copies an earlier record in the original dataset.
    earlier_pos = random.randrange(pos)
    rows[pos] = rows[earlier_pos].copy()

# Shuffle all records so issues are distributed throughout the file.
random.shuffle(rows)

# Write CSV
fieldnames = ["id", "name", "age", "email"]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Print injection summary
print(f"CSV generated successfully: {OUTPUT_FILE}")
print(f"Total data rows: {NUM_ROWS}")
print(f"Random seed: {RANDOM_SEED}")
print("\nBad rows injected (target counts):")

for issue, count in counts.items():
    percentage = count / NUM_ROWS * 100
    print(f"  {issue.replace('_', ' ').title():<20} {count:>3} ({percentage:.1f}%)")

print(f"\nTotal targeted issue injections: {sum(counts.values())}")
print("Note: Issue counts describe the injected categories.")
print("Duplicate rows contain copied IDs, so IDs may repeat.")
