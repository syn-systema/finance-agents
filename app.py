import streamlit as st
import plotly.graph_objects as go
from market_data import MarketData
from technical_analysis import TechnicalAnalysis
from analyst import FinancialAnalyst
from review_agent import ReviewAgent
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinanceApp:
    def __init__(self):
        """Initialize the finance application"""
        load_dotenv()
        
        # Verify API keys
        if not os.getenv('ANTHROPIC_API_KEY'):
            logger.error("ANTHROPIC_API_KEY not found in environment variables")
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            
        if not os.getenv('OPENAI_API_KEY'):
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        logger.info("Initializing components...")
        self.market_data = MarketData()
        self.technical_analyst = TechnicalAnalysis()
        self.financial_analyst = FinancialAnalyst()
        self.review_agent = ReviewAgent()
        logger.info("Components initialized successfully")

    def analyze_stock(self, symbol: str):
        """Analyze a stock using multiple agents"""
        try:
            logger.info(f"Starting analysis for {symbol}")
            
            # Get market data
            logger.info(f"Fetching market data for {symbol}...")
            stock_info = self.market_data.get_stock_info(symbol)
            if not stock_info:
                raise ValueError(f"Could not fetch stock info for {symbol}")
            
            logger.info("Fetching price data...")
            price_data = self.market_data.get_price_data(symbol)
            if price_data.empty:
                raise ValueError(f"Could not fetch price data for {symbol}")
            
            # Calculate technical indicators
            logger.info("Calculating technical indicators...")
            analysis_data = self.technical_analyst.calculate_indicators(price_data)
            if analysis_data.empty:
                raise ValueError("Failed to calculate technical indicators")
                
            technical_data = self.technical_analyst.analyze_trends(analysis_data)
            if not technical_data:
                raise ValueError("Failed to analyze trends")
            
            # Generate analysis report
            logger.info("Generating analysis report...")
            analysis_report = self.financial_analyst.generate_analysis_report(
                symbol, stock_info, technical_data, price_data
            )
            if not analysis_report:
                raise ValueError("Failed to generate analysis report")
            
            # Review the analysis
            logger.info("Reviewing analysis...")
            review_feedback = self.review_agent.review_technical_analysis(
                symbol, analysis_report, technical_data, price_data
            )
            if not review_feedback:
                raise ValueError("Failed to review analysis")
            
            # Validate trading signals
            logger.info("Validating trading signals...")
            signal_validation = self.review_agent.validate_trading_signals(
                technical_data, price_data
            )
            if not signal_validation:
                raise ValueError("Failed to validate trading signals")
            
            # Generate review summary
            logger.info("Generating review summary...")
            review_summary = self.review_agent.generate_summary(review_feedback)
            if not review_summary:
                raise ValueError("Failed to generate review summary")
            
            logger.info(f"Analysis completed successfully for {symbol}")
            return {
                "analysis_report": analysis_report,
                "review_feedback": review_feedback,
                "signal_validation": signal_validation,
                "review_summary": review_summary
            }
            
        except Exception as e:
            logger.error(f"Error analyzing stock: {str(e)}", exc_info=True)
            return None

def main():
    """Main function to run the Streamlit app"""
    st.set_page_config(page_title="Stock Analysis", layout="wide")
    
    try:
        app = FinanceApp()
        
        st.title("Stock Analysis Dashboard")
        
        # Input for stock symbol
        symbol = st.text_input("Enter Stock Symbol:", value="AAPL").upper()
        
        if st.button("Analyze"):
            with st.spinner("Analyzing..."):
                results = app.analyze_stock(symbol)
                
                if results:
                    # Create tabs for different sections
                    tab1, tab2, tab3 = st.tabs(["Analysis Report", "Review Feedback", "Signal Validation"])
                    
                    with tab1:
                        st.markdown(results["analysis_report"])
                    
                    with tab2:
                        st.subheader("Review Summary")
                        st.markdown(results["review_summary"])
                        
                        st.subheader("Detailed Feedback")
                        st.json(results["review_feedback"])
                    
                    with tab3:
                        st.subheader("Signal Validation")
                        st.json(results["signal_validation"])
                else:
                    st.error("Error analyzing stock. Please check the logs for details.")
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        st.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()
