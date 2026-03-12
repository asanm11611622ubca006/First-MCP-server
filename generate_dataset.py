"""
Generate a synthetic patient dataset with ~200 rows.
Run once: python generate_dataset.py
Output: patients.csv
"""

import csv
import random
import os

# Seed for reproducibility
random.seed(42)

FIRST_NAMES_MALE = [
    "James", "Robert", "John", "Michael", "David", "William", "Richard",
    "Joseph", "Thomas", "Christopher", "Daniel", "Matthew", "Anthony",
    "Mark", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin",
    "Brian", "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey",
    "Ryan", "Jacob", "Nicholas", "Gary", "Eric", "Jonathan", "Stephen",
    "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel",
]

FIRST_NAMES_FEMALE = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth",
    "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty",
    "Margaret", "Sandra", "Ashley", "Dorothy", "Kimberly", "Emily",
    "Donna", "Michelle", "Carol", "Amanda", "Melissa", "Deborah",
    "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen",
    "Amy", "Angela", "Shirley", "Anna", "Brenda", "Pamela", "Emma",
    "Nicole", "Helen",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts",
]

DISEASES = [
    "Diabetes",
    "Hypertension",
    "Asthma",
    "Heart Disease",
    "Arthritis",
    "Cancer",
    "Chronic Kidney Disease",
    "Depression",
    "Alzheimer's Disease",
    "Obesity",
    "COPD",
    "Migraine",
    "Thyroid Disorder",
    "Anemia",
    "Pneumonia",
]

NUM_PATIENTS = 200

def generate_patients(num: int) -> list[dict]:
    patients = []
    for i in range(1, num + 1):
        gender = random.choice(["Male", "Female"])
        if gender == "Male":
            first = random.choice(FIRST_NAMES_MALE)
        else:
            first = random.choice(FIRST_NAMES_FEMALE)
        last = random.choice(LAST_NAMES)

        patient = {
            "patient_id": i,
            "name": f"{first} {last}",
            "age": random.randint(18, 90),
            "gender": gender,
            "disease": random.choice(DISEASES),
        }
        patients.append(patient)
    return patients


def main():
    patients = generate_patients(NUM_PATIENTS)
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patients.csv")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["patient_id", "name", "age", "gender", "disease"])
        writer.writeheader()
        writer.writerows(patients)

    print(f"✅ Generated {len(patients)} patients → {output_path}")


if __name__ == "__main__":
    main()
