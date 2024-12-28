# Finance Agents: AI-Powered Stock Analysis Dashboard

A sophisticated financial analysis system that combines traditional technical analysis with AI-powered insights, delivered through an interactive Streamlit dashboard. This system utilizes multiple specialized agents to provide comprehensive market analysis, risk management, and trading recommendations in real-time.

## 🚀 Key Features

- Interactive Streamlit Web Interface
- AI-Powered Analysis Reports
- Advanced Technical Indicators
- Fundamental Analysis
- Risk Management
- Real-time Market Data Processing
- Multi-Agent Review System

## 💻 Live Demo

Access the application by running:
```bash
streamlit run app.py
```

The dashboard provides:
- Stock symbol input
- Real-time analysis
- Interactive charts and visualizations
- Three main sections:
  1. Analysis Report
  2. Review Feedback
  3. Signal Validation

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
- Ichimoku Cloud components
- On Balance Volume (OBV)
- Stochastic RSI
- Custom momentum indicators

### 4. Fundamental Analysis Agent (`fundamental_analysis.py`)
Focuses on company financial metrics:
- Key Financial Ratios
- DCF Valuation
- Growth Rate Analysis
- Financial Health Scoring

### 5. Risk Management Agent (`risk_management.py`)
Handles risk assessment and position sizing:
- Position Size Calculator
- Value at Risk (VaR) calculations
- Risk-Reward Analysis
- Portfolio Risk Assessment

### 6. Review Agent (`review_agent.py`)
Provides additional validation and feedback:
- Analysis review and validation
- Signal confirmation
- Risk assessment verification
- Trading recommendation review

## 🛠 Technical Architecture

The system is built with a modular architecture where each agent specializes in a specific aspect of financial analysis:

1. Frontend Layer (Streamlit)
   - Interactive web interface
   - Real-time data visualization
   - User input handling
   - Results presentation

2. Market Data Layer
   - Real-time and historical data processing
   - Data normalization and cleaning
   - Multiple timeframe analysis

3. Analysis Layer
   - Technical indicators calculation
   - Fundamental data processing
   - Risk metrics computation

4. AI Integration Layer
   - Claude API integration for advanced analysis
   - OpenAI integration for review agent
   - Natural language report generation
   - Pattern recognition and insights

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/syn-systema/finance-agents.git
   cd finance-agents
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file with:
   ```
   ANTHROPIC_API_KEY=your_claude_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 📊 Usage Example

1. Launch the Streamlit app
2. Enter a stock symbol (e.g., "AAPL")
3. Click "Analyze"
4. View the results in three tabs:
   - Analysis Report: Comprehensive market analysis
   - Review Feedback: AI agent's review of the analysis
   - Signal Validation: Technical signal confirmation

## 🔧 Dependencies

- streamlit
- plotly
- pandas
- numpy
- ta (Technical Analysis Library)
- scipy
- anthropic (for Claude AI integration)
- openai
- python-dotenv

## 📝 License

MIT License

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
