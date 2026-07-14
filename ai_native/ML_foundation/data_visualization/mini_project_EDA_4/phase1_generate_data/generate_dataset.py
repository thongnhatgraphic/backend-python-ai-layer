import numpy as np
import pandas as pd
import random
from pathlib import Path

from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase1_generate_data.business_rules import (
    business_rules,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase1_generate_data.constant import (
    MIN_AGE,
    MAX_AGE,
    MIN_ENGLISH,
    MAX_ENGLISH,
    EDUCATION,
    MIN_SCORE_PYTHON,
    MAX_SCORE_PYTHON,
    PASS_SCORE,
)


def calculate_score(candidate):
    score = 0

    for rule in business_rules:
        value = candidate[rule["feature"]]
        condition = rule["range_condition"]

        minimum = condition.get("minimum")
        maximum = condition.get("maximum")

        if maximum is None:
            if value >= minimum:
                score += rule["score"]
        else:
            if minimum <= value <= maximum:
                score += rule["score"]

    return score


def evaluate_to_hire(candidate):
    score = calculate_score(candidate)
    candidate["Hired"] = 1 if score >= PASS_SCORE else 0

    return candidate


def generate_experience(age, career_switcher):
    exp = None
    if career_switcher == 0:
        if age < 25:
            exp = np.random.randint(1, 6)
        elif age < 30:
            exp = np.random.randint(6, 11)
        else:
            exp = np.random.randint(11, 15)
    else:
        if age < 30:
            exp = np.random.randint(1, 4)
        else:
            exp = np.random.randint(2, 5)
    return exp


def generate_projects(exp):
    number_of_projects = None

    if exp >= 10:
        number_of_projects = random.randint(10, 15)
    elif exp > 5 and exp < 10:
        number_of_projects = random.randint(7, 12)
    else:
        number_of_projects = random.randint(2, 6)
    return number_of_projects


def generate_ai(python_score):
    if python_score > 80:
        return random.choice([0, 1])
    else:
        return 0


def generate_education():
    # University = 80% College 20%
    probability = np.random.choice(
        [EDUCATION["university"], EDUCATION["college"]], p=[0.8, 0.2]
    )
    return probability


def generate_candidate(id: int):
    candidate = {}
    age = np.random.randint(MIN_AGE, MAX_AGE + 1)
    eng = np.random.normal(loc=700, scale=100)
    eng = int(np.clip(eng, MIN_ENGLISH, MAX_ENGLISH))

    is_career_switcher = random.choice([0, 1])
    exp = generate_experience(age, is_career_switcher)
    number_of_projects = generate_projects(exp)

    edu = generate_education()
    python = np.random.normal(loc=75, scale=10)
    python = int(np.clip(python, MIN_SCORE_PYTHON, MAX_SCORE_PYTHON))
    docker = np.random.choice([0, 1], p=[0.8, 0.2])
    redis = np.random.choice([0, 1], p=[0.8, 0.2])
    rabbitmq = np.random.choice([0, 1], p=[0.8, 0.2])
    ai = generate_ai(python)

    candidate = {
        "CandidateId": id,
        "Age": age,
        "English": eng,
        "Experience": exp,
        "Projects": number_of_projects,
        "Education": edu,
        "Python": python,
        "Docker": docker,
        "Redis": redis,
        "RabbitMQ": rabbitmq,
        "AI": ai,
    }
    return candidate


list_sample = []
NUM_SAMPLES = 10000
for _ in range(NUM_SAMPLES):
    candidate = generate_candidate(_ + 1)
    candidate = evaluate_to_hire(candidate)
    list_sample.append(candidate)


df = pd.DataFrame(list_sample)


BASE_DIR = Path(__file__).parent


def save_dataset(df):
    csv_path = BASE_DIR / "phase3_mini_generate_dirty_data/employee_recruitment.csv"
    df.to_csv(csv_path, index=False)
    return


save_dataset(df)
