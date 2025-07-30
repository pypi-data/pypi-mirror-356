#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import argrelextrema
from itertools import product
import os
from collections import defaultdict

from lecrapaud.config import PYTHON_ENV
from lecrapaud.utils import logger
from lecrapaud.directory_management import data_dir
from lecrapaud.services.indicators import (
    rsi,
    macd,
    bollinger_bands,
    adx,
    atr,
    stochastic,
    mfi,
    ichimoku_cloud,
    parabolic_sar,
    chaikin_money_flow,
    pivot_points,
    sma,
    ema,
    volatility,
    cumulative_return,
    close_diff,
    obv,
    pressure,
)
from lecrapaud.db import Target


# pd print options
# pd.set_option("display.max_columns", None)
# pd.reset_option("display.max_rows")
# pd.set_option("display.max_colwidth", None)


# Main function to create targets
def targets_creation(
    df: pd.DataFrame,
    top_x_stock: float = 0.1,
    local_max_order: int = 10,
    threshold: int = 5,
):
    """Preprocessing the stock data from yfinance

    Args:
        df (pd.DataFrame): a dataframe obtain with `get_data` function
        top_x_stock (float): the % at which you are considered top ranked stock for the day
        local_max_order (int): this set up the window to look at on both side of the extrema : the greater, the more 'global' is the extrema.

    Returns:
        df with more columns:
            - date variables : we create YEAR, MONTH, DAY, WEEK, WEEKDAY, YEARWEEK and YEARDAY features
            - return, market return, residual return and similar computation with volume are done to create 6 new features
            - target variables :
                - TARGET_1 : next day return
                - TARGET_2 : categorical return (positive 1, or negative 0)
                - TARGET_3 : next day ranking from best (1) to worst (n_stock) returns
                - TARGET_4 : categorical next day top ranking (in top_x_stock) (1), or not (0)
                - TARGET_5, TARGET_6, TARGET_7, TARGET_8 : same but with residual return
                - TARGET_9 : categorical with 1 if it's a local maximum and 0 if not
                - TARGET_10 : categorical with 1 if it's a local minimum and 0 if not
                - TARGET 11 : We will create trading signals based on proximity to local minima and maxima : need multi-binary loss support
                - TARGET 12, 13, 14 : return in 9,14,21 days


    """

    # Creating targets
    logger.info("Creating target variables...")

    # TARGET 1-4 : We start with target RET
    target = "RET"
    stock_column = "STOCK"
    nb_of_stocks = len(df[stock_column].unique())

    first_x_percent = max(int(nb_of_stocks * top_x_stock), 1)

    df["TARGET_1"] = df[target].shift(-1)
    df["TARGET_2"] = np.select([df["TARGET_1"] <= 0, df["TARGET_1"] > 0], [0, 1])
    df["TARGET_3"] = df.groupby("DATE")["TARGET_1"].rank(
        method="first", ascending=False
    )
    df["TARGET_4"] = np.select(
        [
            df.groupby("DATE")["TARGET_1"].rank(method="first", ascending=False)
            <= first_x_percent
        ],
        [1],
        default=0,
    )

    # TARGET 5-8 : We do the same for RESIDUAL_RET
    target = "RESIDUAL_RET"

    df["TARGET_5"] = df[target].shift(-1)
    df["TARGET_6"] = np.select([df["TARGET_5"] <= 0, df["TARGET_5"] > 0], [0, 1])
    df["TARGET_7"] = df.groupby("DATE")["TARGET_5"].rank(
        method="first", ascending=False
    )
    df["TARGET_8"] = np.select(
        [
            df.groupby("DATE")["TARGET_5"].rank(method="first", ascending=False)
            <= first_x_percent
        ],
        [1],
        default=0,
    )

    # TARGET 9-10 : Let's look at local min and max : it can be interpretate as buy and sell signal respectively
    target = "CLOSE"

    df["TARGET_9"] = 0
    df["TARGET_10"] = 0

    # Calculate local maxima and set TARGET_9 to 1 where maxima are found
    maxima_indices = df.groupby(stock_column)[target].transform(
        lambda x: x.index.isin(
            x.iloc[argrelextrema(x.values, np.greater, order=local_max_order)].index
        )
    )

    minima_indices = df.groupby(stock_column)[target].transform(
        lambda x: x.index.isin(
            x.iloc[argrelextrema(x.values, np.less, order=local_max_order)].index
        )
    )

    df.loc[maxima_indices, "TARGET_9"] = 1
    df.loc[minima_indices, "TARGET_10"] = 1

    # TARGET 11 : We will create trading signals based on proximity to local minima and maxima.
    df["TARGET_11"] = 2  # Default value for HOLD

    # Function to detect local minima and maxima, and assign signals
    def assign_signals(group):
        close_prices = group[target].values
        dates = group["DATE"].values

        # Detect local maxima and minima using argrelextrema
        local_maxima_idx = argrelextrema(
            close_prices, np.greater, order=local_max_order
        )[0]
        local_minima_idx = argrelextrema(close_prices, np.less, order=local_max_order)[
            0
        ]

        # STRONG BUY (4) for local minima, STRONG SELL (0) for local maxima
        group.loc[group.index[local_minima_idx], "TARGET_11"] = 4
        group.loc[group.index[local_maxima_idx], "TARGET_11"] = 0

        # Assign BUY (3) and SELL (1) based on proximity to extrema within the threshold window
        for idx in local_minima_idx:
            # Get the actual date of the minima
            min_date = dates[idx]
            # Select the rows within the threshold window around the minima date
            buy_window = group.loc[
                (group["DATE"] >= min_date - pd.Timedelta(days=threshold))
                & (group["DATE"] <= min_date + pd.Timedelta(days=threshold))
            ]
            group.loc[buy_window.index, "TARGET_11"] = np.where(
                buy_window["DATE"] == min_date,
                4,
                3,  # STRONG BUY at minima, BUY near minima
            )

        for idx in local_maxima_idx:
            # Get the actual date of the maxima
            max_date = dates[idx]
            # Select the rows within the threshold window around the maxima date
            sell_window = group.loc[
                (group["DATE"] >= max_date - pd.Timedelta(days=threshold))
                & (group["DATE"] <= max_date + pd.Timedelta(days=threshold))
            ]
            group.loc[sell_window.index, "TARGET_11"] = np.where(
                sell_window["DATE"] == max_date,
                0,
                1,  # STRONG SELL at maxima, SELL near maxima
            )

        return group

    # Apply the function to each stock group
    df = df.groupby(stock_column, group_keys=False).apply(assign_signals)

    # TARGET 12, 13, 14 : return in 9,14,21 days
    df["TARGET_12"] = df.groupby("STOCK")["CLOSE"].pct_change(9).shift(-9)
    df["TARGET_13"] = df.groupby("STOCK")["CLOSE"].pct_change(14).shift(-14)
    df["TARGET_14"] = df.groupby("STOCK")["CLOSE"].pct_change(21).shift(-21)

    # Update database
    # TODO: in bulk
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_1",
        type="regression",
        description="Next day return",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_2",
        type="classification",
        description="Next day return",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_3",
        type="regression",
        description="Ranking of next day return",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_4",
        type="classification",
        description="Top ranking of next day return",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_5",
        type="regression",
        description="Next day residual return",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_6",
        type="classification",
        description="Next day residual return",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_7",
        type="regression",
        description="Ranking of next day residual return",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_8",
        type="classification",
        description="Top ranking of next day residual return",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_9",
        type="classification",
        description="Local maxima",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_10",
        type="classification",
        description="Local minima",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_11",
        type="classification",
        description="Trading signals based on proximity to local minima and maxima",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_12",
        type="regression",
        description="Return in 9 days",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_13",
        type="regression",
        description="Return in 14 days",
    )
    Target.upsert(
        match_fields=["name", "type"],
        name="TARGET_14",
        type="regression",
        description="Return in 21 days",
    )

    return df


def calculate_option_features(option_data: list[dict], spot_price: float):
    puts = [opt for opt in option_data if opt["type"] == "put"]
    calls = [opt for opt in option_data if opt["type"] == "call"]

    def safe_float(x):
        try:
            return float(x)
        except:
            return 0.0

    # Convert and clean data
    for opt in option_data:
        for key in ["strike", "volume", "open_interest", "delta", "implied_volatility"]:
            opt[key] = safe_float(opt.get(key, 0.0))

    # Put/Call ratios
    total_put_vol = sum(p["volume"] for p in puts)
    total_call_vol = sum(c["volume"] for c in calls)
    total_put_oi = sum(p["open_interest"] for p in puts)
    total_call_oi = sum(c["open_interest"] for c in calls)

    put_call_ratio_vol = total_put_vol / total_call_vol if total_call_vol > 0 else None
    put_call_ratio_oi = total_put_oi / total_call_oi if total_call_oi > 0 else None

    # Open Interest Skew
    oi_skew = sum(c["open_interest"] for c in calls if c["strike"] > spot_price) - sum(
        p["open_interest"] for p in puts if p["strike"] < spot_price
    )

    # Total Open Interest
    total_oi = sum(opt["open_interest"] for opt in option_data)

    # Delta-weighted Put/Call Ratio
    dw_put = sum(p["delta"] * p["volume"] for p in puts)
    dw_call = sum(c["delta"] * c["volume"] for c in calls)
    delta_weighted_pcr = dw_put / dw_call if dw_call > 0 else None

    # ATM IV
    atm_option = min(option_data, key=lambda x: abs(x["strike"] - spot_price))
    atm_iv = atm_option["implied_volatility"]

    # IV Skew (25-delta)
    iv_put_25d = np.mean(
        [p["implied_volatility"] for p in puts if abs(p["delta"] + 0.25) < 0.05]
    )
    iv_call_25d = np.mean(
        [c["implied_volatility"] for c in calls if abs(c["delta"] - 0.25) < 0.05]
    )
    iv_skew_25d = iv_put_25d - iv_call_25d if iv_put_25d and iv_call_25d else None

    # IV Term Structure
    iv_by_exp = defaultdict(list)
    for opt in option_data:
        iv_by_exp[opt["expiration"]].append(opt["implied_volatility"])
    expiries = sorted(iv_by_exp.keys())
    if len(expiries) >= 2:
        iv_term_structure = np.mean(iv_by_exp[expiries[-1]]) - np.mean(
            iv_by_exp[expiries[0]]
        )
    else:
        iv_term_structure = None

    # Moneyness
    moneyness = [spot_price / opt["strike"] for opt in option_data if opt["strike"] > 0]

    # % OTM / ITM
    otm_calls = [c for c in calls if c["strike"] > spot_price]
    otm_puts = [p for p in puts if p["strike"] < spot_price]
    otm = len(otm_calls) + len(otm_puts)
    itm = len(option_data) - otm
    percent_otm = otm / len(option_data) if option_data else None
    percent_itm = itm / len(option_data) if option_data else None

    # Weighted Average Strike
    def weighted_avg_strike(options):
        total_vol = sum(o["volume"] for o in options)
        return (
            sum(o["strike"] * o["volume"] for o in options) / total_vol
            if total_vol > 0
            else None
        )

    avg_strike_calls = weighted_avg_strike(calls)
    avg_strike_puts = weighted_avg_strike(puts)

    # Option Sentiment Index
    sentiment_numerator = sum(
        c["volume"] for c in calls if c["strike"] < spot_price
    ) - sum(p["volume"] for p in puts if p["strike"] > spot_price)
    sentiment_index = (
        sentiment_numerator / (total_put_vol + total_call_vol)
        if (total_put_vol + total_call_vol) > 0
        else None
    )

    return {
        "put_call_ratio_volume": put_call_ratio_vol,
        "put_call_ratio_open_interest": put_call_ratio_oi,
        "open_interest_skew": oi_skew,
        "total_open_interest": total_oi,
        "delta_weighted_pcr": delta_weighted_pcr,
        "atm_iv": atm_iv,
        "iv_skew_25d": iv_skew_25d,
        "iv_term_structure": iv_term_structure,
        "average_moneyness": np.mean(moneyness) if moneyness else None,
        "percent_otm": percent_otm,
        "percent_itm": percent_itm,
        "weighted_avg_strike_calls": avg_strike_calls,
        "weighted_avg_strike_puts": avg_strike_puts,
        "option_sentiment_index": sentiment_index,
    }


def apply_indicators(df: pd.DataFrame):
    """Apply multiple indicators to a grouped dataframe of a single stock."""
    # Assuming 'df' is the OHLC data for a single stock, apply indicators
    result = df.copy()

    logger.debug(f"Computing non-period features...")

    # Apply Parabolic SAR
    result["Parabolic_SAR"] = parabolic_sar(df)

    # Apply Bollinger Bands
    result["Upper_BB"], result["Middle_BB"], result["Lower_BB"] = bollinger_bands(df)

    # Apply Ichimoku Cloud
    (
        result["Tenkan"],
        result["Kijun"],
        result["Senkou_A"],
        result["Senkou_B"],
        result["Chikou"],
    ) = ichimoku_cloud(df)

    # Apply Pivot Points (including support and resistance levels)
    result["Pivot"], result["R1"], result["S1"], result["R2"], result["S2"] = (
        pivot_points(df)
    )

    # Other indicators
    result["CLOSE_DIFF"] = close_diff(df)
    result["OBV"] = obv(df)
    result["DOWNWARD_PRESSURE"], result["UPWARD_PRESSURE"] = pressure(df)

    # Apply MACD (Moving Average Convergence Divergence)
    result["MACD_Line"], result["MACD_Signal"] = macd(df)

    # first buy/sell signal : MACD_SIGNAL_DIFF cross 0 levels
    result["MACD_SIGNAL_DIFF"] = result["MACD_Line"] - result["MACD_Signal"]
    result["BUY_1"] = np.where(
        (result["MACD_SIGNAL_DIFF"] > 0)
        & (result["MACD_SIGNAL_DIFF"].shift(1) < 0),  # Buy signal (MACD crossover)
        1,  # Buy
        np.where(
            (result["MACD_SIGNAL_DIFF"] < 0)
            & (
                result["MACD_SIGNAL_DIFF"].shift(1) > 0
            ),  # Sell signal (MACD crossunder)
            -1,  # Sell
            np.nan,  # Default case
        ),
    )
    result["BUY_1"] = result["BUY_1"].fillna(0)  # TODO: should we fill with 0 (done)

    # second buy/sell signal : MACD_SIGNAL_DIFF cross 30% threshold of maximum value while positive and decreasing, or 30% threshold of minimum value while negative and increasing
    # Calculate rolling 20-day max and min values for MACD_SIGNAL_DIFF per stock
    macd_signal_diff_max_20_days = result.groupby("STOCK")[
        "MACD_SIGNAL_DIFF"
    ].transform(lambda x: x.rolling(20).max())
    macd_signal_diff_min_20_days = result.groupby("STOCK")[
        "MACD_SIGNAL_DIFF"
    ].transform(lambda x: x.rolling(20).min())

    # Define the buy/sell signal conditions
    buy_condition = (
        (result["MACD_SIGNAL_DIFF"] > result["MACD_SIGNAL_DIFF"].shift(1))  # Increasing
        & (result["MACD_SIGNAL_DIFF"] < 0)  # Negative value
        & (
            result["MACD_SIGNAL_DIFF"] > 0.3 * macd_signal_diff_min_20_days
        )  # Above 30% of minimum
    )

    sell_condition = (
        (result["MACD_SIGNAL_DIFF"] < result["MACD_SIGNAL_DIFF"].shift(1))  # Decreasing
        & (result["MACD_SIGNAL_DIFF"] > 0)  # Positive value
        & (
            result["MACD_SIGNAL_DIFF"] < 0.3 * macd_signal_diff_max_20_days
        )  # Below 30% of maximum
    )

    # Apply the conditions to calculate buy/sell signals
    result["BUY_2"] = np.where(
        buy_condition,
        np.abs(
            (result["MACD_SIGNAL_DIFF"] - 0.3 * macd_signal_diff_min_20_days)
            / (0.3 * macd_signal_diff_min_20_days)
        ),
        np.where(
            sell_condition,
            -np.abs(
                (result["MACD_SIGNAL_DIFF"] - 0.3 * macd_signal_diff_max_20_days)
                / (0.3 * macd_signal_diff_max_20_days)
            ),
            0,  # Default
        ),
    )

    periods = [
        9,
        14,
        21,
        50,
        126,
        200,
        252,
    ]  # 2 semaines, 3 semaines, 1 mois et 2.5 mois
    # TODO: on pourrait rajouter plus de long terme : 126 jours (6 mois) et 200 jours (9 mois) et 252 jours (1 an)

    features = []
    for period in periods:
        logger.debug(f"Computing period features for {period} days...")

        features.append(
            pd.DataFrame(
                {
                    f"CUMUL_RET_{period}": cumulative_return(df, period=period),
                    f"SMA_{period}": sma(df, period=period),
                    f"EMA_{period}": ema(df, period=period),
                    f"VOLATILITY_{period}": volatility(df, period=period),
                    f"ADX_{period}": adx(df, period=period),
                    f"ATR_{period}": atr(df, period=period),
                    f"CMF_{period}": chaikin_money_flow(df, period=period),
                    f"RSI_{period}": rsi(df, period=period),
                    f"MFI_{period}": mfi(df, period=period),
                },
                index=df.index,
            )
        )

        # Stochastic Oscillator returns two series: %K and %D
        k, d = stochastic(df, period=period)
        features.append(
            pd.DataFrame(
                {
                    f"%K_{period}": k,
                    f"%D_{period}": d,
                },
                index=df.index,
            )
        )

    result = pd.concat([result] + features, axis=1)

    # third buy/sell signal : RSI is overbought >0.7 / oversold <0.3
    result["BUY_3"] = np.where(
        result["RSI_14"] <= 30,
        (30 - result["RSI_14"]) / 30,
        np.where(result["RSI_14"] >= 70, -(result["RSI_14"] - 70) / 30, 0),
    )

    # fourth buy/sell signal : RSI vs CLOSE divergence
    # The RSI vs. Close divergence trading signal identifies potential reversals by detecting when the
    # Relative Strength Index (RSI) and price (Close) move in opposite directions
    # bullish divergence occurs when the price makes lower lows while RSI makes higher lows (potential uptrend),
    # and bearish divergence occurs when the price makes higher highs while RSI makes lower highs (potential downtrend)

    # Detect local peaks (RSI Highs) and troughs (RSI Lows) for divergence analysis
    # Compute local maxima and minima indices
    rsi_peak_indices = argrelextrema(result["RSI_14"].values, np.greater)[
        0
    ]  # RSI highs
    rsi_trough_indices = argrelextrema(result["RSI_14"].values, np.less)[0]  # RSI lows

    # Create boolean masks for peaks and troughs
    rsi_peaks_mask = np.zeros(len(result), dtype=bool)
    rsi_troughs_mask = np.zeros(len(result), dtype=bool)

    rsi_peaks_mask[rsi_peak_indices] = True
    rsi_troughs_mask[rsi_trough_indices] = True

    # Extract peak and trough rows efficiently
    rsi_peaks = result.loc[rsi_peaks_mask, ["CLOSE", "RSI_14"]].copy()
    rsi_troughs = result.loc[rsi_troughs_mask, ["CLOSE", "RSI_14"]].copy()

    # Compute RSI and CLOSE differences to check divergence
    for i in [1, 2, 3]:
        # RSI & Price difference from past peaks
        rsi_peaks[f"RSI_PEAK_DIFF_{i}"] = rsi_peaks["RSI_14"].diff(i)
        rsi_peaks[f"PRICE_PEAK_DIFF_{i}"] = rsi_peaks["CLOSE"].diff(i)

        # RSI & Price difference from past troughs
        rsi_troughs[f"RSI_TROUGH_DIFF_{i}"] = rsi_troughs["RSI_14"].diff(i)
        rsi_troughs[f"PRICE_TROUGH_DIFF_{i}"] = rsi_troughs["CLOSE"].diff(i)

        # Detect bearish divergence (RSI down, price up) and bullish divergence (RSI up, price down)
        rsi_peaks[f"DIVERGENCE_{i}"] = np.where(
            (rsi_peaks[f"RSI_PEAK_DIFF_{i}"] < 0)
            & (rsi_peaks[f"PRICE_PEAK_DIFF_{i}"] > 0),
            -np.abs(rsi_peaks[f"RSI_PEAK_DIFF_{i}"]),
            np.where(
                (rsi_peaks[f"RSI_PEAK_DIFF_{i}"] > 0)
                & (rsi_peaks[f"PRICE_PEAK_DIFF_{i}"] < 0),
                -np.abs(rsi_peaks[f"RSI_PEAK_DIFF_{i}"]),
                0,
            ),
        )

        rsi_troughs[f"DIVERGENCE_{i}"] = np.where(
            (rsi_troughs[f"RSI_TROUGH_DIFF_{i}"] > 0)
            & (rsi_troughs[f"PRICE_TROUGH_DIFF_{i}"] < 0),
            np.abs(rsi_troughs[f"RSI_TROUGH_DIFF_{i}"]),
            np.where(
                (rsi_troughs[f"RSI_TROUGH_DIFF_{i}"] < 0)
                & (rsi_troughs[f"PRICE_TROUGH_DIFF_{i}"] > 0),
                np.abs(rsi_troughs[f"RSI_TROUGH_DIFF_{i}"]),
                0,
            ),
        )

    # Concatenate peak and trough divergences into a single DataFrame
    divergence_cols = [f"DIVERGENCE_{i}" for i in [1, 2, 3]]
    divergence_data = pd.concat(
        [rsi_peaks[divergence_cols], rsi_troughs[divergence_cols]], axis=0
    )

    # Merge using index alignment
    result[divergence_cols] = divergence_data.reindex(result.index, fill_value=0)

    # Sum divergence signals into BUY_4 for a single signal strength metric
    result["BUY_4"] = result[divergence_cols].sum(axis=1)
    return result


# Main function to process the full dataset with multiple stocks
def preprocessing(
    df: pd.DataFrame,
    for_training: bool = False,
    save_as_csv: bool = False,
):
    """Main function to process the full dataset with multiple stocks

    Args:
        - df (pd.DataFrame): the dataframe with ohlc data
        - for_training (bool): whether to compute targets and for_training as data_for_training, or not.
    """

    # Computing residual RET and relative VOLUME
    logger.info("Creating RET and VOLUME metrics...")
    df["RET"] = df.groupby("STOCK")["CLOSE"].pct_change(1)
    df["MARKET_RET"] = df.groupby("DATE")["RET"].transform("mean")
    df["RESIDUAL_RET"] = df["RET"] - df["MARKET_RET"]

    df["VOLUME_RATIO"] = (
        df["VOLUME"]
        / df.groupby("STOCK")["VOLUME"].rolling(20, min_periods=1).mean().values
    )
    df["MARKET_VOLUME_RATIO"] = df.groupby("DATE")["VOLUME_RATIO"].transform("mean")
    df["RELATIVE_VOLUME"] = df["VOLUME_RATIO"] - df["MARKET_VOLUME_RATIO"]

    logger.info("Creating historical time series metrics...")
    periods = [
        1,  # daily
        2,
        3,
        4,
        5,  # weekly
        9,
        14,
        21,  # monthly
        50,
        126,
        200,
        252,
    ]  # need to keep 1, 2, 3, 4, 5 for backward compatibility
    for METRIC in ["RET", "VOLUME", "RESIDUAL_RET", "RELATIVE_VOLUME"]:
        for i in periods:
            df[f"{METRIC}_-{i}"] = df[METRIC].shift(i)

    # Group by "STOCK" and apply the indicators for each stock
    logger.info("Applying indicators...")
    grouped_df = df.groupby("STOCK", group_keys=False)
    preprocessed_df = grouped_df.apply(apply_indicators)

    # Drop non-useful column for training
    if "ISIN" in df.columns:
        df.drop(labels=["ISIN"], axis=1, inplace=True)
    if "SECURITY" in df.columns:
        df.drop(labels=["SECURITY"], axis=1, inplace=True)

    if for_training:
        preprocessed_df = targets_creation(preprocessed_df)

    if save_as_csv and PYTHON_ENV == "Development":
        preprocessed_df_to_csv = preprocessed_df.sort_values(["DATE", "STOCK"])
        preprocessed_df_to_csv.to_csv(
            f"{data_dir}/data_for_training.csv",
            index=False,
            header=True,
        )

    if for_training:
        preprocessed_df.dropna(inplace=True)

    preprocessed_df.sort_values(["DATE", "STOCK"], inplace=True)
    preprocessed_df.reset_index(drop=True, inplace=True)

    logger.info(
        f"{len(preprocessed_df['DATE'])} preprocessed data with shape {preprocessed_df.shape} from {datetime.strftime(preprocessed_df['DATE'].iat[0], '%d/%m/%Y')} to {datetime.strftime(preprocessed_df['DATE'].iat[-1], '%d/%m/%Y')}"
    )

    # for_training results if needed
    if for_training and PYTHON_ENV == "Development":
        joblib.dump(preprocessed_df, f"{data_dir}/data_for_training.pkl")

    # Return the fully processed DataFrame with all new features (copy to avoid fragmented memory)
    return_df = preprocessed_df.copy()
    return return_df


# Descriptive Analytics functions


def plot_sector_repartition(df: pd.DataFrame):
    """Visualise repartition of stock per sectors

    Args:
        df (pd.DataFrame): a df created with `get_data`
    """
    sns.barplot(
        data=df.groupby("SECTOR")["STOCK"].nunique(),
        orient="h",
        order=df.groupby("SECTOR")["STOCK"]
        .nunique()
        .sort_values(ascending=False)
        .index,
    )


def visualize_extrema(
    data: pd.DataFrame,
    stock: str,
    days_before_last: int = 200,
    local_max_order: int = 10,
):
    """
    Function to visualize local maxima and minima for a given stock in the data.

    Parameters:
    - data: pd.DataFrame, DataFrame containing columns 'STOCK', 'DATE', 'CLOSE', and 'ID'
    - stock: str, the stock identifier to analyze (e.g., 'AAPL', 'GOOG')
    - days_before_last: int, number of days before the last date in the dataset to visualize
    - local_max_order: int, the window size for identifying local extrema (default: 5)
    """

    # Calculate the last date in the dataset
    last_date = data["DATE"].max()
    start_date = last_date - pd.Timedelta(days=days_before_last)

    # Find local maxima (argrelextrema with np.greater) for each stock
    local_max_CLOSE = (
        data[data["STOCK"] == stock]
        .set_index("DATE")["CLOSE"]
        .iloc[
            argrelextrema(
                data[data["STOCK"] == stock]["CLOSE"].values,
                np.greater,
                order=local_max_order,
            )
        ]
        .reset_index()
    )

    # Find local minima (argrelextrema with np.less) for each stock
    local_min_CLOSE = (
        data[data["STOCK"] == stock]
        .set_index("DATE")["CLOSE"]
        .iloc[
            argrelextrema(
                data[data["STOCK"] == stock]["CLOSE"].values,
                np.less,
                order=local_max_order,
            )
        ]
        .reset_index()
    )

    # Filter maxima based on stock and date range
    local_max_CLOSE = local_max_CLOSE[local_max_CLOSE["DATE"] >= start_date]

    # Filter minima based on stock and date range
    local_min_CLOSE = local_min_CLOSE[local_min_CLOSE["DATE"] >= start_date]

    # logger.info the maxima and minima dates
    logger.info(
        f"Maxima Dates for Stock {stock}: {list(local_max_CLOSE['DATE'].values)}"
    )
    logger.info(
        f"Minima Dates for Stock {stock}: {list(local_min_CLOSE['DATE'].values)}"
    )

    # Plot the stock's CLOSE prices within the specified date range
    stock_data = data[(data["STOCK"] == stock) & (data["DATE"] >= start_date)][
        ["CLOSE", "DATE"]
    ].set_index("DATE")

    plt.figure(figsize=(10, 6))
    stock_data.plot(color="black", title=f"Stock {stock} Extremas")

    # Add vertical lines for maxima
    for date in local_max_CLOSE["DATE"].values:
        plt.axvline(
            x=date,
            color="red",
            label="Maxima" if date == local_max_CLOSE["DATE"].values[0] else "",
        )

    # Add vertical lines for minima
    for date in local_min_CLOSE["DATE"].values:
        plt.axvline(
            x=date,
            color="green",
            label="Minima" if date == local_min_CLOSE["DATE"].values[0] else "",
        )

    plt.legend()
    plt.show()


def visualize_trading_signals(
    data: pd.DataFrame,
    stock: str,
    days_before_last: int = 200,
):
    """
    Function to visualize trading signals (BUY, SELL, HOLD) for a given stock.

    Parameters:
    - data: pd.DataFrame, DataFrame containing columns 'STOCK', 'DATE', 'CLOSE', and 'TRADING_SIGNAL'
    - stock: str, the stock identifier to analyze (e.g., 'AAPL', 'GOOG')
    - days_before_last: int, number of days before the last date in the dataset to visualize
    """

    # Calculate the last date in the dataset
    last_date = data["DATE"].max()
    start_date = last_date - pd.Timedelta(days=days_before_last)

    # Filter data for the selected stock and date range
    stock_data = data[(data["STOCK"] == stock) & (data["DATE"] >= start_date)].copy()

    # Plot the stock's CLOSE prices
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data["DATE"], stock_data["CLOSE"], color="black", label="CLOSE")

    # Define the colors for the trading signals
    colors = {2: "green", 1: "lightgreen", 0: "yellow", -1: "red", -2: "darkred"}

    # Plot each trading signal with the respective color
    for signal_value, color in colors.items():
        plt.scatter(
            stock_data.loc[stock_data["TARGET_11"] == signal_value, "DATE"],
            stock_data.loc[stock_data["TARGET_11"] == signal_value, "CLOSE"],
            color=color,
            label=f"Signal {signal_value}",
            s=50,  # Size of the points
        )

    plt.title(f"Trading Signals for {stock}")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid(True)
    plt.show()


def visualize_data_distribution(
    data,
    plot_type="hist",
    features=None,
    bins=50,
    rows=5,
    cols=5,
    width_per_plot=4,
    height_per_plot=3,
):
    """
    Function to visualize the data distribution for multiple features in a DataFrame with dynamic figsize,
    splitting into multiple figures if there are too many features for one figure.

    Parameters:
    - data: pd.DataFrame, the DataFrame containing the data to visualize.
    - plot_type: str, the type of plot to use ('hist', 'kde', 'box').
    - features: list, list of features (columns) to visualize. If None, all numeric features are used.
    - bins: int, the number of bins for histograms (default: 50).
    - rows: int, number of rows in the subplot grid (default: 5).
    - cols: int, number of columns in the subplot grid (default: 5).
    - width_per_plot: int, the width of each subplot (default: 4).
    - height_per_plot: int, the height of each subplot (default: 3).
    """

    # If no features are specified, use all numeric features
    if features is None:
        features = data.select_dtypes(include=[np.number]).columns.tolist()

    # Calculate the total number of features
    total_features = len(features)

    # How many plots can fit into one figure
    plots_per_figure = rows * cols

    # Loop over the features and create new figures as needed
    for start in range(0, total_features, plots_per_figure):
        # Subset of features for the current figure
        subset_features = features[start : start + plots_per_figure]

        # Dynamically calculate figure size based on grid size and plot dimensions
        num_plots = len(subset_features)
        grid_rows = min(rows, num_plots // cols + (num_plots % cols != 0))
        grid_cols = min(cols, num_plots)
        figsize = (grid_cols * width_per_plot, grid_rows * height_per_plot)

        # Set up the figure and axes for this subset of features
        fig, axes = plt.subplots(grid_rows, grid_cols, figsize=figsize)
        axes = axes.flatten()  # Flatten the axes for easy iteration

        # Plot each feature
        for i, feature in enumerate(subset_features):
            ax = axes[i]

            if plot_type == "hist":
                sns.histplot(data[feature].dropna(), bins=bins, kde=False, ax=ax)
            elif plot_type == "kde":
                sns.kdeplot(data[feature].dropna(), ax=ax, fill=True)
            elif plot_type == "box":
                sns.boxplot(data[feature].dropna(), ax=ax)

            ax.set_xlabel(feature)
            ax.set_ylabel("Count")

        # Hide any empty subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        # Use tight layout to ensure there's no overlap
        fig.tight_layout()

        # Show the plot for this figure
        plt.show()


def detect_outliers_iqr(data, degree: float = 1.5):
    """
    Detect outliers in a DataFrame using the Interquartile Range (IQR) method.

    Parameters:
    - data: pd.DataFrame, the DataFrame in which to detect outliers.

    Returns:
    - outliers: pd.DataFrame, DataFrame with boolean values indicating outliers for each feature.
    """
    outliers = pd.DataFrame(index=data.index)

    for column in data.select_dtypes(include=[np.number]).columns:
        Q1 = data[column].quantile(0.25)  # 1st quartile (25th percentile)
        Q3 = data[column].quantile(0.75)  # 3rd quartile (75th percentile)
        IQR = Q3 - Q1  # Interquartile range

        lower_bound = Q1 - degree * IQR
        upper_bound = Q3 + degree * IQR

        # Detect outliers
        outliers[column] = (data[column] < lower_bound) | (data[column] > upper_bound)

    return outliers


def plot_distribution(df):
    logger.info("DATA_DISTRIBUTION")

    logger.info("numerical features")
    visualize_data_distribution(df.select_dtypes(include=["float64"]))

    logger.info("categorical features")
    visualize_data_distribution(df.select_dtypes(include=["int64"]))

    logger.info("nb of outliers")
    outliers = detect_outliers_iqr(df.select_dtypes(include=["float64"]), degree=5)

    with pd.option_context("display.max_rows", None):
        logger.info(outliers.sum().sort_values(ascending=False))

    logger.info("zoom on volume outliers")
    columns = [c for c in df.columns if "VOLUME" in c]
    visualize_data_distribution(df, features=columns, plot_type="box", cols=3)
