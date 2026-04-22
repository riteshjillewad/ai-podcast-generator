'''import requests


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
'''

import requests


def generate_dialogue(topic, mode):

    if mode == "debate":

        prompt = f"""
Create a podcast debate between HOST and GUEST.

Topic: {topic}

HOST challenges ideas.
GUEST gives arguments.

6 lines only.

Format:
HOST:
GUEST:
"""

    elif mode == "motivational":

        prompt = f"""
Create an inspiring podcast between HOST and GUEST.

Topic: {topic}

HOST asks uplifting questions.
GUEST gives motivational answers.

6 lines only.

Format:
HOST:
GUEST:
"""

    elif mode == "news":

        prompt = f"""
Create a podcast news discussion between HOST and GUEST.

Topic: {topic}

HOST presents headlines.
GUEST gives insights.

6 lines only.

Format:
HOST:
GUEST:
"""

    else:

        prompt = f"""
Create an interview podcast between HOST and GUEST.

Topic: {topic}

HOST asks engaging questions.
GUEST gives expert answers.

6 lines only.

Format:
HOST:
GUEST:
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
