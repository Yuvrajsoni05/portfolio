import requests

API_URL = "YOUR_HUGGINGFACE_API_URL"

HEADERS = {
    "Authorization": "Bearer YOUR_TOKEN"
}


def load_resume():

    with open("resume_context.txt", "r") as file:
        return file.read()


resume_context = load_resume()


def ask_ai(question):

    prompt = f"""
    You are an AI assistant for Yuvraj Soni.

    Resume Context:
    {resume_context}

    User Question:
    {question}

    Reply professionally and naturally.
    """

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={
            "inputs": prompt
        }
    )

    return response.json()


while True:

    question = input("You: ")

    answer = ask_ai(question)

    print(answer)