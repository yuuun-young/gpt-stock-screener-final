import yfinance as yf

def run_stock_filter():
    tickers = yf.Tickers(' '.join(get_nasdaq_nyse_tickers()))
    result = []
    for ticker_symbol, ticker_obj in tickers.tickers.items():
        try:
            info = ticker_obj.info
            market_cap = info.get("marketCap", 0)
            revenue = info.get("totalRevenue", 0)
            current_ratio = info.get("currentRatio", 0)
            psr = market_cap / revenue if revenue else None

            if market_cap and revenue:
                if market_cap < 5e9 and (
                    (psr and psr < 0.1) +
                    (current_ratio and current_ratio > 1.5)
                ) >= 2:
                    result.append({
                        "ticker": ticker_symbol,
                        "market_cap": market_cap,
                        "revenue": revenue,
                        "current_ratio": current_ratio,
                        "psr": psr
                    })
        except Exception:
            continue
    return result

def get_nasdaq_nyse_tickers():
    from yfinance import tickers_nasdaq, tickers_other
    return tickers_nasdaq() + tickers_other()