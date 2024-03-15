# Inspired by  Algorithmic Trading – Machine Learning & Quant Strategies Course with Python by freeCodeCamp.org
!pip install pandas-ta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas_datareader.data as web
import yfinance as yf
from statsmodels.regression.rolling import RollingOLS
import datetime as dt
import pandas_ta

class DataFrame:
  def __init__(self, end_date):
    """ Instantiate the strategy by downloading the SP500 companies, and set the time window of your backtest"""
    self.stock_link = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    self.stock_symbols = pd.read_html(self.stock_link)[0]['Symbol'].str.replace('.', '-', regex = False).unique().tolist()
    self.end_date = end_date
    self.start_date = pd.to_datetime(end_date) - pd.DateOffset(365*8)

  def __str__(self):
    return "This is my first algorithmic trading strategy"

  def _download_dataframe(self):
    """ Download companies in the given timeframe using yahoo finance"""
    return yf.download(tickers = self.stock_symbols,
                                 start = self.start_date,
                                 end = self.end_date)

  def _fixed_dataframe(self, dataframe):
    """ Apply some data cleaning """
    dataframe = dataframe.stack()
    dataframe.index.names = ['date', 'ticker']
    dataframe.columns = dataframe.columns.str.lower()
    return dataframe

  def get_dataframe(self):
    self.dataframe = self._download_dataframe()
    self.dataframe = self._fixed_dataframe(self.dataframe)

  def _garman_klass(self):
    """ Create the Garman-Klass indicator """
    self.dataframe['garman_klass'] = ((np.log(self.dataframe['high']) - np.log(self.dataframe['low']))**2) / 2 - \
                            (2 * np.log(2) - 1) * (np.log(self.dataframe['adj close']) - np.log(self.dataframe['open']))**2

  def _rsi(self, periods = 20):
    """ Create the RSI indicator """
    self.dataframe['rsi'] = self.dataframe.groupby(level = 1)['adj close'].transform(lambda x : pandas_ta.rsi(close = x,
                                                                                      length = periods))

  def _bollinger_bands(self, periods = 20):
    """ Create the bollinger bands"""
    self.dataframe['bb_low'] = self.dataframe.groupby(level = 1)['adj close'].transform(lambda x : pandas_ta.bbands(close = np.log1p(x),
                                                                             length = periods).iloc[:,0])

    self.dataframe['bb_mid'] = self.dataframe.groupby(level = 1)['adj close'].transform(lambda x : pandas_ta.bbands(close = np.log1p(x),
                                                                             length = periods).iloc[:,1])

    self.dataframe['bb_high'] = self.dataframe.groupby(level = 1)['adj close'].transform(lambda x : pandas_ta.bbands(close = np.log1p(x),
                                                                             length = periods).iloc[:,2])

  def _atr(self, periods = 20):
    """ Create the ATR indicator"""
    def _compute_atr(dataframe):
      atr = pandas_ta.atr(high = dataframe['high'],
                          low = dataframe['low'],
                          close = dataframe['close'],
                          length = periods)
      return atr.sub(atr.mean()).div(atr.std())

    self.dataframe['atr'] = self.dataframe.groupby(level = 1, group_keys = False).apply(_compute_atr)

  def _macd(self, periods = 20):
    """ Compute the MACD indicator """
    def _compute_macd(dataframe):
      macd = pandas_ta.macd(close = dataframe['close'], length = periods).iloc[:, 0]
      return macd.sub(macd.mean()).div(macd.std())

    self.dataframe['macd'] = self.dataframe.groupby(level = 1, group_keys = False).apply(_compute_macd)

  def _dollar_volume(self):
    """ Get the liquidity indicator """
    self.dataframe['dollar_volume'] = (self.dataframe['adj close'] * self.dataframe['volume']) / 1e6

  def get_tech_indicators(self, lista: list, liquidity = False):
    """ Get the techincal indicators, whichever you want """
    # Create a key value pair, so that for each indicator's name you have the corresponding functions
    indicators_map = {
        "garman_klass": self._garman_klass,
        "rsi": self._rsi,
        "bollinger_bands": self._bollinger_bands,
        "atr": self._atr,
        "macd": self._macd,
    }

    if liquidity == True:
      # Add the liquidity indicator
      self._dollar_volume()

    # Run each indicator in the list
    for indicator in lista:
        if indicator in indicators_map:
            indicators_map[indicator]()

  def get_monthly_data(self):
    """ Get the average monthly liquidity and monthly indicators, taking the last value per month """

    # Define the columns you want to keep, which are the indicators
    last_cols = [c for c in self.dataframe.columns.unique(0) if c not in ['dollar_volume', 'volume', 'open', 'high', 'low', 'close']]

    avg_dollar_volume = self.dataframe['dollar_volume'].unstack('ticker').resample('M').mean().stack('ticker').to_frame('dollar_volume')

    # Keep the last value per each month, per each ticker for selected columns
    last_values = self.dataframe.unstack()[last_cols].resample('M').last().stack('ticker')

    # Concatenate the calculated values
    self.dataframe = pd.concat([avg_dollar_volume, last_values], axis=1).dropna()

  def filtering(self):
    """ Calculate the 5-year rolling average of dollar volume for each stock and filter in the first 150 most liquid companies """

    #  Calculate the dollar volume 5 years * 12 months rolling average
    self.dataframe['dollar_volume_5'] = (self.dataframe['dollar_volume'].unstack('ticker').rolling(5*12).mean().stack())

    # Rank the stock based on the 5-year rolling average
    self.dataframe['dollar_volume_5_rank'] = (self.dataframe.groupby('date')['dollar_volume_5'].rank(ascending =False))

    # Filter the first 150 most liquid companies
    self.dataframe = self.dataframe[self.dataframe['dollar_volume_5_rank'] < 150].drop(['dollar_volume', 'dollar_volume_5', 'dollar_volume_5_rank'], axis=1)

  def returns(self, lags_in_month: list = [1, 2, 3, 6, 9, 12], outlier_cutoff = 0):
    """ Calculate monthly returns considering different lags"""

    def _calculate_returns(data):

      # For each lag of the month, calculate the return
      for lag in lags_in_month:

          data[f'return_{lag}m'] = (data['adj close']
                                .pct_change(lag)
                                .pipe(lambda x: x.clip(lower=x.quantile(outlier_cutoff),
                                                      upper=x.quantile(1-outlier_cutoff)))
                                .add(1)
                                .pow(1/lag)
                                .sub(1))
      return data

    self.dataframe = self.dataframe.groupby(level=1, group_keys=False).apply(_calculate_returns).dropna()

strategy = DataFrame('2023-09-27')
strategy.get_dataframe()
strategy.get_tech_indicators(["rsi", "macd"], liquidity = True)
strategy.get_monthly_data()
strategy.filtering()
strategy.returns(outlier_cutoff = 0.005)
