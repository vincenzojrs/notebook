# Inspired by  Algorithmic Trading – Machine Learning & Quant Strategies Course with Python by freeCodeCamp.org
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas_datareader.data as web
import yfinance as yf
from statsmodels.regression.rolling import RollingOLS
import datetime as dt
import pandas_ta

class AlgoTradingStrategy:
  def __init__(self, end_date):
    """ Instantiate the strategy by downloading the SP500 companies, and set the time window of your backtest"""
    self.stock_link = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    self.stock_symbols = pd.read_html(self.stock_link)[0]['Symbol'].str.replace('.', '-', regex = False).unique().tolist()
    self.end_date = end_date
    self.start_date = pd.to_datetime(end_date) - pd.DateOffset(365*8)

  def __str__(self):
    return "This is my first algorithmic trading strategy"

  def download_dataframe(self):
    """ Download companies in the given timeframe using yahoo finance"""
    return yf.download(tickers = self.stock_symbols,
                       start = self.start_date,
                       end = self.end_date)

  def fixed_dataframe(self, df):
    """ Apply some data cleaning """
    dataframe = df.stack()
    dataframe.index.names = ['date', 'ticker']
    dataframe.columns = dataframe.columns.str.lower()
    return dataframe

  def garman_klass(self, df):
    """ Create the Garman-Klass indicator """
    df['garman_klass'] = ((np.log(df['high']) - np.log(df['low']))**2) / 2 - \
                            (2 * np.log(2) - 1) * (np.log(df['adj close']) - np.log(df['open']))**2
    return df

  def rsi(self, df, periods = 20):
    """ Create the RSI indicator """
    df['rsi'] = df.groupby(level = 1)['adj close'].transform(lambda x : pandas_ta.rsi(close = x,
                                                                                      length = periods))
    return df

  def bollingerbands(self, df, periods = 20):
    """ Create the bollinger bands"""
    df['bb_low'] = df.groupby(level = 1)['adj close'].transform(lambda x : pandas_ta.bbands(close = np.log1p(x),
                                                                             length = periods).iloc[:,0])

    df['bb_mid'] = df.groupby(level = 1)['adj close'].transform(lambda x : pandas_ta.bbands(close = np.log1p(x),
                                                                             length = periods).iloc[:,1])

    df['bb_high'] = df.groupby(level = 1)['adj close'].transform(lambda x : pandas_ta.bbands(close = np.log1p(x),
                                                                             length = periods).iloc[:,2])
    return df

  def atr(self, df, periods = 20):
    """ Create the ATR indicator"""
    def compute_atr(dataframe):
      atr = pandas_ta.atr(high = dataframe['high'],
                          low = dataframe['low'],
                          close = dataframe['close'],
                          length = periods)
      return atr.sub(atr.mean()).div(atr.std())

    df['atr'] = df.groupby(level = 1, group_keys = False).apply(compute_atr)
    return df

  def macd(self, df, periods = 20):
    """ Compute the MACD indicator """
    def compute_macd(dataframe):
      macd = pandas_ta.macd(close = dataframe['close'], length = periods).iloc[:, 0]
      return macd.sub(macd.mean()).div(macd.std())

    df['macd'] = df.groupby(level = 1, group_keys = False).apply(compute_macd)
    return df

  def dollar_volume(self, df):
    df['dollar_volume'] = (df['adj close'] * df['volume']) / 1e6
    return df

strategy = AlgoTradingStrategy('2023-09-27')

df = strategy.download_dataframe()

df_fixed = strategy.fixed_dataframe(df)

strategy.dollar_volume(df_fixed)