from fastapi import FastAPI
from utils.screener import run_stock_filter
from utils.summary import summarize

app = FastAPI()

@app.get("/")
def root():
    return {"message": "✅ GPT 주식 필터 API 정상 작동 중입니다. /docs로 이동하세요."}

@app.get("/filter_stocks")
def filter_stocks():
    return {"filtered_stocks": run_stock_filter()}

@app.get("/summary/{ticker}")
def get_summary(ticker: str):
    return {"summary": summarize(ticker)}