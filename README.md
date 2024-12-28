# Finance Agents: Advanced Financial Analysis System

A sophisticated financial analysis system that combines traditional technical analysis with AI-powered insights. This system utilizes multiple specialized agents to provide comprehensive market analysis, risk management, and trading recommendations.

## 🚀 Key Features

- AI-Powered Analysis Reports
- Advanced Technical Indicators
- Fundamental Analysis
- Risk Management
- Market Data Processing
- Real-time Trading Signals

## 🤖 Agent Components

### 1. Financial Analyst Agent (`analyst.py`)
An AI-powered analyst that generates comprehensive market reports using the Claude API. This agent:
- Processes market data and technical indicators
- Generates professional analysis reports in markdown format
- Provides actionable trading insights
- Combines multiple data sources for holistic analysis

### 2. Technical Analysis Agent (`technical_analysis.py`)
Performs advanced technical analysis with multiple indicators:
- RSI (Relative Strength Index) with trend identification
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands with width calculation
- Multiple Moving Averages (SMA, EMA)
- Volume analysis and trends
- ATR (Average True Range) for volatility measurement

### 3. Advanced Indicators Agent (`advanced_indicators.py`)
Implements sophisticated technical indicators:
- Fibonacci Retracement levels
- Ichimoku Cloud components (Tenkan-sen, Kijun-sen, Senkou Span A/B, Chikou Span)
- On Balance Volume (OBV)
- Stochastic RSI
- Custom momentum indicators

### 4. Fundamental Analysis Agent (`fundamental_analysis.py`)
Focuses on company financial metrics:
- Key Financial Ratios
  - Profitability (ROA, ROE, Net Margin)
  - Liquidity (Current Ratio, Quick Ratio)
  - Efficiency (Asset Turnover, Receivables Turnover)
  - Leverage (Debt-to-Equity, Debt-to-Assets)
- DCF (Discounted Cash Flow) Valuation
- Growth Rate Analysis
- Financial Health Scoring

### 5. Risk Management Agent (`risk_management.py`)
Handles risk assessment and position sizing:
- Position Size Calculator based on account risk
- Value at Risk (VaR) calculations
  - Parametric VaR
  - Historical VaR
- Risk-Reward Ratio Analysis
- Portfolio Risk Assessment
- Stop Loss Optimization

## 🛠 Technical Architecture

The system is built with a modular architecture where each agent specializes in a specific aspect of financial analysis. The agents work together to provide a comprehensive analysis platform:

1. Market Data Layer
   - Real-time and historical data processing
   - Data normalization and cleaning
   - Multiple timeframe analysis

2. Analysis Layer
   - Technical indicators calculation
   - Fundamental data processing
   - Risk metrics computation

3. AI Integration Layer
   - Claude API integration for advanced analysis
   - Natural language report generation
   - Pattern recognition and insights

4. Risk Management Layer
   - Position sizing calculations
   - Risk assessment
   - Portfolio optimization

## 📊 Usage Example

```python
# Initialize the analysis system
analyst = FinancialAnalyst()
technical = TechnicalAnalysis()
risk_manager = RiskManagement()

# Generate analysis report
report = analyst.generate_analysis_report(
    symbol="AAPL",
    stock_info=stock_data,
    technical_data=technical_indicators,
    price_data=historical_prices
)

# Calculate optimal position size
position = risk_manager.position_size_calculator(
    account_size=100000,
    risk_percentage=2,
    entry_price=150.0,
    stop_loss=145.0
)
```

## 🔧 Dependencies

- pandas
- numpy
- ta (Technical Analysis Library)
- scipy
- anthropic (for Claude AI integration)

## 🚀 Getting Started

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   ```
4. Import and initialize the required agents
5. Start analyzing!
