"""
Marketing strategy development module for RFM analysis
"""

import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class MarketingAction:
    """Marketing action definition"""
    action: str
    description: str
    priority: str
    expected_impact: str


@dataclass
class SegmentStrategy:
    """Marketing strategy for a customer segment"""
    segment: str
    characteristics: str
    goals: List[str]
    actions: List[MarketingAction]
    kpis: List[str]
    budget_allocation: float


class MarketingStrategyGenerator:
    """
    Generates marketing strategies based on RFM segments
    """
    
    def __init__(self):
        self.strategies = {}
        self._initialize_default_strategies()
    
    def _initialize_default_strategies(self):
        """Initialize default marketing strategies for each segment"""
        
        # Champions Strategy
        self.strategies['Champions'] = SegmentStrategy(
            segment='Champions',
            characteristics='Recent purchases, high frequency, high spend',
            goals=['Maximize lifetime value', 'Increase referral rate', 'Maintain loyalty'],
            actions=[
                MarketingAction('VIP Program', 'Exclusive benefits and early access', 'High', 'High'),
                MarketingAction('Referral Rewards', 'Incentivize customer referrals', 'High', 'Medium'),
                MarketingAction('Premium Bundles', 'Offer exclusive product bundles', 'Medium', 'Medium'),
                MarketingAction('Personalized Service', 'Dedicated account manager', 'High', 'High')
            ],
            kpis=['Repeat purchase rate', 'Referral rate', 'ARPU uplift', 'NPS score'],
            budget_allocation=0.25
        )
        
        # Loyal Customers Strategy
        self.strategies['Loyal Customers'] = SegmentStrategy(
            segment='Loyal Customers',
            characteristics='Frequent buyers, good spend',
            goals=['Increase frequency', 'Cross-sell opportunities', 'Subscription adoption'],
            actions=[
                MarketingAction('Loyalty Program', 'Tiered points and rewards system', 'High', 'High'),
                MarketingAction('Cross-sell Campaigns', 'Recommend complementary products', 'Medium', 'Medium'),
                MarketingAction('Subscription Offers', 'Auto-ship and subscription options', 'Medium', 'Medium'),
                MarketingAction('Exclusive Discounts', 'Special pricing for loyal customers', 'Low', 'Medium')
            ],
            kpis=['Purchase frequency', 'Cross-sell rate', 'Subscription uptake', 'Retention rate'],
            budget_allocation=0.20
        )
        
        # Potential Loyalist Strategy
        self.strategies['Potential Loyalist'] = SegmentStrategy(
            segment='Potential Loyalist',
            characteristics='New but promising, moderate frequency/spend',
            goals=['Increase engagement', 'Build loyalty', 'Accelerate purchase frequency'],
            actions=[
                MarketingAction('Welcome Series', 'Educational content and onboarding', 'High', 'High'),
                MarketingAction('Purchase Incentives', 'Discounts on 2nd and 3rd orders', 'High', 'High'),
                MarketingAction('Personalized Recommendations', 'AI-driven product suggestions', 'Medium', 'Medium'),
                MarketingAction('Community Building', 'Social proof and user-generated content', 'Low', 'Low')
            ],
            kpis=['Second purchase rate', '90-day retention', 'CAC payback period', 'Engagement rate'],
            budget_allocation=0.20
        )
        
        # New Customers Strategy
        self.strategies['New Customers'] = SegmentStrategy(
            segment='New Customers',
            characteristics='Recent first-time buyers',
            goals=['Onboarding success', 'Second purchase', 'Brand education'],
            actions=[
                MarketingAction('Onboarding Sequence', 'Welcome emails and tutorials', 'High', 'High'),
                MarketingAction('First Purchase Follow-up', 'Thank you and next steps', 'High', 'Medium'),
                MarketingAction('Educational Content', 'Product guides and tips', 'Medium', 'Medium'),
                MarketingAction('Social Proof', 'Customer testimonials and reviews', 'Low', 'Low')
            ],
            kpis=['Onboarding completion', 'Second purchase rate', 'Email engagement', 'Time to second purchase'],
            budget_allocation=0.15
        )
        
        # At Risk Strategy
        self.strategies['At Risk'] = SegmentStrategy(
            segment='At Risk',
            characteristics='Declining activity, previously valuable',
            goals=['Reactivation', 'Prevent churn', 'Restore engagement'],
            actions=[
                MarketingAction('Win-back Campaign', 'Special offers to return', 'High', 'High'),
                MarketingAction('Feedback Survey', 'Understand why they left', 'High', 'Medium'),
                MarketingAction('Cart Recovery', 'Reminders for abandoned purchases', 'Medium', 'Medium'),
                MarketingAction('Reactivation Bundles', 'Attractive package deals', 'Medium', 'High')
            ],
            kpis=['Reactivation rate', 'Time to reorder', 'Churn reduction', 'Response rate'],
            budget_allocation=0.10
        )
        
        # Lost Strategy
        self.strategies['Lost'] = SegmentStrategy(
            segment='Lost',
            characteristics='Very long recency, low engagement',
            goals=['List cleaning', 'Occasional reactivation', 'Cost optimization'],
            actions=[
                MarketingAction('Sunset Campaign', 'Final attempt with deep discounts', 'Medium', 'Low'),
                MarketingAction('List Segmentation', 'Separate active from inactive', 'High', 'Medium'),
                MarketingAction('Reactivation Offers', 'Aggressive pricing for return', 'Low', 'Low'),
                MarketingAction('Data Cleanup', 'Remove unengaged customers', 'Medium', 'High')
            ],
            kpis=['Open/reply rate', 'Reactivation conversion', 'List quality score', 'Cost per contact'],
            budget_allocation=0.05
        )
        
        # Other segments
        self.strategies['Promising'] = SegmentStrategy(
            segment='Promising',
            characteristics='Good recency and frequency, low monetary',
            goals=['Increase spend', 'Build loyalty', 'Upgrade behavior'],
            actions=[
                MarketingAction('Value Communication', 'Show total value and benefits', 'High', 'Medium'),
                MarketingAction('Upgrade Incentives', 'Rewards for higher spending', 'Medium', 'Medium'),
                MarketingAction('Loyalty Program', 'Points and tier benefits', 'Medium', 'Medium')
            ],
            kpis=['Average order value', 'Purchase frequency', 'Loyalty program adoption'],
            budget_allocation=0.03
        )
        
        self.strategies['Need Attention'] = SegmentStrategy(
            segment='Need Attention',
            characteristics='Moderate RFM scores',
            goals=['Increase engagement', 'Prevent decline', 'Build loyalty'],
            actions=[
                MarketingAction('Engagement Campaigns', 'Regular touchpoints and content', 'High', 'Medium'),
                MarketingAction('Personalized Offers', 'Tailored promotions', 'Medium', 'Medium'),
                MarketingAction('Feedback Collection', 'Understand needs and preferences', 'Medium', 'Low')
            ],
            kpis=['Engagement rate', 'Purchase frequency', 'Response rate'],
            budget_allocation=0.02
        )
    
    def generate_strategies_for_segments(self, segments_data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate marketing strategies for all segments in the data
        
        Args:
            segments_data: DataFrame with segment information
            
        Returns:
            DataFrame with marketing strategies
        """
        strategies_list = []
        
        for segment in segments_data['Segment'].unique():
            if segment in self.strategies:
                strategy = self.strategies[segment]
                
                # Count customers in segment
                segment_count = len(segments_data[segments_data['Segment'] == segment])
                segment_percentage = (segment_count / len(segments_data)) * 100
                
                strategies_list.append({
                    'Segment': segment,
                    'Customer_Count': segment_count,
                    'Percentage': round(segment_percentage, 1),
                    'Characteristics': strategy.characteristics,
                    'Primary_Goals': '; '.join(strategy.goals),
                    'Key_Actions': '; '.join([action.action for action in strategy.actions]),
                    'KPIs': '; '.join(strategy.kpis),
                    'Budget_Allocation': strategy.budget_allocation,
                    'Priority': 'High' if segment_count > len(segments_data) * 0.1 else 'Medium'
                })
        
        return pd.DataFrame(strategies_list)
    
    def get_detailed_actions(self, segment: str) -> List[MarketingAction]:
        """
        Get detailed actions for a specific segment
        
        Args:
            segment: Segment name
            
        Returns:
            List of MarketingAction objects
        """
        if segment in self.strategies:
            return self.strategies[segment].actions
        else:
            return []
    
    def calculate_budget_allocation(self, total_budget: float, segments_data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate budget allocation across segments
        
        Args:
            total_budget: Total marketing budget
            segments_data: DataFrame with segment information
            
        Returns:
            Dictionary with budget allocation by segment
        """
        budget_allocation = {}
        segment_counts = segments_data['Segment'].value_counts()
        total_customers = len(segments_data)
        
        for segment, count in segment_counts.items():
            if segment in self.strategies:
                # Base allocation from strategy
                base_allocation = self.strategies[segment].budget_allocation
                
                # Adjust based on segment size
                size_factor = count / total_customers
                
                # Calculate final allocation
                final_allocation = base_allocation * (1 + size_factor)
                
                budget_allocation[segment] = {
                    'allocation_percentage': final_allocation,
                    'budget_amount': total_budget * final_allocation,
                    'customers_count': count,
                    'budget_per_customer': (total_budget * final_allocation) / count
                }
        
        # Normalize allocations to sum to 1.0
        total_allocation = sum([allocation['allocation_percentage'] for allocation in budget_allocation.values()])
        
        for segment in budget_allocation:
            budget_allocation[segment]['allocation_percentage'] /= total_allocation
            budget_allocation[segment]['budget_amount'] = total_budget * budget_allocation[segment]['allocation_percentage']
            budget_allocation[segment]['budget_per_customer'] = budget_allocation[segment]['budget_amount'] / budget_allocation[segment]['customers_count']
        
        return budget_allocation
    
    def export_strategies_to_csv(self, segments_data: pd.DataFrame, 
                                output_path: str = 'marketing_strategies.csv') -> None:
        """
        Export marketing strategies to CSV file
        
        Args:
            segments_data: DataFrame with segment information
            output_path: Path to save the CSV file
        """
        strategies_df = self.generate_strategies_for_segments(segments_data)
        strategies_df.to_csv(output_path, index=False)
        print(f"Marketing strategies exported to {output_path}")
    
    def get_strategy_summary(self, segments_data: pd.DataFrame) -> Dict:
        """
        Get summary of marketing strategies
        
        Args:
            segments_data: DataFrame with segment information
            
        Returns:
            Dictionary with strategy summary
        """
        segment_counts = segments_data['Segment'].value_counts()
        total_customers = len(segments_data)
        
        summary = {
            'total_customers': total_customers,
            'segments_count': len(segment_counts),
            'segment_distribution': segment_counts.to_dict(),
            'high_value_segments': segment_counts.head(3).index.tolist(),
            'strategies_available': list(self.strategies.keys())
        }
        
        return summary
