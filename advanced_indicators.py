import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional

class AdvancedIndicators:
    @staticmethod
    def fibonacci_retracement(high: float, low: float) -> Dict[str, float]:
        """Calculate Fibonacci retracement levels"""
        diff = high - low
        levels = {
            '0.0': low,
            '0.236': low + 0.236 * diff,
            '0.382': low + 0.382 * diff,
            '0.5': low + 0.5 * diff,
            '0.618': low + 0.618 * diff,
            '0.786': low + 0.786 * diff,
            '1.0': high
        }
        return levels

    @staticmethod
    def ichimoku_cloud(df: pd.DataFrame, 
                      tenkan_period: int = 9,
                      kijun_period: int = 26,
                      senkou_span_b_period: int = 52) -> pd.DataFrame:
        """Calculate Ichimoku Cloud components"""
        # Tenkan-sen (Conversion Line)
        high_9 = df['High'].rolling(window=tenkan_period).max()
        low_9 = df['Low'].rolling(window=tenkan_period).min()
        df['tenkan_sen'] = (high_9 + low_9) / 2

        # Kijun-sen (Base Line)
        high_26 = df['High'].rolling(window=kijun_period).max()
        low_26 = df['Low'].rolling(window=kijun_period).min()
        df['kijun_sen'] = (high_26 + low_26) / 2

        # Senkou Span A (Leading Span A)
        df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(kijun_period)

        # Senkou Span B (Leading Span B)
        high_52 = df['High'].rolling(window=senkou_span_b_period).max()
        low_52 = df['Low'].rolling(window=senkou_span_b_period).min()
        df['senkou_span_b'] = ((high_52 + low_52) / 2).shift(kijun_period)

        # Chikou Span (Lagging Span)
        df['chikou_span'] = df['Close'].shift(-kijun_period)

        return df

    @staticmethod
    def on_balance_volume(df: pd.DataFrame) -> pd.Series:
        """Calculate On-Balance Volume (OBV)"""
        obv = pd.Series(index=df.index, dtype=float)
        obv.iloc[0] = df['Volume'].iloc[0]
        
        for i in range(1, len(df)):
            if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] + df['Volume'].iloc[i]
            elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] - df['Volume'].iloc[i]
            else:
                obv.iloc[i] = obv.iloc[i-1]
        
        return obv

    @staticmethod
    def money_flow_index(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Money Flow Index (MFI)"""
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        money_flow = typical_price * df['Volume']
        
        positive_flow = pd.Series(0.0, index=df.index)
        negative_flow = pd.Series(0.0, index=df.index)
        
        # Calculate positive and negative money flow
        for i in range(1, len(df)):
            if typical_price[i] > typical_price[i-1]:
                positive_flow[i] = money_flow[i]
            elif typical_price[i] < typical_price[i-1]:
                negative_flow[i] = money_flow[i]
        
        positive_mf = positive_flow.rolling(window=period).sum()
        negative_mf = negative_flow.rolling(window=period).sum()
        
        mfi = 100 - (100 / (1 + positive_mf / negative_mf))
        return mfi

    @staticmethod
    def stochastic_rsi(df: pd.DataFrame, period: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> pd.DataFrame:
        """Calculate Stochastic RSI"""
        # Calculate RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Calculate Stochastic RSI
        stoch_rsi = pd.Series(index=df.index, dtype=float)
        rsi_min = rsi.rolling(window=period).min()
        rsi_max = rsi.rolling(window=period).max()
        stoch_rsi = (rsi - rsi_min) / (rsi_max - rsi_min)
        
        # Calculate smoothed Stochastic RSI
        k = stoch_rsi.rolling(window=smooth_k).mean()
        d = k.rolling(window=smooth_d).mean()
        
        return pd.DataFrame({
            'K': k * 100,  # Fast stochastic
            'D': d * 100   # Slow stochastic
        })
