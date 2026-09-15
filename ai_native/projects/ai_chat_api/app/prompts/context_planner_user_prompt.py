def build_context_planner_user_prompt(
    user_message: str,
    history: list[dict[str, str]],
) -> str:

    history_text = "\n".join(
        f"{message['role']}: {message['content']}" for message in history
    )

    return f"""
        <recent_conversation>
        {history_text}
        </recent_conversation>

        <current_user_message>
        {user_message}
        </current_user_message>
"""
