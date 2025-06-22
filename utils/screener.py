import pandas as pd
import yfinance as yf
import time

def get_all_nasdaq_tickers():
    try:
        url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
        tickers = pd.read_csv(url, sep='|')
        tickers = tickers[~tickers['Symbol'].str.contains('File Creation Time')]
        return tickers['Symbol'].tolist()
    except Exception as e:
        print(f"[티커 수집 실패] {e}")
        return []

def run_midcap_value_filter():
    tickers = get_all_nasdaq_tickers()
    result = []

    for ticker in tickers[:300]:  # ✅ 너무 많으므로 임시로 300개 제한
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            market_cap = info.get("marketCap")

            # ✅ 시가총액 기준 중소형주 필터 (3억~10억 달러)
            if not market_cap or not (3e8 <= market_cap <= 1e9):
                continue

            fin = stock.quarterly_financials
            if "Total Revenue" not in fin.index:
                continue
            revenue = fin.loc["Total Revenue"].iloc[0]

            if revenue * 10 > market_cap:
                reason = "매출 x10 > 시총"
            elif revenue * 5 > market_cap:
                reason = "매출 x5 > 시총 (완화)"
            else:
                continue

            result.append({
                "ticker": ticker,
                "market_cap": int(market_cap),
                "quarterly_revenue": int(revenue),
                "reason": reason
            })

            time.sleep(0.6)
        except Exception as e:
            print(f"[오류] {ticker}: {e}")
            continue

    return pd.DataFrame(result)
