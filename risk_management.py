import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Union, Tuple

class RiskManagement:
    @staticmethod
    def position_size_calculator(
        account_size: float,
        risk_percentage: float,
        entry_price: float,
        stop_loss: float
    ) -> Dict[str, float]:
        """
        Calculate optimal position size based on account risk management
        
        Parameters:
        - account_size: Total account value
        - risk_percentage: Maximum risk per trade as percentage (e.g., 2 for 2%)
        - entry_price: Planned entry price
        - stop_loss: Stop loss price
        """
        risk_amount = account_size * (risk_percentage / 100)
        price_risk = abs(entry_price - stop_loss)
        position_size = risk_amount / price_risk
        total_position_value = position_size * entry_price
        
        return {
            'position_size': position_size,
            'total_position_value': total_position_value,
            'risk_amount': risk_amount,
            'risk_per_share': price_risk
        }

    @staticmethod
    def calculate_var(
        returns: pd.Series,
        confidence_level: float = 0.95,
        time_horizon: int = 1
    ) -> Dict[str, float]:
        """
        Calculate Value at Risk (VaR) using both parametric and historical methods
        
        Parameters:
        - returns: Series of historical returns
        - confidence_level: Confidence level for VaR calculation (e.g., 0.95 for 95%)
        - time_horizon: Time horizon in days
        """
        # Parametric VaR
        mean = returns.mean()
        std = returns.std()
        z_score = stats.norm.ppf(1 - confidence_level)
        parametric_var = -(mean + z_score * std) * np.sqrt(time_horizon)
        
        # Historical VaR
        historical_var = -np.percentile(returns, (1 - confidence_level) * 100)
        
        # Conditional VaR (Expected Shortfall)
        cvar = -returns[returns <= -historical_var].mean()
        
        return {
            'parametric_var': parametric_var,
            'historical_var': historical_var,
            'cvar': cvar
        }

    @staticmethod
    def monte_carlo_simulation(
        price: float,
        volatility: float,
        days: int,
        simulations: int = 1000,
        confidence_level: float = 0.95
    ) -> Dict[str, Union[float, List[float]]]:
        """
        Perform Monte Carlo simulation for price movements
        
        Parameters:
        - price: Current price
        - volatility: Annual volatility
        - days: Number of days to simulate
        - simulations: Number of simulation paths
        - confidence_level: Confidence level for risk metrics
        """
        daily_vol = volatility / np.sqrt(252)
        daily_returns = np.random.normal(0, daily_vol, (simulations, days))
        price_paths = price * np.exp(np.cumsum(daily_returns, axis=1))
        
        final_prices = price_paths[:, -1]
        var = np.percentile(final_prices, (1 - confidence_level) * 100)
        expected_price = np.mean(final_prices)
        
        return {
            'expected_price': expected_price,
            'var_price': var,
            'max_price': np.max(final_prices),
            'min_price': np.min(final_prices),
            'price_paths': price_paths.tolist()
        }

    @staticmethod
    def optimize_stop_loss(
        df: pd.DataFrame,
        atr_multiple: float = 2.0,
        lookback_period: int = 20
    ) -> pd.Series:
        """
        Calculate optimal stop-loss levels using Average True Range (ATR)
        
        Parameters:
        - df: DataFrame with OHLC data
        - atr_multiple: Multiplier for ATR to set stop distance
        - lookback_period: Period for ATR calculation
        """
        # Calculate ATR
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(window=lookback_period).mean()
        
        # Calculate stop levels
        stop_distance = atr * atr_multiple
        long_stop = df['Close'] - stop_distance
        short_stop = df['Close'] + stop_distance
        
        return pd.DataFrame({
            'long_stop': long_stop,
            'short_stop': short_stop,
            'atr': atr
        })
