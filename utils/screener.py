import yfinance as yf
import pandas as pd
import time
import logging

logging.basicConfig(level=logging.INFO)

# ✅ CSV에서 티커 로딩 (예: NASDAQ 중소형주 리스트)
def get_tickers_from_csv(file_path="nasdaq_screener.csv"):
    try:
        df = pd.read_csv(file_path)
        tickers = df["Symbol"].dropna().unique().tolist()
        logging.info(f"총 {len(tickers)}개 티커 로딩 완료")
        return tickers
    except Exception as e:
        logging.error(f"[CSV 로딩 실패] {e}")
        return []

# ✅ 조건 필터 실행
def run_stock_filter():
    tickers = get_tickers_from_csv()
    selected = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)

            # 분기 재무 정보
            fin = stock.quarterly_financials
            if "Total Revenue" not in fin.index or fin.loc["Total Revenue"].empty:
                continue
            revenue = fin.loc["Total Revenue"].iloc[0]  # 최신 분기 매출

            # 시가총액 정보
            info = stock.info
            market_cap = info.get("marketCap", None)

            if revenue is None or market_cap is None:
                continue

            # ✅ 조건 비교 (엄격/완화 모두)
            tag = None
            if revenue * 10 > market_cap:
                tag = "✅ 기준 만족 (x10)"
            elif revenue * 8 > market_cap:
                tag = "⚠️ 완화 기준 (x8)"

            if tag and market_cap < 3_000_000_000:  # 30억 달러 이하 (중소형주)
                selected.append({
                    "ticker": ticker,
                    "name": info.get("shortName", ""),
                    "revenue": int(revenue),
                    "marketCap": int(market_cap),
                    "tag": tag
                })

            time.sleep(0.5)

        except Exception as e:
            logging.warning(f"[{ticker} 오류] {e}")
            continue

    return selected

# ✅ 실행 예시
if __name__ == "__main__":
    results = run_stock_filter()
    df = pd.DataFrame(results)
    df.to_csv("filtered_stocks.csv", index=False)
    print(df)
