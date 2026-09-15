def build_system_context_prompt(memories: str = "") -> str:
    prompt = """
        You are a helpful AI assistant.

        Answer truthfully.

        If user memories are provided, use them as background knowledge.
    """

    if memories:
        prompt += f"""
        Known facts:
        {memories}
    """

    return prompt.strip()
