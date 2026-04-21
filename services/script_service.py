import requests


def generate_script(topic, tone, duration):
    prompt = f"""
Write a clean single speaker podcast narration.

Topic: {topic}
Tone: {tone}
Length: {duration}

Rules:
- Only one speaker
- No title
- No labels
- No intro tags
- No stage notes
- Natural spoken narration
- Maximum 80 words
- Clear opening and closing

Output only final script.
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