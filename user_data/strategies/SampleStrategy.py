# SampleStrategy for Freqtrade
# Simple RSI-based example strategy. Place this file in user_data/strategies/ and set --strategy SampleStrategy

from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib

class SampleStrategy(IStrategy):
    # Minimal timeframe required
    timeframe = '5m'

    # Minimal ROI designed for the example
    minimal_roi = {"0": 0.02}

    # Stoploss
    stoploss = -0.10

    # Trailing stoploss disabled in this simple example
    trailing_stop = False

    # Use hyperoptable parameters if desired

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Example indicator: RSI
        dataframe['rsi'] = talib.RSI(dataframe['close'], timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Buy when RSI < 30
        dataframe.loc[
            (
                dataframe['rsi'] < 30
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Sell when RSI > 70
        dataframe.loc[
            (
                dataframe['rsi'] > 70
            ),
            'exit_long'] = 1
        return dataframe
