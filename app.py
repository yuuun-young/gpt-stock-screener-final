from fastapi import FastAPI
from utils.screener import filter_stocks

app = FastAPI()

@app.get("/filter_stocks")
def get_filtered_stocks():
    return filter_stocks()
