from anthropic import Anthropic
import os
from typing import Dict, Any
import pandas as pd
from datetime import datetime

class FinancialAnalyst:
    """Class for generating AI-powered financial analysis reports using Claude"""
    
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def generate_analysis_report(self, 
                               symbol: str,
                               stock_info: Dict[str, Any],
                               technical_data: Dict[str, Any],
                               price_data: pd.DataFrame) -> str:
        """Generate a comprehensive technical analysis report using Claude"""
        
        # Prepare the context for Claude
        context = self._prepare_analysis_context(symbol, stock_info, technical_data, price_data)
        
        # Create the prompt for Claude
        prompt = f"""You are an expert financial analyst. Based on the following market data and technical analysis, 
        provide a comprehensive technical analysis report. Focus on actionable insights and potential trading opportunities.

        {context}

        Create a professional technical analysis report in clean markdown format. Be specific with price levels and provide clear, actionable insights.
        Format all numbers consistently (e.g., $259.45, 23.5%). Use tables for organized presentation of data.

        Use this exact structure and formatting:

        # Technical Analysis Report for {symbol}

        ## Executive Summary
        [Provide a 2-3 sentence overview focusing on the primary trend, key levels, and most important signals]

        ## Market Overview

        | Key Statistics | Value |
        |---------------|-------|
        | Current Price | ${technical_data['current_price']:.2f} |
        | Daily Change | {technical_data['price_change_pct']:.2f}% |
        | 52-Week Range | ${price_data['Low'].min():.2f} - ${price_data['High'].max():.2f} |
        | Market Cap | ${stock_info.get('market_cap', 0)/1e9:.2f}B |
        | RSI | {technical_data['rsi']['value']:.2f} |
        | Volume | {technical_data['volume']['current']:,.0f} |
        | Avg Volume | {technical_data['volume']['average']:,.0f} |

        ### Current Market Status
        - Primary Trend: {technical_data['trend']['direction']}
        - Trend Strength: {technical_data['trend']['description']} ({technical_data['trend']['strength']:.1f})
        - Momentum: {technical_data['trend']['momentum']:.1f}%
        - Volume Status: {technical_data['volume']['trend']} ({technical_data['volume']['change_vs_avg']:.1f}% vs avg)

        ## Technical Analysis

        ### Price Action
        - SMA 20: ${price_data['SMA_20'].iloc[-1]:.2f}
        - SMA 50: ${price_data['SMA_50'].iloc[-1]:.2f}
        - EMA 20: ${price_data['EMA_20'].iloc[-1]:.2f}

        ### Key Price Levels

        | Level Type | Price | Description |
        |------------|-------|-------------|
        | Major Resistance (R2) | ${technical_data['support_resistance']['r2']:.2f} | Strong resistance level |
        | Minor Resistance (R1) | ${technical_data['support_resistance']['r1']:.2f} | Near-term resistance |
        | Pivot Point | ${technical_data['support_resistance']['pivot']:.2f} | Key pivot level |
        | Minor Support (S1) | ${technical_data['support_resistance']['s1']:.2f} | Near-term support |
        | Major Support (S2) | ${technical_data['support_resistance']['s2']:.2f} | Strong support level |

        ### Technical Indicators
        1. **RSI Analysis**
           - Current RSI: {technical_data['rsi']['value']:.2f}
           - Status: {technical_data['rsi']['condition']}
           [Provide interpretation]

        2. **MACD Analysis**
           - MACD Line: {technical_data['macd']['value']:.2f}
           - Signal Line: {technical_data['macd']['signal']:.2f}
           - Histogram: {technical_data['macd']['histogram']:.2f}
           - Signal: {technical_data['macd']['crossover']}
           [Provide interpretation]

        3. **Volume Analysis**
           - Current vs Average: {technical_data['volume']['change_vs_avg']:.1f}%
           - Volume Trend: {technical_data['volume']['trend']}
           [Provide interpretation]

        ## Trading Strategy

        ### Entry Points
        [Provide specific entry points based on technical levels]

        ### Exit Points
        [Provide specific profit targets]

        ### Stop Loss Levels
        [Provide specific stop loss levels]

        ### Position Sizing
        [Provide position sizing recommendations based on volatility ({technical_data['volatility']:.1f}%)]

        ## Risk Assessment

        ### Key Risk Factors
        1. [Risk factor 1]
        2. [Risk factor 2]
        3. [Risk factor 3]

        ### Market Conditions
        - Volatility: {technical_data['volatility']:.1f}%
        - Volume Conditions: {technical_data['volume']['trend']}
        - Trend Reliability: {technical_data['trend']['description']}

        Remember to:
        1. Be specific with price levels
        2. Provide clear, actionable insights
        3. Explain the reasoning behind recommendations
        4. Consider current market conditions
        5. Address both bullish and bearish scenarios
        """

        # Get analysis from Claude
        message = self.anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            temperature=0.7,
            system="You are an expert financial analyst. Provide detailed technical analysis with specific price levels and clear reasoning. Format all output in clean markdown with consistent number formatting ($XXX.XX, XX.XX%). Focus on actionable insights.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract the content and ensure it's properly formatted
        if hasattr(message.content[0], 'text'):
            return message.content[0].text
        return message.content

    def _prepare_analysis_context(self,
                                symbol: str,
                                stock_info: Dict[str, Any],
                                technical_data: Dict[str, Any],
                                price_data: pd.DataFrame) -> str:
        """Prepare the market data context for Claude's analysis"""
        
        # Calculate additional metrics
        latest_price = price_data['Close'].iloc[-1]
        prev_price = price_data['Close'].iloc[-2]
        price_change = (latest_price - prev_price) / prev_price * 100
        
        # Calculate key price levels
        high_52w = price_data['High'].tail(252).max()
        low_52w = price_data['Low'].tail(252).min()
        
        # Calculate volume metrics
        avg_volume = price_data['Volume'].mean()
        latest_volume = price_data['Volume'].iloc[-1]
        vol_change = (latest_volume - avg_volume) / avg_volume * 100
        
        context = f"""
        Analysis Context:
        
        Stock: {symbol}
        Analysis Date: {datetime.now().strftime('%Y-%m-%d')}
        
        Company Information:
        Name: {stock_info.get('name', symbol)}
        Sector: {stock_info.get('sector', 'N/A')}
        Industry: {stock_info.get('industry', 'N/A')}
        Market Cap: ${stock_info.get('market_cap', 0)/1e9:.2f}B
        
        Price Information:
        Current Price: ${latest_price:.2f}
        Daily Change: {price_change:.2f}%
        52-Week Range: ${low_52w:.2f} - ${high_52w:.2f}
        Distance from 52w High: {((high_52w - latest_price) / latest_price * 100):.2f}%
        Distance from 52w Low: {((latest_price - low_52w) / low_52w * 100):.2f}%
        
        Volume Information:
        Latest Volume: {latest_volume:,.0f}
        Average Volume: {avg_volume:,.0f}
        Volume Change: {vol_change:.2f}%
        
        Technical Indicators:
        Trend Direction: {technical_data['trend']['direction']}
        Trend Strength: {technical_data['trend']['description']} ({technical_data['trend']['strength']:.2f}%)
        RSI: {technical_data['rsi']['value']:.2f} ({technical_data['rsi']['condition']})
        MACD: {technical_data['macd']['value']:.2f}
        MACD Signal: {technical_data['macd']['signal']:.2f}
        MACD Crossover: {technical_data['macd']['crossover']}
        Volatility: {technical_data['volatility']:.2f}%
        
        Moving Averages:
        SMA 20: ${price_data['SMA_20'].iloc[-1]:.2f}
        SMA 50: ${price_data['SMA_50'].iloc[-1]:.2f}
        EMA 20: ${price_data['EMA_20'].iloc[-1]:.2f}
        
        Bollinger Bands:
        Upper Band: ${price_data['BB_High'].iloc[-1]:.2f}
        Middle Band: ${price_data['BB_Mid'].iloc[-1]:.2f}
        Lower Band: ${price_data['BB_Low'].iloc[-1]:.2f}
        """
        
        return context
