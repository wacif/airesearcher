# prompts.py

def get_research_prompt(question, field):
    return {
        "role": "user",
        "content": f"The user is asking a research-related question. Explain the topic '{question}' within the field of '{field}' in a concise, clear, and informative way. "
                   f"Limit your response to essential information and do not provide too much detail. Your role is to help with research-related topics only.",
    }

def get_guidance_prompt(question, field):
    return (f"To help you explore the research question '{question}' in the field of '{field}', start with a broad understanding of key concepts. "
            "Then, identify gaps or specific questions worth investigating further. Always cross-check sources and stay focused on research literature. "
            "If experiments or projects are needed, ensure you plan them systematically and document your findings.")

def invalid_question_prompt():
    return ("You are an AI research assistant and should only assist with research-related queries. "
            "If the question is not related to research (e.g., cooking recipes, politics, or other non-research topics), respond politely that you only assist with research.")
