import requests


def generate_dialogue(topic):
    prompt = f"""
Create a realistic podcast conversation between HOST and GUEST.

Topic: {topic}

Rules:
- Natural conversational style
- HOST asks engaging questions
- GUEST gives smart informative answers
- Alternate lines properly
- Keep it short (6 total lines only)
- Each line should be short and concise.
- Use only this format:

HOST: line here
GUEST: line here

No title.
No notes.
No extra text.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()
