import copy

messages = [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Redis là gì?"},
]


def connect():
    parts = []

    for message in messages:
        parts.append(message["content"])

    print(parts)

    return "".join(parts)


result = connect()

print(result)


BEGIN_OF_TEXT = "<|begin_of_text|>"
END_OF_TURN = "<|eot_id|>"

START_HEADER = "<|start_header_id|>"
END_HEADER = "<|end_header_id|>"

ASSISTANT_HEADER = f"{START_HEADER}assistant{END_HEADER}"


def apply_chat_template(messages):
    parts = [BEGIN_OF_TEXT]

    for message in messages:
        parts.append(
            f"{START_HEADER}{message['role']}{END_HEADER}\n"
            f"{message['content']}\n"
            f"{END_OF_TURN}\n"
        )

    parts.append(ASSISTANT_HEADER)

    return "".join(parts)
