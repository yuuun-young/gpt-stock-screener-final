import pandas as pd
import yfinance as yf
import time

def get_all_tickers_from_nasdaq():
    url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
    df = pd.read_csv(url, sep="|")
    return df["Symbol"].tolist()[:-1]

def run_filtered_stock_scan(limit=3000, max_market_cap=3e8, min_ratio=5):
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
                ratio = revenue / market_cap if market_cap else 0
                if ratio >= min_ratio and market_cap < max_market_cap:
                    selected.append({
                        "ticker": ticker,
                        "Quarterly Revenue": int(revenue),
                        "Market Cap": int(market_cap),
                        "Ratio": round(ratio, 2),
                        "Name": info.get("shortName", ""),
                        "Sector": info.get("sector", ""),
                        "Industry": info.get("industry", "")
                    })
                else:
                    print(f"❌ 제외됨: {ticker} - ratio={round(ratio,2)}, rev={revenue}, mcap={market_cap}")
            else:
                print(f"⚠️ 데이터 부족: {ticker}")

            time.sleep(0.5)

        except Exception as e:
            print(f"[오류] {ticker}: {e}")
            continue

    return pd.DataFrame(selected)

# 사용 예시
if __name__ == "__main__":
    df = run_filtered_stock_scan(min_ratio=5)  # 5배 이상으로 완화 가능
    df.to_csv("filtered_stocks_relaxed.csv", index=False)
    print("✅ 완료: 조건 충족 종목 수 =", len(df))
