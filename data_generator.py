import random
import csv

locations = ["Bangalore", "Hyderabad", "Chennai", "Pune", "Delhi"]
roles = ["Developer", "QA", "Manager", "DevOps"]

with open("employees_1.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "id",
        "work_location",
        "present_salary",
        "expected_hike",
        "performance_rating",
        "role"
    ])

    # Generate 100,000 records
    for i in range(1001, 100001):   # IDs from 1001 to 100000
        writer.writerow([
            i,
            random.choice(locations),
            random.randint(40000, 120000),
            random.randint(5, 20),
            round(random.uniform(3, 5), 1),
            random.choice(roles)
        ])

print("✅ 100,000 employee records generated successfully in employees.csv")