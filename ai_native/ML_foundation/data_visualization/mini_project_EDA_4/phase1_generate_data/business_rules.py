business_rules = [
    {"feature": "Experience", "range_condition": {"minimum": 10}, "score": 30},
    {
        "feature": "Experience",
        "range_condition": {"minimum": 5, "maximum": 9},
        "score": 20,
    },
    {
        "feature": "Experience",
        "range_condition": {"minimum": 2, "maximum": 4},
        "score": 10,
    },
    {
        "feature": "Python",
        "range_condition": {"minimum": 95, "maximum": 100},
        "score": 20,
    },
    {
        "feature": "Python",
        "range_condition": {"minimum": 85, "maximum": 94},
        "score": 15,
    },
    {
        "feature": "Python",
        "range_condition": {"minimum": 70, "maximum": 84},
        "score": 5,
    },
    {"feature": "Projects", "range_condition": {"minimum": 12}, "score": 15},
    {
        "feature": "Projects",
        "range_condition": {"minimum": 8, "maximum": 11},
        "score": 8,
    },
    {
        "feature": "Projects",
        "range_condition": {"minimum": 5, "maximum": 7},
        "score": 5,
    },
    {"feature": "Docker", "range_condition": {"minimum": 1}, "score": 5},
    {"feature": "Redis", "range_condition": {"minimum": 1}, "score": 5},
    {"feature": "RabbitMQ", "range_condition": {"minimum": 1}, "score": 5},
    {"feature": "AI", "range_condition": {"minimum": 1}, "score": 10},
    {"feature": "English", "range_condition": {"minimum": 800}, "score": 10},
    {
        "feature": "English",
        "range_condition": {"minimum": 600, "maximum": 799},
        "score": 5,
    },
]
