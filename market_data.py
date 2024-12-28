import yfinance as yf
import pandas as pd
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MarketData:
    """Class for fetching and processing market data"""
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get basic stock information"""
        try:
            logger.info(f"Fetching stock info for {symbol} using yfinance...")
            stock = yf.Ticker(symbol)
            info = stock.info
            
            if not info:
                logger.error(f"No info found for {symbol}")
                return None
            
            logger.info(f"Successfully fetched info for {symbol}")
            # Extract relevant information
            result = {
                'name': info.get('shortName', symbol),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('forwardPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0),
                'description': info.get('longBusinessSummary', '')
            }
            logger.debug(f"Extracted info for {symbol}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {str(e)}", exc_info=True)
            return None
            
    def get_price_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get historical price data"""
        try:
            logger.info(f"Fetching price data for {symbol} using yfinance...")
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            
            if data.empty:
                logger.error(f"No price data found for {symbol}")
                return pd.DataFrame()
            
            logger.info(f"Successfully fetched price data for {symbol}")
            logger.debug(f"Price data shape: {data.shape}")
            logger.debug(f"Price data columns: {data.columns.tolist()}")
            logger.debug(f"Latest price: {data['Close'].iloc[-1]:.2f}")
            
            # Verify required columns exist
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                return pd.DataFrame()
                
            return data
        except Exception as e:
            logger.error(f"Error fetching price data for {symbol}: {str(e)}", exc_info=True)
            return pd.DataFrame()
