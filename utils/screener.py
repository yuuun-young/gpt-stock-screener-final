import yfinance as yf
import pandas as pd
import requests
from fastapi import FastAPI
from typing import List

app = FastAPI()


# ✅ NASDAQ 전체 티커 불러오기 (nasdaqlisted.txt)
def get_nasdaq_tickers() -> List[str]:
    url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
    try:
        df = pd.read_csv(url, sep="|")
        tickers = df['Symbol'].dropna().tolist()
        return [t for t in tickers if t.isalpha()]  # 숫자/기호 제외
    except Exception as e:
        print(f"[티커 로딩 실패] {e}")
        return []


# ✅ 조건 필터링
@app.get("/filter_stocks")
def filter_stocks():
    tickers = get_nasdaq_tickers()
    filtered_stocks = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            market_cap = stock.info.get("marketCap")

            if market_cap is None or market_cap > 3_000_000_000:
                continue  # 시총 30억 초과 또는 정보 없음

            revenue = stock.quarterly_financials.loc["Total Revenue"].iloc[0]

            # 기본 조건: 분기 매출 x 10 > 시가총액
            if revenue * 10 > market_cap:
                filtered_stocks.append({
                    "ticker": ticker,
                    "market_cap": market_cap,
                    "quarterly_revenue": revenue,
                    "condition": "R×10 > 시총"
                })

            # 조건 완화 fallback (optional)
            elif revenue * 5 > market_cap:
                filtered_stocks.append({
                    "ticker": ticker,
                    "market_cap": market_cap,
                    "quarterly_revenue": revenue,
                    "condition": "R×5 > 시총 (완화)"
                })

        except Exception as e:
            continue

    return {"filtered_stocks": filtered_stocks}

# ✅ 실행 예시
if __name__ == "__main__":
    results = run_stock_filter()
    df = pd.DataFrame(results)
    df.to_csv("filtered_stocks.csv", index=False)
    print(df)
    
def get_stock_summary(ticker: str):
    import yfinance as yf
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # 최근 분기 매출 (API 개선용)
        fin = stock.quarterly_financials
        if "Total Revenue" in fin.index and not fin.loc["Total Revenue"].empty:
            quarterly_revenue = fin.loc["Total Revenue"].iloc[0]
        else:
            quarterly_revenue = None

        summary = {
            "ticker": ticker,
            "name": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "marketCap": info.get("marketCap"),
            "totalRevenue": int(quarterly_revenue) if quarterly_revenue else None,
            "summary": info.get("longBusinessSummary", "No summary available.")
        }
        return summary
    except Exception as e:
        return {"error": str(e)}
