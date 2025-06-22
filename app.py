from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils.summary import summarize
from utils.screener import run_stock_filter

app = FastAPI()

@app.get("/", response_class=JSONResponse)
def root():
    return JSONResponse(
        content={"message": "✅ GPT 주식 필터 API 정상 작동 중입니다. /docs로 이동하세요."},
        media_type="application/json; charset=utf-8"
    )

@app.get("/filter_stocks", response_class=JSONResponse)
def filter_stocks():
    filtered = run_stock_filter()
    return JSONResponse(
        content={"filtered_stocks": filtered},
        media_type="application/json; charset=utf-8"
    )

@app.get("/summary/{ticker}", response_class=JSONResponse)
def get_summary(ticker: str):
    summary_text = summarize(ticker)
    return JSONResponse(
        content={"summary": summary_text},
        media_type="application/json; charset=utf-8"
    )
