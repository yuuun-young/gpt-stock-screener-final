import yfinance as yf
import pandas as pd
import time
import logging

logging.basicConfig(level=logging.INFO)

def get_us_tickers(limit=1000):  # 중소형주 중심으로 나스닥 100~300개만 임시 수집
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
            stock = yf.Ticker(ticker)
            fin = stock.quarterly_financials
            revenue = fin.loc["Total Revenue"][0] if "Total Revenue" in fin.index else None
            market_cap = stock.info.get("marketCap")

            if revenue and market_cap and revenue * 10 > market_cap:
                selected.append({
                    "ticker": ticker,
                    "Quarterly Revenue": int(revenue),
                    "Market Cap": int(market_cap)
                })
            else:
                print(f"❌ 제외됨: {ticker}, Revenue={revenue}, MCap={market_cap}")

            time.sleep(0.5)

        except Exception as e:
            print(f"[오류] {ticker}: {e}")
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
