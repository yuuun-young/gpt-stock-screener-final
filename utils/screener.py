import yfinance as yf
import pandas as pd


def get_nasdaq_nyse_tickers():
    nasdaq_url = "https://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
    nyse_url = "https://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download"

    try:
        nasdaq_df = pd.read_csv(nasdaq_url)
        nyse_df = pd.read_csv(nyse_url)
    except Exception as e:
        print(f"Error fetching ticker data: {e}")
        return []

    tickers = list(nasdaq_df['Symbol'].dropna()) + list(nyse_df['Symbol'].dropna())
    return tickers


def run_stock_filter():
    tickers = get_nasdaq_nyse_tickers()

    result = []
    for ticker in tickers[:200]:  # 과부하 방지를 위해 우선 200개만 사용
        try:
            info = yf.Ticker(ticker).info
            if info and 'marketCap' in info and 'totalRevenue' in info:
                market_cap = info['marketCap']
                revenue = info['totalRevenue']

                if revenue and market_cap and revenue > 0:
                    psr = market_cap / revenue
                    if psr < 1:
                        result.append({
                            'ticker': ticker,
                            'psr': round(psr, 2),
                            'marketCap': market_cap,
                            'revenue': revenue
                        })
        except Exception as e:
            continue

    return result
