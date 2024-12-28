import os
from typing import Dict, Any
from openai import OpenAI
import pandas as pd
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReviewAgent:
    """Agent that reviews and validates analysis from other agents using GPT-4"""
    
    def __init__(self):
        """Initialize the review agent with OpenAI client"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def review_technical_analysis(self, 
                                symbol: str,
                                analysis_report: str,
                                technical_data: Dict[str, Any],
                                price_data: pd.DataFrame) -> Dict[str, Any]:
        """Review a technical analysis report and provide feedback"""
        try:
            logger.info(f"Starting technical analysis review for {symbol}")
            
            prompt = f"""You are an expert financial analyst reviewing a technical analysis report. 
            Your task is to validate the analysis, identify any inconsistencies, and provide constructive feedback.
            
            Original Report:
            {analysis_report}
            
            Key Technical Data:
            - Current Price: ${technical_data['current_price']:.2f}
            - RSI: {technical_data['rsi']['value']:.2f}
            - MACD: {technical_data['macd']['value']:.2f}
            - Signal: {technical_data['macd']['signal']:.2f}
            - Trend Direction: {technical_data['trend']['direction']}
            - Trend Strength: {technical_data['trend']['strength']:.2f}
            - Volume vs Avg: {technical_data['volume']['change_vs_avg']:.1f}%
            
            Please review the analysis and provide feedback on:
            1. Accuracy of trend identification
            2. Validity of support/resistance levels
            3. Consistency of technical indicators
            4. Quality of trading recommendations
            5. Risk assessment completeness
            
            Respond with a JSON object using this exact structure:
            {{
                "overall_rating": <1-10 score>,
                "accuracy": {{
                    "trend_analysis": "<comments on trend analysis accuracy>",
                    "price_levels": "<comments on support/resistance levels>",
                    "indicators": "<comments on technical indicators>"
                }},
                "recommendations": {{
                    "quality": "<comments on trading recommendations>",
                    "risk_assessment": "<comments on risk assessment>"
                }},
                "improvements": [
                    "<list of specific improvements needed>"
                ],
                "validation": {{
                    "confirmed_points": [
                        "<list of valid points>"
                    ],
                    "questionable_points": [
                        "<list of points that need verification>"
                    ]
                }}
            }}
            
            Be specific and reference actual numbers from the report. Focus on actionable feedback."""
            
            logger.info("Sending review request to GPT-4")
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial analyst reviewing technical analysis reports. Provide detailed, specific feedback in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the JSON response
            feedback = json.loads(response.choices[0].message.content)
            logger.info("Successfully received and parsed review feedback")
            return feedback
            
        except Exception as e:
            logger.error(f"Error in review_technical_analysis: {str(e)}", exc_info=True)
            return None
    
    def generate_summary(self, review_feedback: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the review feedback"""
        try:
            logger.info("Generating review summary")
            
            prompt = f"""Based on the following review feedback, generate a concise, professional summary
            highlighting the key points and most important recommendations.
            
            Review Data:
            {json.dumps(review_feedback, indent=2)}
            
            Focus on:
            1. Overall assessment
            2. Key strengths
            3. Critical areas for improvement
            4. Specific recommendations
            
            Format the response in clean markdown with clear sections."""
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial analyst summarizing technical analysis review feedback. Be concise and specific."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            logger.info("Successfully generated review summary")
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in generate_summary: {str(e)}", exc_info=True)
            return None
        
    def validate_trading_signals(self,
                               technical_data: Dict[str, Any],
                               price_data: pd.DataFrame) -> Dict[str, Any]:
        """Validate specific trading signals and recommendations"""
        try:
            logger.info("Starting trading signal validation")
            
            # Calculate additional validation metrics
            last_close = price_data['Close'].iloc[-1]
            sma_20 = price_data['SMA_20'].iloc[-1]
            sma_50 = price_data['SMA_50'].iloc[-1]
            rsi = technical_data['rsi']['value']
            macd = technical_data['macd']['value']
            macd_signal = technical_data['macd']['signal']
            volume_trend = technical_data['volume']['change_vs_avg']
            
            prompt = f"""Validate the following trading signals for potential trades:

            Price Action:
            - Current Price: ${last_close:.2f}
            - SMA 20: ${sma_20:.2f}
            - SMA 50: ${sma_50:.2f}
            
            Technical Indicators:
            - RSI: {rsi:.2f}
            - MACD: {macd:.2f}
            - MACD Signal: {macd_signal:.2f}
            - Volume vs Avg: {volume_trend:.1f}%
            
            Respond with a JSON object using this exact structure:
            {{
                "signal_strength": <1-10 score>,
                "confirmation": {{
                    "trend": "<trend confirmation analysis>",
                    "momentum": "<momentum confirmation analysis>",
                    "volume": "<volume confirmation analysis>"
                }},
                "conflicts": [
                    "<list of conflicting signals>"
                ],
                "validation_summary": "<overall validation summary>",
                "confidence_score": <1-10 score>
            }}
            
            Focus on signal confirmation and potential conflicts."""
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial analyst validating trading signals. Provide detailed validation in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the JSON response
            validation = json.loads(response.choices[0].message.content)
            logger.info("Successfully completed trading signal validation")
            return validation
            
        except Exception as e:
            logger.error(f"Error in validate_trading_signals: {str(e)}", exc_info=True)
            return None
