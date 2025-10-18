"""
Advanced visualization module for RFM analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Tuple
import warnings

# Set style
plt.style.use('default')
sns.set_palette("husl")


class RFMPlotter:
    """
    Advanced plotting class for RFM analysis visualizations
    """
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8), dpi: int = 300):
        self.figsize = figsize
        self.dpi = dpi
        self.color_palette = sns.color_palette("husl", 10)
        
    def plot_rfm_distributions(self, rfm_data: pd.DataFrame, 
                              save_path: Optional[str] = None) -> None:
        """
        Plot distribution of RFM metrics
        
        Args:
            rfm_data: DataFrame with Recency, Frequency, Monetary columns
            save_path: Path to save the plot
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Recency distribution
        axes[0].hist(rfm_data['Recency'], bins=30, alpha=0.7, color=self.color_palette[0])
        axes[0].set_title('Recency Distribution')
        axes[0].set_xlabel('Days Since Last Purchase')
        axes[0].set_ylabel('Number of Customers')
        axes[0].grid(True, alpha=0.3)
        
        # Frequency distribution
        axes[1].hist(rfm_data['Frequency'], bins=30, alpha=0.7, color=self.color_palette[1])
        axes[1].set_title('Frequency Distribution')
        axes[1].set_xlabel('Number of Purchases')
        axes[1].set_ylabel('Number of Customers')
        axes[1].grid(True, alpha=0.3)
        
        # Monetary distribution
        axes[2].hist(rfm_data['Monetary'], bins=30, alpha=0.7, color=self.color_palette[2])
        axes[2].set_title('Monetary Distribution')
        axes[2].set_xlabel('Total Amount Spent')
        axes[2].set_ylabel('Number of Customers')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
    
    def plot_segment_distribution(self, segments_data: pd.DataFrame,
                                 save_path: Optional[str] = None) -> None:
        """
        Plot customer segment distribution
        
        Args:
            segments_data: DataFrame with Segment column
            save_path: Path to save the plot
        """
        segment_counts = segments_data['Segment'].value_counts()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Bar plot
        bars = ax1.bar(range(len(segment_counts)), segment_counts.values, 
                      color=self.color_palette[:len(segment_counts)])
        ax1.set_title('Customer Segment Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Segments')
        ax1.set_ylabel('Number of Customers')
        ax1.set_xticks(range(len(segment_counts)))
        ax1.set_xticklabels(segment_counts.index, rotation=45, ha='right')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Pie chart
        colors = self.color_palette[:len(segment_counts)]
        wedges, texts, autotexts = ax2.pie(segment_counts.values, 
                                          labels=segment_counts.index,
                                          autopct='%1.1f%%',
                                          colors=colors,
                                          startangle=90)
        
        ax2.set_title('Customer Segment Distribution (%)', fontsize=14, fontweight='bold')
        
        # Improve text readability
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
    
    def plot_rfm_heatmap(self, segments_data: pd.DataFrame,
                        save_path: Optional[str] = None) -> None:
        """
        Plot RFM heatmap by segments
        
        Args:
            segments_data: DataFrame with RFM scores and Segment column
            save_path: Path to save the plot
        """
        # Calculate mean RFM scores by segment
        heatmap_data = segments_data.groupby('Segment')[['R_Score', 'F_Score', 'M_Score']].mean()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(heatmap_data, annot=True, cmap='RdYlBu_r', 
                   cbar_kws={'label': 'Average Score'}, fmt='.1f')
        plt.title('Average RFM Scores by Segment', fontsize=14, fontweight='bold')
        plt.xlabel('RFM Dimensions')
        plt.ylabel('Customer Segments')
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
    
    def plot_clustering_analysis(self, clustering_results: Dict,
                               save_path: Optional[str] = None) -> None:
        """
        Plot clustering analysis (elbow method and silhouette analysis)
        
        Args:
            clustering_results: Dictionary with clustering results
            save_path: Path to save the plot
        """
        # This would need to be implemented based on the clustering results structure
        # For now, create a placeholder
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Clustering Analysis Plot\n(Implementation needed)', 
                ha='center', va='center', fontsize=16)
        ax.set_title('Clustering Analysis')
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
    
    def plot_interactive_rfm_3d(self, rfm_data: pd.DataFrame,
                               segments_data: Optional[pd.DataFrame] = None,
                               save_path: Optional[str] = None) -> None:
        """
        Create interactive 3D scatter plot of RFM dimensions
        
        Args:
            rfm_data: DataFrame with Recency, Frequency, Monetary columns
            segments_data: DataFrame with segment information
            save_path: Path to save the HTML file
        """
        if segments_data is not None:
            # Merge data
            plot_data = rfm_data.merge(segments_data[['CustomerID', 'Segment']], on='CustomerID')
            color_col = 'Segment'
        else:
            plot_data = rfm_data
            color_col = None
        
        fig = px.scatter_3d(plot_data, 
                           x='Recency', 
                           y='Frequency', 
                           z='Monetary',
                           color=color_col,
                           hover_data=['CustomerID'],
                           title='RFM Analysis - 3D Scatter Plot',
                           labels={'Recency': 'Recency (Days)',
                                 'Frequency': 'Frequency (Purchases)',
                                 'Monetary': 'Monetary (Total Amount)'})
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Recency (Days)',
                yaxis_title='Frequency (Purchases)',
                zaxis_title='Monetary (Total Amount)'
            ),
            width=800,
            height=600
        )
        
        if save_path:
            fig.write_html(save_path)
        
        fig.show()
    
    def plot_segment_comparison(self, segments_data: pd.DataFrame,
                              clusters_data: Optional[pd.DataFrame] = None,
                              save_path: Optional[str] = None) -> None:
        """
        Plot comparison between rule-based segments and ML clusters
        
        Args:
            segments_data: DataFrame with rule-based segments
            clusters_data: DataFrame with cluster assignments
            save_path: Path to save the plot
        """
        if clusters_data is not None:
            # Create crosstab
            comparison_data = pd.crosstab(segments_data['Segment'], clusters_data['Cluster'])
            
            plt.figure(figsize=(12, 8))
            sns.heatmap(comparison_data, annot=True, fmt='d', cmap='Blues',
                       cbar_kws={'label': 'Number of Customers'})
            plt.title('Rule-based Segments vs ML Clusters', fontsize=14, fontweight='bold')
            plt.xlabel('ML Clusters')
            plt.ylabel('Rule-based Segments')
            
            if save_path:
                plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            
            plt.show()
        else:
            print("No cluster data provided for comparison")
    
    def plot_customer_journey(self, segments_data: pd.DataFrame,
                            save_path: Optional[str] = None) -> None:
        """
        Plot customer journey visualization
        
        Args:
            segments_data: DataFrame with segment information
            save_path: Path to save the plot
        """
        # Define customer journey stages
        journey_mapping = {
            'New Customers': 'Acquisition',
            'Potential Loyalist': 'Activation',
            'Promising': 'Activation',
            'Champions': 'Retention',
            'Loyal Customers': 'Retention',
            'Need Attention': 'Retention',
            'About to Sleep': 'Retention',
            'At Risk': 'Retention',
            'Cannot Lose Them': 'Retention',
            'Hibernating': 'Retention',
            'Lost': 'Churn'
        }
        
        journey_data = segments_data.copy()
        journey_data['Stage'] = journey_data['Segment'].map(journey_mapping)
        
        stage_counts = journey_data['Stage'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create funnel-like visualization
        bars = ax.barh(range(len(stage_counts)), stage_counts.values,
                      color=self.color_palette[:len(stage_counts)])
        
        ax.set_yticks(range(len(stage_counts)))
        ax.set_yticklabels(stage_counts.index)
        ax.set_xlabel('Number of Customers')
        ax.set_title('Customer Journey Stages', fontsize=14, fontweight='bold')
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
                   f'{int(width)}', ha='left', va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
    
    def create_comprehensive_report(self, rfm_data: pd.DataFrame,
                                  segments_data: pd.DataFrame,
                                  clusters_data: Optional[pd.DataFrame] = None,
                                  output_dir: str = 'visualizations') -> None:
        """
        Create comprehensive visualization report
        
        Args:
            rfm_data: DataFrame with RFM metrics
            segments_data: DataFrame with segment assignments
            clusters_data: Optional DataFrame with cluster assignments
            output_dir: Directory to save visualizations
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate all visualizations
        print("Generating comprehensive RFM visualization report...")
        
        self.plot_rfm_distributions(rfm_data, 
                                   f"{output_dir}/rfm_distributions.png")
        
        self.plot_segment_distribution(segments_data,
                                     f"{output_dir}/segment_distribution.png")
        
        self.plot_rfm_heatmap(segments_data,
                             f"{output_dir}/rfm_heatmap.png")
        
        self.plot_interactive_rfm_3d(rfm_data, segments_data,
                                    f"{output_dir}/rfm_3d_plot.html")
        
        if clusters_data is not None:
            self.plot_segment_comparison(segments_data, clusters_data,
                                        f"{output_dir}/segment_vs_cluster.png")
        
        self.plot_customer_journey(segments_data,
                                  f"{output_dir}/customer_journey.png")
        
        print(f"Visualization report saved to {output_dir}/")
        print("Generated files:")
        print("- rfm_distributions.png")
        print("- segment_distribution.png")
        print("- rfm_heatmap.png")
        print("- rfm_3d_plot.html")
        if clusters_data is not None:
            print("- segment_vs_cluster.png")
        print("- customer_journey.png")
