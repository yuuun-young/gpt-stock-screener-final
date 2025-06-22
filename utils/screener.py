import yfinance as yf
import pandas as pd
import time
import logging

logging.basicConfig(level=logging.INFO)

def get_us_tickers(limit=300):  # 중소형주 중심으로 나스닥 100~300개만 임시 수집
    try:
        table = pd.read_html("https://en.wikipedia.org/wiki/NASDAQ-100")[4]
        tickers = table["Ticker"].tolist()
        return tickers[:limit]
    except Exception as e:
        logging.warning(f"티커 수집 실패: {e}")
        return []

def run_stock_filter():
    tickers = get_us_tickers()
    selected = []

    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).info
            revenue = data.get("totalRevenue")
            market_cap = data.get("marketCap")

            if revenue and market_cap and revenue * 10 > market_cap:
                selected.append({
                    "ticker": ticker,
                    "Revenue": revenue,
                    "Market Cap": market_cap
                })

            time.sleep(1.0)  # 과도한 요청 방지 (API Rate limit 보호)
        except Exception as e:
            logging.warning(f"{ticker} 오류: {e}")
            continue

    return selected

def get_stock_summary(ticker: str):
    try:
        info = yf.Ticker(ticker).info
        summary = {
            "ticker": ticker,
            "name": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "marketCap": info.get("marketCap"),
            "totalRevenue": info.get("totalRevenue"),
            "summary": info.get("longBusinessSummary", "No summary available.")
        }
        return summary
    except Exception as e:
        return {"error": str(e)}
