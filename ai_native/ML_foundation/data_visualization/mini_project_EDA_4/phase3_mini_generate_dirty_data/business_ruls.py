percent_duplicate = 0.05

percent_missing = 0.05

percent_wrong_type = 0.05

percent_invalid_value = 0.05

percent_outlier = 0.05

invalid_rules = {
    "Age": 100,  # value from 22 to 45
    "English": 22222,  # value from 350 to 950
    "Python": 33333,  # value from 0 to 100
    "Docker": -3,
    "Redis": -2,
    "RabbitMQ": 33333333,
    "AI": 2222,
}

outlier_rules = {
    "Age": (10, 80),
    "English": (100, 1500),
    "Python": (10, 100),
    "Experience": (0, 50),
    "Projects": (0, 50),
}
