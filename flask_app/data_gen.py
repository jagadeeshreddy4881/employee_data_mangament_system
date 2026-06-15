import pandas as pd
import random

# Number of employees to generate
NUM_EMPLOYEES = 100

# Sample data
locations = [
    "Chennai",
    "Bangalore",
    "Hyderabad",
    "Pune",
    "Mumbai"
]

roles = [
    "Developer",
    "QA",
    "DevOps",
    "Manager",
    "Designer"
]

employees = []

# Generate employee data
for i in range(NUM_EMPLOYEES):

    employee = {

        "id": 1001 + i,

        "work_location":
            random.choice(locations),

        "present_salary":
            random.randint(
                30000,
                150000
            ),

        "expected_hike":
            random.randint(
                5,
                25
            ),

        "performance_rating":
            round(
                random.uniform(
                    3.0,
                    5.0
                ),
                1
            ),

        "role":
            random.choice(roles)
    }

    employees.append(employee)

# Convert list to DataFrame
df = pd.DataFrame(employees)

# Save as CSV
df.to_csv(
    "employees_1.csv",
    index=False
)

print(
    f"{NUM_EMPLOYEES} employees generated successfully."
)

print(
    "File saved as employees_1.csv"
)