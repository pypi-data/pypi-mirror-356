import pandas as pd
import numpy as np


def rsi(ohlc: pd.DataFrame, period: int = 14) -> pd.Series:
    """Implements the RSI indicator

    Args:
        - ohlc (pd.DataFrame):
        - period (int):

    Return:
        an pd.Series with the RSI indicator values
    """
    close = ohlc["CLOSE"]
    delta = close.diff()

    gain = (delta.where(delta > 0, 0)).ewm(alpha=1 / period).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1 / period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return pd.Series(rsi, index=ohlc.index)


def macd(
    ohlc: pd.DataFrame,
    short_period: int = 12,
    long_period: int = 26,
    signal_period: int = 9,
):
    close = ohlc["CLOSE"]
    short_ema = close.ewm(span=short_period, adjust=False).mean()
    long_ema = close.ewm(span=long_period, adjust=False).mean()

    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    return macd_line, signal_line


def bollinger_bands(ohlc: pd.DataFrame, period: int = 20, num_std: int = 2):
    close = ohlc["CLOSE"]
    sma = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()

    upper_band = sma + (num_std * std)
    lower_band = sma - (num_std * std)

    return upper_band, sma, lower_band


def adx(ohlc: pd.DataFrame, period: int = 14):
    high = ohlc["HIGH"]
    low = ohlc["LOW"]
    close = ohlc["CLOSE"]

    plus_dm = high.diff().where((high.diff() > low.diff()) & (high.diff() > 0), 0)
    minus_dm = low.diff().where((low.diff() > high.diff()) & (low.diff() > 0), 0)

    tr = pd.concat(
        [high - low, abs(high - close.shift()), abs(low - close.shift())], axis=1
    ).max(axis=1)

    atr = tr.rolling(window=period).mean()
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)

    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean()

    return adx


def sma(ohlc: pd.DataFrame, period: int):
    return ohlc["CLOSE"].rolling(window=period).mean()


def ema(ohlc: pd.DataFrame, period: int):
    return ohlc["CLOSE"].ewm(span=period, adjust=False).mean()


def atr(ohlc: pd.DataFrame, period: int = 14):
    high = ohlc["HIGH"]
    low = ohlc["LOW"]
    close = ohlc["CLOSE"]

    tr = pd.concat(
        [high - low, abs(high - close.shift()), abs(low - close.shift())], axis=1
    ).max(axis=1)
    atr = tr.rolling(window=period).mean()

    return atr


def stochastic(ohlc: pd.DataFrame, period: int = 14, k_slowing_period: int = 3):
    low_min = ohlc["LOW"].rolling(window=period).min()
    high_max = ohlc["HIGH"].rolling(window=period).max()

    k_percent = 100 * (ohlc["CLOSE"] - low_min) / (high_max - low_min)
    d_percent = k_percent.rolling(window=k_slowing_period).mean()  # Smoothed K

    return k_percent, d_percent


def mfi(ohlc: pd.DataFrame, period: int = 14):
    typical_price = (ohlc["HIGH"] + ohlc["LOW"] + ohlc["CLOSE"]) / 3
    money_flow = typical_price * ohlc["VOLUME"]

    positive_flow = money_flow.where(typical_price > typical_price.shift(), 0)
    negative_flow = money_flow.where(typical_price < typical_price.shift(), 0)

    positive_mf = positive_flow.rolling(window=period).sum()
    negative_mf = negative_flow.rolling(window=period).sum()

    mfi = 100 - (100 / (1 + (positive_mf / negative_mf)))

    return mfi


def fibonacci_retracement(high: float, low: float):
    diff = high - low
    levels = {
        "23.6%": high - diff * 0.236,
        "38.2%": high - diff * 0.382,
        "50.0%": high - diff * 0.5,
        "61.8%": high - diff * 0.618,
        "100%": low,
    }
    return levels


def ichimoku_cloud(ohlc: pd.DataFrame):
    high = ohlc["HIGH"]
    low = ohlc["LOW"]

    tenkan_sen = (high.rolling(window=9).max() + low.rolling(window=9).min()) / 2
    kijun_sen = (high.rolling(window=26).max() + low.rolling(window=26).min()) / 2
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    senkou_span_b = (
        (high.rolling(window=52).max() + low.rolling(window=52).min()) / 2
    ).shift(26)
    chikou_span = ohlc["CLOSE"].shift(26)

    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span


def parabolic_sar(ohlc: pd.DataFrame, af_step: float = 0.02, af_max: float = 0.2):
    high = ohlc["HIGH"]
    low = ohlc["LOW"]
    close = ohlc["CLOSE"]

    # Initialize the SAR series with the closing prices as a starting point
    sar = close.copy()

    # Define initial trend and extreme point
    trend_up = True
    ep = high.iloc[0] if trend_up else low.iloc[0]  # Extremum Price
    af = af_step  # Acceleration Factor

    # Iterate over the data points starting from the second row
    for i in range(1, len(ohlc)):
        prev_sar = sar.iloc[i - 1]  # Previous SAR value

        if trend_up:
            # Update SAR for an uptrend
            sar.iloc[i] = prev_sar + af * (ep - prev_sar)
            if low.iloc[i] < sar.iloc[i]:
                # Switch to downtrend if current low breaks the SAR
                trend_up = False
                sar.iloc[i] = ep
                ep = low.iloc[i]
                af = af_step
        else:
            # Update SAR for a downtrend
            sar.iloc[i] = prev_sar + af * (ep - prev_sar)
            if high.iloc[i] > sar.iloc[i]:
                # Switch to uptrend if current high breaks the SAR
                trend_up = True
                sar.iloc[i] = ep
                ep = high.iloc[i]
                af = af_step

        # Update the extremum price (EP) and acceleration factor (AF) based on the trend
        if trend_up:
            if high.iloc[i] > ep:
                ep = high.iloc[i]
                af = min(af + af_step, af_max)
        else:
            if low.iloc[i] < ep:
                ep = low.iloc[i]
                af = min(af + af_step, af_max)

    return sar


def chaikin_money_flow(ohlc: pd.DataFrame, period: int = 21):
    money_flow_multiplier = (
        (ohlc["CLOSE"] - ohlc["LOW"]) - (ohlc["HIGH"] - ohlc["CLOSE"])
    ) / (ohlc["HIGH"] - ohlc["LOW"])
    money_flow_volume = money_flow_multiplier * ohlc["VOLUME"]

    cmf = (
        money_flow_volume.rolling(window=period).sum()
        / ohlc["VOLUME"].rolling(window=period).sum()
    )

    return cmf


def pivot_points(ohlc: pd.DataFrame):
    high = ohlc["HIGH"]
    low = ohlc["LOW"]
    close = ohlc["CLOSE"]

    pivot = (high + low + close) / 3
    r1 = 2 * pivot - low
    s1 = 2 * pivot - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)

    return pivot, r1, s1, r2, s2


def volatility(
    ohlc: pd.DataFrame,
    period: int = 14,
):
    """
    Calculates rolling volatility for each stock based on the rolling standard deviation of returns.

    Parameters:
    - ohlc: pd.DataFrame containing stock data, including returns (RET) and stock identifier.
    - period: int, the rolling window period for volatility calculation (default is 14 days).

    Returns:
    - pd.Series representing the calculated volatility for each row in the DataFrame.
    """

    # Calculate returns based on CLOSE prices
    ret = ohlc["CLOSE"].pct_change()

    # Calculate rolling standard deviation of returns
    rolling_std = ret.rolling(window=period, min_periods=1).std()

    # Multiply by the square root of the period to scale volatility
    volatility = rolling_std * np.sqrt(period)

    return volatility


def cumulative_return(ohlc: pd.DataFrame, period: int = 14):
    """
    Calculates cumulative returns over the specified period using the 'CLOSE' price.

    Parameters:
    - ohlc: pd.DataFrame containing stock data, including 'CLOSE' column.
    - period: int, the number of days over which to calculate the cumulative return.

    Returns:
    - pd.Series representing the cumulative returns for each row in the DataFrame.
    """

    # Calculate cumulative return based on CLOSE prices
    cumul_ret = ohlc["CLOSE"].pct_change(period - 1)

    return cumul_ret


def close_diff(ohlc: pd.DataFrame):
    """
    Calculates the difference between consecutive close prices.

    Parameters:
    - ohlc: pd.DataFrame containing stock data with a 'CLOSE' column.

    Returns:
    - pd.Series representing the difference in closing prices.
    """
    return ohlc["CLOSE"].diff()


def obv(ohlc: pd.DataFrame):
    """
    Calculates On-Balance Volume (OBV) based on closing price differences and volume.

    Parameters:
    - ohlc: pd.DataFrame containing 'CLOSE', 'VOLUME' columns.

    Returns:
    - pd.Series representing the OBV values.
    """
    close_diff = ohlc["CLOSE"].diff()
    obv = (np.sign(close_diff) * ohlc["VOLUME"]).fillna(0).cumsum()
    return obv


def pressure(ohlc: pd.DataFrame):
    """
    Calculates both upward and downward pressure based on price movements.

    Parameters:
    - ohlc: pd.DataFrame containing 'OPEN', 'HIGH', 'LOW', and 'CLOSE' columns.

    Returns:
    - pd.DataFrame with 'UPWARD_PRESSURE' and 'DOWNWARD_PRESSURE' columns.
    """
    upward = (ohlc["LOW"] - ohlc["OPEN"]) / ohlc["OPEN"]
    downward = (ohlc["HIGH"] - ohlc["CLOSE"]) / ohlc["OPEN"]
    return upward, downward
