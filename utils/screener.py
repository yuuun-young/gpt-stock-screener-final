import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_small_cap_tickers(min_cap=1e8, max_cap=3e9):
    url = "https://finance.yahoo.com/screener/predefined/ms_small_cap"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find_all("script")
    tickers = []

    for script in scripts:
        if "root.App.main" in script.text:
            try:
                raw_json = script.text.split("root.App.main = ")[1].split(";\n}(this));")[0]
                import json
                data = json.loads(raw_json)
                stores = data["context"]["dispatcher"]["stores"]
                quotes = stores["ScreenerResultsStore"]["results"]["rows"]
                for q in quotes:
                    cap = q.get("marketCap", 0)
                    if min_cap < cap < max_cap:
                        tickers.append(q["symbol"])
                break
            except Exception:
                continue
    return tickers

def get_stock_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        fin = stock.quarterly_financials
        if "Total Revenue" in fin.index and not fin.loc["Total Revenue"].empty:
            quarterly_revenue = fin.loc["Total Revenue"].iloc[0]
        else:
            quarterly_revenue = None

        return {
            "ticker": ticker,
            "name": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "marketCap": info.get("marketCap"),
            "quarterlyRevenue": int(quarterly_revenue) if quarterly_revenue else None,
            "summary": info.get("longBusinessSummary", "No summary available.")
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

def filter_stocks():
    tickers = get_small_cap_tickers()
    results = []

    for ticker in tickers:
        data = get_stock_summary(ticker)
        if data.get("marketCap") and data.get("quarterlyRevenue"):
            if data["quarterlyRevenue"] * 10 > data["marketCap"]:
                results.append(data)

    return results
