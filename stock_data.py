import sys
from datetime import date
import time
import yfinance as yf
import pandas as pd
import yfinance_fields as yf_fields

def get_ticker_list():
    tickers = []
    with open(sys.argv[1], 'r') as tick_file:
        for line in tick_file:
            line = line.replace(' ', '')
            line = line.strip()
            ticks = line.split(',')
            tickers.extend(ticks)

    return tickers

def filter_fields(info):
    new_info = {}
    for key in info.keys():
        if key in yf_fields.fields:
            if 'date' in key.lower() and info[key]:
                new_info[key] = date.fromtimestamp(info[key])
            else:
                new_info[key] = info[key]

    return new_info

def write_df(df):
    today = date.today()
    df.to_excel(f'stock_data_{today.strftime("%b-%d-%Y")}.xlsx')

def main():
    tickers = get_ticker_list()
    stock_df = pd.DataFrame(columns=yf_fields.fields)

    # Get stock data
    for ticker in tickers:
        print(f'Getting data for {ticker}')
        try:
            stock = yf.Ticker(ticker)
            stock_info = filter_fields(stock.info)
            stock_df = stock_df.append(stock_info, ignore_index=True)
        except Exception as e:
            e.with_traceback()
            print(f'ERROR: Could not retrieve info on {ticker}')
        finally:
            time.sleep(0.5)
    
    write_df(stock_df)

    
if __name__ == '__main__':
    main()
