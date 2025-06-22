from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.screener import run_stock_filter, get_stock_summary

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "✅ GPT 주식 필터 API 정상 작동 중입니다. /docs로 이동하세요."}

@app.get("/filter_stocks")
def filter_stocks():
    return run_stock_filter()

@app.get("/summary/{ticker}")
def stock_summary(ticker: str):
    return get_stock_summary(ticker)
