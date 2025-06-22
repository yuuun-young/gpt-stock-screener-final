import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize(ticker):
    prompt = f"{ticker} 기업의 최근 재무 정보와 사업 개요를 요약해줘."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]