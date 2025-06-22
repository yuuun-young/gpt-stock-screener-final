import yfinance as yf
import openai
import os
import time

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_all_us_tickers():
    try:
        from yfinance import tickers_nasdaq, tickers_sp500
        tickers = tickers_nasdaq()
        tickers += [t for t in tickers_sp500() if t not in tickers]
        return tickers
    except Exception as e:
        print(f"[티커 수집 오류] {e}")
        return []

def run_stock_filter():
    tickers = get_all_us_tickers()
    selected = []
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).info
            revenue = data.get("totalRevenue", 0)
            market_cap = data.get("marketCap", 1)
            if revenue and market_cap and revenue * 10 > market_cap:
                selected.append({
                    "ticker": ticker,
                    "Revenue": revenue,
                    "Market Cap": market_cap
                })
            time.sleep(0.2)  # 너무 빠른 요청 방지
        except Exception as e:
            print(f"[오류] {ticker}: {e}")
            continue
    return selected
