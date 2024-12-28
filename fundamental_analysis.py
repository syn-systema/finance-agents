import pandas as pd
import numpy as np
from typing import Dict, List, Union, Optional

class FundamentalAnalysis:
    @staticmethod
    def financial_ratios(
        financial_data: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate key financial ratios
        
        Parameters:
        - financial_data: Dictionary containing financial statement data
        """
        ratios = {}
        
        # Profitability Ratios
        if all(k in financial_data for k in ['net_income', 'total_assets', 'total_equity', 'revenue']):
            ratios['roa'] = financial_data['net_income'] / financial_data['total_assets']
            ratios['roe'] = financial_data['net_income'] / financial_data['total_equity']
            ratios['net_margin'] = financial_data['net_income'] / financial_data['revenue']
        
        # Liquidity Ratios
        if all(k in financial_data for k in ['current_assets', 'current_liabilities', 'inventory']):
            ratios['current_ratio'] = financial_data['current_assets'] / financial_data['current_liabilities']
            ratios['quick_ratio'] = (financial_data['current_assets'] - financial_data['inventory']) / financial_data['current_liabilities']
        
        # Efficiency Ratios
        if all(k in financial_data for k in ['revenue', 'total_assets', 'accounts_receivable', 'inventory']):
            ratios['asset_turnover'] = financial_data['revenue'] / financial_data['total_assets']
            ratios['receivables_turnover'] = financial_data['revenue'] / financial_data['accounts_receivable']
            ratios['inventory_turnover'] = financial_data['revenue'] / financial_data['inventory']
        
        # Leverage Ratios
        if all(k in financial_data for k in ['total_debt', 'total_equity', 'total_assets']):
            ratios['debt_to_equity'] = financial_data['total_debt'] / financial_data['total_equity']
            ratios['debt_to_assets'] = financial_data['total_debt'] / financial_data['total_assets']
        
        return ratios

    @staticmethod
    def dcf_valuation(
        cash_flows: List[float],
        discount_rate: float,
        terminal_growth_rate: float,
        shares_outstanding: float
    ) -> Dict[str, float]:
        """
        Perform Discounted Cash Flow (DCF) valuation
        
        Parameters:
        - cash_flows: List of projected free cash flows
        - discount_rate: Required rate of return
        - terminal_growth_rate: Long-term growth rate
        - shares_outstanding: Number of shares outstanding
        """
        # Calculate present value of explicit forecast period
        pv_cash_flows = sum(cf / (1 + discount_rate) ** (i + 1) 
                           for i, cf in enumerate(cash_flows))
        
        # Calculate terminal value
        terminal_value = (cash_flows[-1] * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)
        pv_terminal_value = terminal_value / (1 + discount_rate) ** len(cash_flows)
        
        # Calculate enterprise value and equity value
        enterprise_value = pv_cash_flows + pv_terminal_value
        equity_value = enterprise_value
        price_per_share = equity_value / shares_outstanding
        
        return {
            'enterprise_value': enterprise_value,
            'equity_value': equity_value,
            'price_per_share': price_per_share,
            'pv_forecast_cash_flows': pv_cash_flows,
            'pv_terminal_value': pv_terminal_value
        }

    @staticmethod
    def competitor_analysis(
        company_metrics: Dict[str, float],
        competitor_metrics: List[Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        """
        Perform competitor analysis and benchmarking
        
        Parameters:
        - company_metrics: Dictionary of company metrics
        - competitor_metrics: List of dictionaries containing competitor metrics
        """
        all_metrics = [company_metrics] + competitor_metrics
        metrics_df = pd.DataFrame(all_metrics)
        
        analysis = {}
        for column in metrics_df.columns:
            analysis[column] = {
                'company_value': company_metrics[column],
                'industry_avg': metrics_df[column].mean(),
                'industry_median': metrics_df[column].median(),
                'percentile': stats.percentileofscore(metrics_df[column], company_metrics[column])
            }
        
        return analysis

    @staticmethod
    def esg_scoring(
        environmental_metrics: Dict[str, float],
        social_metrics: Dict[str, float],
        governance_metrics: Dict[str, float],
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Union[float, Dict[str, float]]]:
        """
        Calculate ESG score based on various metrics
        
        Parameters:
        - environmental_metrics: Dictionary of environmental metrics
        - social_metrics: Dictionary of social metrics
        - governance_metrics: Dictionary of governance metrics
        - weights: Optional dictionary of weights for each category
        """
        if weights is None:
            weights = {
                'environmental': 0.33,
                'social': 0.33,
                'governance': 0.34
            }
        
        # Calculate individual scores
        env_score = np.mean(list(environmental_metrics.values()))
        social_score = np.mean(list(social_metrics.values()))
        gov_score = np.mean(list(governance_metrics.values()))
        
        # Calculate weighted total score
        total_score = (
            env_score * weights['environmental'] +
            social_score * weights['social'] +
            gov_score * weights['governance']
        )
        
        return {
            'total_score': total_score,
            'environmental_score': env_score,
            'social_score': social_score,
            'governance_score': gov_score,
            'detailed_metrics': {
                'environmental': environmental_metrics,
                'social': social_metrics,
                'governance': governance_metrics
            }
        }
