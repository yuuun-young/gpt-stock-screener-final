import pandas as pd
import yfinance as yf
import time

def get_all_tickers_from_nasdaq():
    url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
    df = pd.read_csv(url, sep="|")
    return df["Symbol"].tolist()[:-1]  # 마지막 행은 Summary

def run_filtered_stock_scan(limit=3000, max_market_cap=3e8):
    tickers = get_all_tickers_from_nasdaq()[:limit]
    selected = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            fin = stock.quarterly_financials

            revenue = None
            if "Total Revenue" in fin.index and not fin.loc["Total Revenue"].empty:
                revenue = fin.loc["Total Revenue"].iloc[0]

            market_cap = info.get("marketCap")

            if revenue and market_cap:
                if revenue * 10 > market_cap and market_cap < max_market_cap:
                    selected.append({
                        "ticker": ticker,
                        "Quarterly Revenue": int(revenue),
                        "Market Cap": int(market_cap),
                        "Name": info.get("shortName", ""),
                        "Sector": info.get("sector", ""),
                        "Industry": info.get("industry", "")
                    })
                else:
                    print(f"❌ 제외됨: {ticker} - Revenue={revenue}, MCap={market_cap}")
            else:
                print(f"⚠️ 데이터 부족: {ticker}")
            
            time.sleep(0.5)  # 과도한 요청 방지

        except Exception as e:
            print(f"[오류] {ticker}: {e}")
            continue

    return pd.DataFrame(selected)

# 사용 예시
if __name__ == "__main__":
    df = run_filtered_stock_scan()
    df.to_csv("filtered_smallcap_stocks.csv", index=False)
    print("✅ 완료: 조건 충족 종목 수 =", len(df))
