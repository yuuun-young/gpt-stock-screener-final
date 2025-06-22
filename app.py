from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils.summary import summarize
from utils.screener import run_stock_filter

app = FastAPI()

@app.get("/")
def root():
    return JSONResponse(content={"message": "✅ GPT 주식 필터 API 정상 작동 중입니다. /docs로 이동하세요."})

@app.get("/filter_stocks")
def filter_stocks():
    filtered = run_stock_filter()
    return {"filtered_stocks": filtered}

@app.get("/summary/{ticker}")
def get_summary(ticker: str):
    summary_text = summarize(ticker)
    return {"summary": summary_text}
