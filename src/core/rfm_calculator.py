"""
RFM calculation and scoring module
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List, Optional
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings


class RFMCalculator:
    """
    Handles RFM calculation, scoring, and segmentation
    """
    
    def __init__(self):
        self.rfm_data = None
        self.rfm_scores = None
        self.segments = None
        self.clusters = None
        
    def calculate_rfm_scores(self, rfm_data: pd.DataFrame, 
                           method: str = 'quantile',
                           n_quantiles: int = 5) -> pd.DataFrame:
        """
        Calculate RFM scores based on quantiles or percentiles
        
        Args:
            rfm_data: DataFrame with Recency, Frequency, Monetary columns
            method: Scoring method ('quantile' or 'percentile')
            n_quantiles: Number of quantiles for scoring (default 5)
            
        Returns:
            DataFrame with RFM scores
        """
        self.rfm_data = rfm_data.copy()
        
        # For Recency, lower values are better (more recent)
        # For Frequency and Monetary, higher values are better
        self.rfm_data['R_Score'] = pd.qcut(
            self.rfm_data['Recency'].rank(method='first'), 
            q=n_quantiles, 
            labels=list(range(1, n_quantiles + 1))
        ).astype(int)
        
        # Reverse Recency scores (1 = most recent, 5 = least recent)
        self.rfm_data['R_Score'] = n_quantiles + 1 - self.rfm_data['R_Score']
        
        self.rfm_data['F_Score'] = pd.qcut(
            self.rfm_data['Frequency'].rank(method='first'), 
            q=n_quantiles, 
            labels=list(range(1, n_quantiles + 1))
        ).astype(int)
        
        self.rfm_data['M_Score'] = pd.qcut(
            self.rfm_data['Monetary'].rank(method='first'), 
            q=n_quantiles, 
            labels=list(range(1, n_quantiles + 1))
        ).astype(int)
        
        # Create combined RFM score
        self.rfm_data['RFM_Score'] = (
            self.rfm_data['R_Score'].astype(str) + 
            self.rfm_data['F_Score'].astype(str) + 
            self.rfm_data['M_Score'].astype(str)
        ).astype(int)
        
        self.rfm_scores = self.rfm_data.copy()
        
        print(f"RFM scores calculated for {len(self.rfm_scores)} customers")
        return self.rfm_scores
    
    def create_segments(self, rfm_scores: pd.DataFrame) -> pd.DataFrame:
        """
        Create customer segments based on RFM scores
        
        Args:
            rfm_scores: DataFrame with RFM scores
            
        Returns:
            DataFrame with segment assignments
        """
        if rfm_scores is None:
            raise ValueError("No RFM scores available. Call calculate_rfm_scores() first.")
        
        data = rfm_scores.copy()
        
        # Define segment rules based on RFM scores
        def assign_segment(row):
            r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
            
            # Champions: High R, F, M
            if r >= 4 and f >= 4 and m >= 4:
                return 'Champions'
            
            # Loyal Customers: High F, good R and M
            elif r >= 3 and f >= 3 and m >= 3:
                return 'Loyal Customers'
            
            # Potential Loyalists: Good R, moderate F and M
            elif r >= 4 and f >= 2 and m >= 2:
                return 'Potential Loyalist'
            
            # New Customers: High R, low F and M
            elif r >= 4 and f <= 2 and m <= 2:
                return 'New Customers'
            
            # Promising: Good R and F, low M
            elif r >= 3 and f >= 3 and m <= 2:
                return 'Promising'
            
            # Need Attention: Moderate R, F, M
            elif r >= 2 and f >= 2 and m >= 2:
                return 'Need Attention'
            
            # About to Sleep: Low R, moderate F and M
            elif r <= 2 and f >= 2 and m >= 2:
                return 'About to Sleep'
            
            # At Risk: Low R, good F and M
            elif r <= 2 and f >= 3 and m >= 3:
                return 'At Risk'
            
            # Cannot Lose Them: Low R, high F and M
            elif r <= 1 and f >= 4 and m >= 4:
                return 'Cannot Lose Them'
            
            # Hibernating: Low R and F, moderate M
            elif r <= 2 and f <= 2 and m >= 2:
                return 'Hibernating'
            
            # Lost: Low R, F, M
            else:
                return 'Lost'
        
        data['Segment'] = data.apply(assign_segment, axis=1)
        
        self.segments = data
        
        # Print segment distribution
        segment_counts = data['Segment'].value_counts()
        print("Segment Distribution:")
        for segment, count in segment_counts.items():
            percentage = (count / len(data)) * 100
            print(f"  {segment}: {count} customers ({percentage:.1f}%)")
        
        return data
    
    def perform_clustering(self, rfm_data: pd.DataFrame, 
                          n_clusters: Optional[int] = None,
                          max_clusters: int = 10,
                          random_state: int = 42) -> Tuple[pd.DataFrame, Dict]:
        """
        Perform K-means clustering on RFM data
        
        Args:
            rfm_data: DataFrame with Recency, Frequency, Monetary columns
            n_clusters: Number of clusters. If None, optimal k is determined
            max_clusters: Maximum number of clusters to test
            random_state: Random state for reproducibility
            
        Returns:
            Tuple of (DataFrame with cluster assignments, clustering results)
        """
        # Prepare data for clustering
        clustering_data = rfm_data[['Recency', 'Frequency', 'Monetary']].copy()
        
        # Log transform to handle skewness
        clustering_data['Frequency'] = np.log1p(clustering_data['Frequency'])
        clustering_data['Monetary'] = np.log1p(clustering_data['Monetary'])
        
        # Standardize features
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(clustering_data)
        
        # Determine optimal number of clusters if not specified
        if n_clusters is None:
            n_clusters = self._find_optimal_clusters(scaled_data, max_clusters)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        cluster_labels = kmeans.fit_predict(scaled_data)
        
        # Add cluster labels to data
        result_data = rfm_data.copy()
        result_data['Cluster'] = cluster_labels
        
        # Calculate silhouette score
        silhouette_avg = silhouette_score(scaled_data, cluster_labels)
        
        clustering_results = {
            'n_clusters': n_clusters,
            'silhouette_score': silhouette_avg,
            'cluster_centers': kmeans.cluster_centers_,
            'inertia': kmeans.inertia_,
            'scaler': scaler
        }
        
        self.clusters = result_data
        
        print(f"Clustering completed with {n_clusters} clusters")
        print(f"Silhouette Score: {silhouette_avg:.3f}")
        
        # Print cluster distribution
        cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()
        print("Cluster Distribution:")
        for cluster, count in cluster_counts.items():
            percentage = (count / len(result_data)) * 100
            print(f"  Cluster {cluster}: {count} customers ({percentage:.1f}%)")
        
        return result_data, clustering_results
    
    def _find_optimal_clusters(self, data: np.ndarray, max_clusters: int) -> int:
        """
        Find optimal number of clusters using elbow method and silhouette analysis
        
        Args:
            data: Scaled RFM data
            max_clusters: Maximum number of clusters to test
            
        Returns:
            Optimal number of clusters
        """
        inertias = []
        silhouette_scores = []
        k_range = range(2, max_clusters + 1)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(data)
            
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(data, cluster_labels))
        
        # Find elbow point
        elbow_idx = self._find_elbow_point(inertias)
        elbow_k = k_range[elbow_idx]
        
        # Find best silhouette score
        best_silhouette_idx = np.argmax(silhouette_scores)
        best_silhouette_k = k_range[best_silhouette_idx]
        
        # Use silhouette-based k if it's close to elbow, otherwise use elbow
        if abs(best_silhouette_k - elbow_k) <= 1:
            optimal_k = best_silhouette_k
            method = "silhouette"
        else:
            optimal_k = elbow_k
            method = "elbow"
        
        print(f"Optimal clusters determined by {method} method: {optimal_k}")
        print(f"Elbow method suggests: {elbow_k}")
        print(f"Silhouette method suggests: {best_silhouette_k}")
        
        return optimal_k
    
    def _find_elbow_point(self, inertias: List[float]) -> int:
        """
        Find elbow point in inertia curve
        
        Args:
            inertias: List of inertia values
            
        Returns:
            Index of elbow point
        """
        # Calculate second derivative to find elbow
        if len(inertias) < 3:
            return 0
        
        # Calculate second differences
        second_diff = np.diff(inertias, n=2)
        
        # Find point with maximum second difference (elbow)
        elbow_idx = np.argmax(second_diff)
        
        return elbow_idx
    
    def get_segment_analysis(self) -> pd.DataFrame:
        """
        Get detailed analysis of segments
        
        Returns:
            DataFrame with segment statistics
        """
        if self.segments is None:
            raise ValueError("No segments available. Call create_segments() first.")
        
        segment_analysis = self.segments.groupby('Segment').agg({
            'Recency': ['mean', 'std'],
            'Frequency': ['mean', 'std'],
            'Monetary': ['mean', 'std'],
            'CustomerID': 'count'
        }).round(2)
        
        # Flatten column names
        segment_analysis.columns = ['_'.join(col).strip() for col in segment_analysis.columns]
        segment_analysis = segment_analysis.reset_index()
        
        # Calculate percentages
        total_customers = len(self.segments)
        segment_analysis['Percentage'] = (segment_analysis['CustomerID_count'] / total_customers * 100).round(1)
        
        return segment_analysis
    
    def get_cluster_analysis(self) -> pd.DataFrame:
        """
        Get detailed analysis of clusters
        
        Returns:
            DataFrame with cluster statistics
        """
        if self.clusters is None:
            raise ValueError("No clusters available. Call perform_clustering() first.")
        
        cluster_analysis = self.clusters.groupby('Cluster').agg({
            'Recency': ['mean', 'std'],
            'Frequency': ['mean', 'std'],
            'Monetary': ['mean', 'std'],
            'CustomerID': 'count'
        }).round(2)
        
        # Flatten column names
        cluster_analysis.columns = ['_'.join(col).strip() for col in cluster_analysis.columns]
        cluster_analysis = cluster_analysis.reset_index()
        
        # Calculate percentages
        total_customers = len(self.clusters)
        cluster_analysis['Percentage'] = (cluster_analysis['CustomerID_count'] / total_customers * 100).round(1)
        
        return cluster_analysis
