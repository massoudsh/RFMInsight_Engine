#!/usr/bin/env python3
"""
RFM Insight Engine - Command Line Interface

Quick start script for running complete RFM analysis from command line.
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from engine import RFMInsightEngine


def main():
    """Main function for command-line usage"""
    print("🚀 RFM Insight Engine - Command Line Analysis")
    print("=" * 60)
    
    # Check if data file exists
    data_file = 'data/RFM_dataset.csv'
    if not os.path.exists(data_file):
        print(f"❌ Error: Data file not found at {data_file}")
        print("Please ensure the data file exists in the data/ directory.")
        return
    
    # Initialize engine
    output_dir = f"output/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    engine = RFMInsightEngine(output_dir=output_dir)
    
    print(f"📊 Starting analysis with data file: {data_file}")
    print(f"📁 Output directory: {output_dir}")
    print()
    
    try:
        # Run complete analysis
        results = engine.run_complete_analysis(
            file_path=data_file,
            include_clustering=True,
            total_budget=100000
        )
        
        print("\n🎉 Analysis completed successfully!")
        print(f"📄 Check the comprehensive report: {results['report_path']}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
