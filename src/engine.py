"""
Main RFM Insight Engine - Comprehensive RFM Analysis Platform
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
from typing import Optional, Dict, Any, Tuple

from src.core.data_processor import DataProcessor
from src.core.rfm_calculator import RFMCalculator
from src.visualization.plotter import RFMPlotter
from src.strategy.marketing_strategies import MarketingStrategyGenerator


class RFMInsightEngine:
    """
    Comprehensive RFM Analysis Engine
    
    A complete platform for customer segmentation, retention analysis,
    and marketing strategy development using RFM methodology.
    """
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize the RFM Insight Engine
        
        Args:
            output_dir: Directory to save all outputs
        """
        self.output_dir = output_dir
        self.data_processor = DataProcessor()
        self.rfm_calculator = RFMCalculator()
        self.plotter = RFMPlotter()
        self.strategy_generator = MarketingStrategyGenerator()
        
        # Results storage
        self.raw_data = None
        self.processed_data = None
        self.rfm_data = None
        self.rfm_scores = None
        self.segments = None
        self.clusters = None
        self.strategies = None
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/data", exist_ok=True)
        os.makedirs(f"{output_dir}/visualizations", exist_ok=True)
        os.makedirs(f"{output_dir}/reports", exist_ok=True)
        
        print(f"RFM Insight Engine initialized. Output directory: {output_dir}")
    
    def load_and_process_data(self, file_path: str, 
                             analysis_date: Optional[datetime] = None,
                             **kwargs) -> pd.DataFrame:
        """
        Load and process transaction data
        
        Args:
            file_path: Path to transaction data CSV file
            analysis_date: Reference date for RFM calculations
            **kwargs: Additional arguments for data processing
            
        Returns:
            Processed RFM data
        """
        print("=" * 60)
        print("STEP 1: DATA LOADING AND PROCESSING")
        print("=" * 60)
        
        # Load data
        self.raw_data = self.data_processor.load_data(file_path, **kwargs)
        
        # Clean data
        self.processed_data = self.data_processor.clean_data()
        
        # Set analysis date
        if analysis_date:
            self.data_processor.set_analysis_date(analysis_date)
        else:
            self.data_processor.set_analysis_date()
        
        # Prepare RFM data
        self.rfm_data = self.data_processor.prepare_rfm_data()
        
        # Save processed data
        self.rfm_data.to_csv(f"{self.output_dir}/data/rfm_data.csv", index=False)
        
        # Print data summary
        summary = self.data_processor.get_data_summary()
        print(f"\nData Summary:")
        print(f"- Total transactions: {summary['total_transactions']:,}")
        print(f"- Unique customers: {summary['unique_customers']:,}")
        print(f"- Date range: {summary['date_range']['start'].strftime('%Y-%m-%d')} to {summary['date_range']['end'].strftime('%Y-%m-%d')}")
        print(f"- Total revenue: ${summary['amount_statistics']['total_revenue']:,.2f}")
        print(f"- Average transaction: ${summary['amount_statistics']['avg_transaction']:.2f}")
        
        return self.rfm_data
    
    def calculate_rfm_analysis(self, n_quantiles: int = 5) -> pd.DataFrame:
        """
        Perform complete RFM analysis
        
        Args:
            n_quantiles: Number of quantiles for RFM scoring
            
        Returns:
            DataFrame with RFM scores and segments
        """
        print("\n" + "=" * 60)
        print("STEP 2: RFM CALCULATION AND SEGMENTATION")
        print("=" * 60)
        
        if self.rfm_data is None:
            raise ValueError("No RFM data available. Run load_and_process_data() first.")
        
        # Calculate RFM scores
        self.rfm_scores = self.rfm_calculator.calculate_rfm_scores(
            self.rfm_data, n_quantiles=n_quantiles
        )
        
        # Create segments
        self.segments = self.rfm_calculator.create_segments(self.rfm_scores)
        
        # Save results
        self.rfm_scores.to_csv(f"{self.output_dir}/data/rfm_scores.csv", index=False)
        self.segments.to_csv(f"{self.output_dir}/data/rfm_segments.csv", index=False)
        
        return self.segments
    
    def perform_clustering_analysis(self, n_clusters: Optional[int] = None,
                                  max_clusters: int = 10) -> Tuple[pd.DataFrame, Dict]:
        """
        Perform machine learning clustering analysis
        
        Args:
            n_clusters: Number of clusters (auto-determined if None)
            max_clusters: Maximum clusters to test
            
        Returns:
            Tuple of (clustered data, clustering results)
        """
        print("\n" + "=" * 60)
        print("STEP 3: MACHINE LEARNING CLUSTERING")
        print("=" * 60)
        
        if self.rfm_data is None:
            raise ValueError("No RFM data available. Run load_and_process_data() first.")
        
        # Perform clustering
        self.clusters, clustering_results = self.rfm_calculator.perform_clustering(
            self.rfm_data, n_clusters=n_clusters, max_clusters=max_clusters
        )
        
        # Save results
        self.clusters.to_csv(f"{self.output_dir}/data/rfm_clusters.csv", index=False)
        
        return self.clusters, clustering_results
    
    def generate_marketing_strategies(self) -> pd.DataFrame:
        """
        Generate marketing strategies for all segments
        
        Returns:
            DataFrame with marketing strategies
        """
        print("\n" + "=" * 60)
        print("STEP 4: MARKETING STRATEGY DEVELOPMENT")
        print("=" * 60)
        
        if self.segments is None:
            raise ValueError("No segments available. Run calculate_rfm_analysis() first.")
        
        # Generate strategies
        self.strategies = self.strategy_generator.generate_strategies_for_segments(self.segments)
        
        # Save strategies
        self.strategies.to_csv(f"{self.output_dir}/data/marketing_strategies.csv", index=False)
        
        print("Marketing strategies generated for all segments")
        return self.strategies
    
    def create_visualizations(self, include_clusters: bool = True) -> None:
        """
        Create comprehensive visualizations
        
        Args:
            include_clusters: Whether to include cluster visualizations
        """
        print("\n" + "=" * 60)
        print("STEP 5: VISUALIZATION GENERATION")
        print("=" * 60)
        
        if self.rfm_data is None or self.segments is None:
            raise ValueError("Insufficient data for visualization. Complete analysis first.")
        
        # Create comprehensive visualization report
        self.plotter.create_comprehensive_report(
            rfm_data=self.rfm_data,
            segments_data=self.segments,
            clusters_data=self.clusters if include_clusters else None,
            output_dir=f"{self.output_dir}/visualizations"
        )
        
        print("All visualizations generated successfully")
    
    def generate_report(self, include_clusters: bool = True,
                       total_budget: float = 100000) -> str:
        """
        Generate comprehensive HTML report
        
        Args:
            include_clusters: Whether to include cluster analysis
            total_budget: Total marketing budget for strategy allocation
            
        Returns:
            Path to generated report
        """
        print("\n" + "=" * 60)
        print("STEP 6: COMPREHENSIVE REPORT GENERATION")
        print("=" * 60)
        
        if self.segments is None:
            raise ValueError("No analysis results available. Complete analysis first.")
        
        # Get analysis summaries
        segment_analysis = self.rfm_calculator.get_segment_analysis()
        budget_allocation = self.strategy_generator.calculate_budget_allocation(
            total_budget, self.segments
        )
        
        # Generate HTML report
        report_path = f"{self.output_dir}/reports/rfm_comprehensive_report.html"
        
        html_content = self._create_html_report(
            segment_analysis, budget_allocation, include_clusters
        )
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        print(f"Comprehensive report generated: {report_path}")
        return report_path
    
    def _create_html_report(self, segment_analysis: pd.DataFrame,
                          budget_allocation: Dict, include_clusters: bool) -> str:
        """Create HTML report content"""
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>RFM Analysis Comprehensive Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .summary-box {{ background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #bdc3c7; padding: 12px; text-align: left; }}
        th {{ background-color: #34495e; color: white; }}
        .highlight {{ background-color: #f39c12; color: white; padding: 5px 10px; border-radius: 3px; }}
        .success {{ background-color: #27ae60; color: white; padding: 5px 10px; border-radius: 3px; }}
        .warning {{ background-color: #e74c3c; color: white; padding: 5px 10px; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>🎯 RFM Analysis Comprehensive Report</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="summary-box">
        <h2>📊 Executive Summary</h2>
        <p>This comprehensive RFM analysis provides actionable insights for customer segmentation, 
        retention strategies, and marketing optimization. The analysis covers {len(self.segments):,} customers 
        across {len(self.segments['Segment'].unique())} distinct segments.</p>
    </div>
    
    <h2>👥 Customer Segment Analysis</h2>
    <table>
        <tr>
            <th>Segment</th>
            <th>Customers</th>
            <th>Percentage</th>
            <th>Avg Recency</th>
            <th>Avg Frequency</th>
            <th>Avg Monetary</th>
        </tr>
"""
        
        # Add segment analysis rows
        for _, row in segment_analysis.iterrows():
            html += f"""
        <tr>
            <td>{row['Segment']}</td>
            <td>{row['CustomerID_count']:,}</td>
            <td>{row['Percentage']:.1f}%</td>
            <td>{row['Recency_mean']:.1f}</td>
            <td>{row['Frequency_mean']:.1f}</td>
            <td>${row['Monetary_mean']:,.0f}</td>
        </tr>
"""
        
        html += """
    </table>
    
    <h2>💰 Budget Allocation Strategy</h2>
    <table>
        <tr>
            <th>Segment</th>
            <th>Customers</th>
            <th>Budget Allocation</th>
            <th>Budget Amount</th>
            <th>Cost per Customer</th>
        </tr>
"""
        
        # Add budget allocation rows
        for segment, allocation in budget_allocation.items():
            html += f"""
        <tr>
            <td>{segment}</td>
            <td>{allocation['customers_count']:,}</td>
            <td>{allocation['allocation_percentage']*100:.1f}%</td>
            <td>${allocation['budget_amount']:,.0f}</td>
            <td>${allocation['budget_per_customer']:.2f}</td>
        </tr>
"""
        
        html += f"""
    </table>
    
    <h2>📈 Key Insights & Recommendations</h2>
    <div class="summary-box">
        <h3>🎯 Top Priority Segments:</h3>
        <ul>
            <li><span class="highlight">Champions</span>: Focus on retention and referral programs</li>
            <li><span class="success">Loyal Customers</span>: Implement cross-sell and up-sell strategies</li>
            <li><span class="warning">At Risk</span>: Launch immediate win-back campaigns</li>
        </ul>
        
        <h3>💡 Strategic Recommendations:</h3>
        <ul>
            <li>Allocate 60% of budget to high-value segments (Champions, Loyal Customers)</li>
            <li>Implement automated win-back campaigns for At Risk customers</li>
            <li>Develop personalized onboarding for New Customers</li>
            <li>Create referral programs to leverage Champions' influence</li>
        </ul>
    </div>
    
    <h2>📁 Generated Files</h2>
    <ul>
        <li><strong>Data Files:</strong> rfm_data.csv, rfm_scores.csv, rfm_segments.csv</li>
        <li><strong>Visualizations:</strong> Complete set of charts and plots</li>
        <li><strong>Strategies:</strong> marketing_strategies.csv with detailed action plans</li>
"""
        
        if include_clusters:
            html += "        <li><strong>Clustering:</strong> Machine learning cluster analysis</li>"
        
        html += """
    </ul>
    
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #bdc3c7;">
        <p><em>Report generated by RFM Insight Engine v1.0.0</em></p>
    </footer>
</body>
</html>
"""
        
        return html
    
    def run_complete_analysis(self, file_path: str, 
                            analysis_date: Optional[datetime] = None,
                            include_clustering: bool = True,
                            total_budget: float = 100000,
                            **kwargs) -> Dict[str, Any]:
        """
        Run complete RFM analysis pipeline
        
        Args:
            file_path: Path to transaction data
            analysis_date: Reference date for analysis
            include_clustering: Whether to include ML clustering
            total_budget: Marketing budget for strategy allocation
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with all analysis results
        """
        print("🚀 STARTING COMPLETE RFM ANALYSIS")
        print("=" * 80)
        
        try:
            # Step 1: Load and process data
            self.load_and_process_data(file_path, analysis_date, **kwargs)
            
            # Step 2: Calculate RFM analysis
            self.calculate_rfm_analysis()
            
            # Step 3: Perform clustering (optional)
            if include_clustering:
                self.perform_clustering_analysis()
            
            # Step 4: Generate marketing strategies
            self.generate_marketing_strategies()
            
            # Step 5: Create visualizations
            self.create_visualizations(include_clustering)
            
            # Step 6: Generate comprehensive report
            report_path = self.generate_report(include_clustering, total_budget)
            
            print("\n" + "=" * 80)
            print("✅ RFM ANALYSIS COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            print(f"📊 All results saved to: {self.output_dir}/")
            print(f"📄 Comprehensive report: {report_path}")
            
            # Return results summary
            results = {
                'rfm_data': self.rfm_data,
                'rfm_scores': self.rfm_scores,
                'segments': self.segments,
                'clusters': self.clusters if include_clustering else None,
                'strategies': self.strategies,
                'output_directory': self.output_dir,
                'report_path': report_path
            }
            
            return results
            
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
            raise


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='RFM Insight Engine')
    parser.add_argument('data_file', help='Path to transaction data CSV file')
    parser.add_argument('--output-dir', default='output', help='Output directory')
    parser.add_argument('--budget', type=float, default=100000, help='Marketing budget')
    parser.add_argument('--no-clustering', action='store_true', help='Skip clustering analysis')
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = RFMInsightEngine(output_dir=args.output_dir)
    
    # Run complete analysis
    results = engine.run_complete_analysis(
        file_path=args.data_file,
        include_clustering=not args.no_clustering,
        total_budget=args.budget
    )
    
    print("Analysis completed successfully!")


if __name__ == "__main__":
    main()
