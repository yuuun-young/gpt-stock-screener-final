import yfinance as yf
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_stock_filter():
    tickers = yf.tickers_sp500().tickers + yf.tickers_nasdaq().tickers + yf.tickers_other().tickers
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
        except Exception:
            continue
    return selected

def get_stock_summary(ticker: str):
    try:
        info = yf.Ticker(ticker).info
        prompt = f"Summarize this stock based on the following data:\n{info}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return {"error": str(e)}
