import pandas as pd
import numpy as np
import ta
from typing import Dict, Any

class TechnicalAnalysis:
    """Class for performing technical analysis"""
    
    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate common technical indicators"""
        if df.empty:
            return df
            
        try:
            # Calculate price momentum
            df['Price_Momentum'] = df['Close'].pct_change(5)  # 5-day momentum
            
            # Add RSI with multiple periods
            df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
            df['RSI_Trend'] = "Neutral"
            df.loc[df['RSI'] > 70, 'RSI_Trend'] = "Overbought"
            df.loc[df['RSI'] < 30, 'RSI_Trend'] = "Oversold"
            
            # Add MACD with standard settings
            macd = ta.trend.MACD(df['Close'])
            df['MACD'] = macd.macd()
            df['MACD_Signal'] = macd.macd_signal()
            df['MACD_Hist'] = macd.macd_diff()
            df['MACD_Trend'] = np.where(df['MACD'] > df['MACD_Signal'], "Bullish", "Bearish")
            
            # Bollinger Bands
            bollinger = ta.volatility.BollingerBands(df['Close'])
            df['BB_High'] = bollinger.bollinger_hband()
            df['BB_Low'] = bollinger.bollinger_lband()
            df['BB_Mid'] = bollinger.bollinger_mavg()
            df['BB_Width'] = (df['BB_High'] - df['BB_Low']) / df['BB_Mid']
            
            # Moving Averages
            df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
            df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
            df['EMA_20'] = ta.trend.ema_indicator(df['Close'], window=20)
            
            # Volume indicators
            df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
            df['Volume_Trend'] = df['Volume'] / df['Volume_SMA']
            
            # ATR for volatility
            df['ATR'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range()
            df['ATR_Pct'] = df['ATR'] / df['Close'] * 100
            
            # Trend strength indicators
            df['ADX'] = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close']).adx()
            df['Trend_Strength'] = "Weak"
            df.loc[df['ADX'] > 25, 'Trend_Strength'] = "Moderate"
            df.loc[df['ADX'] > 50, 'Trend_Strength'] = "Strong"
            
            # Support and Resistance levels using pivot points
            df['PP'] = (df['High'] + df['Low'] + df['Close']) / 3
            df['R1'] = 2 * df['PP'] - df['Low']
            df['S1'] = 2 * df['PP'] - df['High']
            df['R2'] = df['PP'] + (df['High'] - df['Low'])
            df['S2'] = df['PP'] - (df['High'] - df['Low'])
            
            return df
        except Exception as e:
            print(f"Error calculating indicators: {str(e)}")
            return df
    
    @staticmethod
    def analyze_trends(df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze current market trends"""
        if df.empty:
            return {}
            
        try:
            current_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]
            sma_20 = df['SMA_20'].iloc[-1]
            sma_50 = df['SMA_50'].iloc[-1]
            
            # Determine primary trend
            trend_direction = "Neutral"
            if current_price > sma_20 and sma_20 > sma_50:
                trend_direction = "Bullish"
            elif current_price < sma_20 and sma_20 < sma_50:
                trend_direction = "Bearish"
            
            # Calculate trend strength using ADX
            trend_strength = df['ADX'].iloc[-1]
            
            # Determine momentum
            momentum = df['Price_Momentum'].iloc[-1] * 100
            
            # Volume analysis
            volume_trend = df['Volume_Trend'].iloc[-1]
            volume_signal = "Normal"
            if volume_trend > 1.5:
                volume_signal = "High"
            elif volume_trend < 0.5:
                volume_signal = "Low"
            
            analysis = {
                "current_price": round(current_price, 2),
                "price_change_pct": round((current_price - prev_price) / prev_price * 100, 2),
                "trend": {
                    "direction": trend_direction,
                    "strength": round(trend_strength, 2),
                    "description": df['Trend_Strength'].iloc[-1],
                    "momentum": round(momentum, 2)
                },
                "rsi": {
                    "value": round(df['RSI'].iloc[-1], 2),
                    "condition": df['RSI_Trend'].iloc[-1]
                },
                "macd": {
                    "value": round(df['MACD'].iloc[-1], 2),
                    "signal": round(df['MACD_Signal'].iloc[-1], 2),
                    "histogram": round(df['MACD_Hist'].iloc[-1], 2),
                    "crossover": df['MACD_Trend'].iloc[-1]
                },
                "volume": {
                    "current": df['Volume'].iloc[-1],
                    "average": df['Volume_SMA'].iloc[-1],
                    "trend": volume_signal,
                    "change_vs_avg": round((volume_trend - 1) * 100, 2)
                },
                "support_resistance": {
                    "r2": round(df['R2'].iloc[-1], 2),
                    "r1": round(df['R1'].iloc[-1], 2),
                    "pivot": round(df['PP'].iloc[-1], 2),
                    "s1": round(df['S1'].iloc[-1], 2),
                    "s2": round(df['S2'].iloc[-1], 2)
                },
                "volatility": round(df['ATR_Pct'].iloc[-1], 2)
            }
            return analysis
        except Exception as e:
            print(f"Error analyzing trends: {str(e)}")
            return {}
