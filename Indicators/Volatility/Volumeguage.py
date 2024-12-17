import pandas as pd
import numpy as np


def calculate_indicators(data, atr_length=14, signal_threshold=1.5,
                         mom_length=14, mom_oversold=-1, mom_overbought=1,
                         volume_lookback=20, high_volume_threshold=1.2,
                         low_volume_threshold=0.8):
    """
    Calculates positive volatility, dynamic volume thresholds, and momentum oscillator.

    :param data: DataFrame with 'high', 'low', 'close', 'volume' columns.
    :param atr_length: Lookback period for ATR calculation.
    :param signal_threshold: Signal multiplier for positive volatility.
    :param mom_length: Lookback period for momentum calculation.
    :param mom_oversold: Oversold level for momentum.
    :param mom_overbought: Overbought level for momentum.
    :param volume_lookback: Lookback for average volume.
    :param high_volume_threshold: Multiplier for high volume detection.
    :param low_volume_threshold: Multiplier for low volume detection.
    :return: Updated DataFrame with calculated indicators.
    """
    # True Range (TR) calculation
    data['high-low'] = data['high'] - data['low']
    data['high-prev_close'] = abs(data['high'] - data['close'].shift(1))
    data['low-prev_close'] = abs(data['low'] - data['close'].shift(1))
    data['TR'] = data[['high-low', 'high-prev_close', 'low-prev_close']].max(axis=1)

    # Positive Real Volatility: Filter non-negative TR values
    data['positive_volatility'] = data['TR']

    # Signal Line w/safety check
    if len(data) >= atr_length:
        data['upper_signal'] = data['positive_volatility'].rolling(window=atr_length).mean() * signal_threshold
    else:
        data['upper_signal'] = np.nan


    # Average Volume and Volume Gauge w/safety check
    if len(data) >= volume_lookback:
        data['avg_volume'] = data['volume'].rolling(window=volume_lookback).mean()
        data['volume_gauge'] = np.where(data['avg_volume'] > 0, data['volume'] / data['avg_volume'], np.nan)
    else:
        data['volume_gauge'] = np.nan

    # Volume Threshold Color (logical flag)
    data['volume_color'] = np.select(
        [data['volume_gauge'] > high_volume_threshold, data['volume_gauge'] < low_volume_threshold],
        ['High', 'Low'],
        default='Medium'
    )

    # Momentum Oscillator w/safety check
    if len(data) >= mom_length:
        data['momentum'] = data['close'].diff(periods=mom_length)
    else:
        data['momentum'] = np.nan

    #Static Oversold/Overbought Levels
    data['mom_oversold'] = mom_oversold
    data['mom_overbought'] = mom_overbought

    return data[['positive_volatility', 'upper_signal', 'volume_gauge', 'volume_color',
                 'momentum', 'mom_oversold', 'mom_overbought']]
