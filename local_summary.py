import requests
import ollama
# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# # Load variables from .env into environment
# load_dotenv()

# API_KEY = os.getenv("OPENROUTER_API_KEY")

def summarize_local_news(articles: list) -> list:
    system_prompt = """
    You are a news summarizer for LOCAL Ghanaian news.
    IMPORTANT: Use ONLY the TITLE of the article to decide if it is Ghana-related.
    - If the TITLE indicates the news is about Ghana or local Ghanaian issues, summarize it.
    - If the TITLE is about foreign/international issues, SKIP it (do not summarize).
    - Keep the original title as given.
    - Generate a short, clear summary (4–6 sentences) of the body text.
    - Capture key facts (who, what, where, when, why, how).
    - Maintain a neutral, professional tone.
    - Format strictly as:
  
    Summary: [summary]  
    """

    summaries = []
    url = "http://localhost:11434/api/chat"

    for title, body in articles:
        user_content = f"Title: {title}\nBody: {body}"

        payload = {
            "model": "llama3.2",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "stream": False
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        if "message" in data:
            summary = data["message"]["content"].strip()
        elif "messages" in data and len(data["messages"]) > 0:
            summary = data["messages"][-1]["content"].strip()
        else:
            summary = ""

        if summary:
            summaries.append({
                "title": title,
                "summary": summary
            })

    return summaries

from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="<OPENROUTER_API_KEY>",
)

