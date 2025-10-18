"""
Data processing and preparation module for RFM analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, Any
import warnings


class DataProcessor:
    """
    Handles data loading, cleaning, and preparation for RFM analysis
    """
    
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
        self.analysis_date = None
        
    def load_data(self, file_path: str, 
                  customer_col: str = 'CustomerID',
                  date_col: str = 'InvoiceDate', 
                  amount_col: str = 'Amount',
                  invoice_col: str = 'InvoiceNo') -> pd.DataFrame:
        """
        Load transaction data from CSV file
        
        Args:
            file_path: Path to the CSV file
            customer_col: Name of customer ID column
            date_col: Name of date column
            amount_col: Name of amount column
            invoice_col: Name of invoice number column
            
        Returns:
            Loaded DataFrame
        """
        try:
            self.raw_data = pd.read_csv(file_path)
            
            # Standardize column names
            column_mapping = {
                customer_col: 'CustomerID',
                date_col: 'InvoiceDate',
                amount_col: 'Amount',
                invoice_col: 'InvoiceNo'
            }
            
            self.raw_data = self.raw_data.rename(columns=column_mapping)
            
            # Validate required columns
            required_columns = ['CustomerID', 'InvoiceDate', 'Amount']
            missing_columns = [col for col in required_columns if col not in self.raw_data.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
                
            print(f"Data loaded successfully: {len(self.raw_data)} records")
            return self.raw_data
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise
    
    def clean_data(self, 
                   remove_negative_amounts: bool = True,
                   remove_zero_amounts: bool = False,
                   min_amount: Optional[float] = None) -> pd.DataFrame:
        """
        Clean and validate transaction data
        
        Args:
            remove_negative_amounts: Remove transactions with negative amounts
            remove_zero_amounts: Remove transactions with zero amounts
            min_amount: Minimum transaction amount threshold
            
        Returns:
            Cleaned DataFrame
        """
        if self.raw_data is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        data = self.raw_data.copy()
        
        # Convert date column to datetime
        data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')
        
        # Remove rows with invalid dates
        invalid_dates = data['InvoiceDate'].isna()
        if invalid_dates.sum() > 0:
            print(f"Removing {invalid_dates.sum()} records with invalid dates")
            data = data[~invalid_dates]
        
        # Clean amount column
        data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
        
        # Remove rows with invalid amounts
        invalid_amounts = data['Amount'].isna()
        if invalid_amounts.sum() > 0:
            print(f"Removing {invalid_amounts.sum()} records with invalid amounts")
            data = data[~invalid_amounts]
        
        # Remove negative amounts
        if remove_negative_amounts:
            negative_amounts = data['Amount'] < 0
            if negative_amounts.sum() > 0:
                print(f"Removing {negative_amounts.sum()} records with negative amounts")
                data = data[~negative_amounts]
        
        # Remove zero amounts
        if remove_zero_amounts:
            zero_amounts = data['Amount'] == 0
            if zero_amounts.sum() > 0:
                print(f"Removing {zero_amounts.sum()} records with zero amounts")
                data = data[~zero_amounts]
        
        # Apply minimum amount threshold
        if min_amount is not None:
            below_threshold = data['Amount'] < min_amount
            if below_threshold.sum() > 0:
                print(f"Removing {below_threshold.sum()} records below minimum amount threshold")
                data = data[~below_threshold]
        
        # Remove duplicates
        initial_count = len(data)
        data = data.drop_duplicates()
        final_count = len(data)
        
        if initial_count != final_count:
            print(f"Removed {initial_count - final_count} duplicate records")
        
        self.processed_data = data
        print(f"Data cleaning completed: {len(data)} valid records remaining")
        
        return data
    
    def set_analysis_date(self, analysis_date: Optional[datetime] = None) -> datetime:
        """
        Set the analysis date for RFM calculations
        
        Args:
            analysis_date: Date to use as reference point. If None, uses max date + 1 day
            
        Returns:
            Analysis date used
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Call clean_data() first.")
        
        if analysis_date is None:
            # Use the day after the latest transaction
            max_date = self.processed_data['InvoiceDate'].max()
            self.analysis_date = max_date + timedelta(days=1)
        else:
            self.analysis_date = analysis_date
        
        print(f"Analysis date set to: {self.analysis_date.strftime('%Y-%m-%d')}")
        return self.analysis_date
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of the processed data
        
        Returns:
            Dictionary with data summary statistics
        """
        if self.processed_data is None:
            raise ValueError("No processed data available.")
        
        data = self.processed_data
        
        summary = {
            'total_transactions': len(data),
            'unique_customers': data['CustomerID'].nunique(),
            'date_range': {
                'start': data['InvoiceDate'].min(),
                'end': data['InvoiceDate'].max(),
                'days': (data['InvoiceDate'].max() - data['InvoiceDate'].min()).days
            },
            'amount_statistics': {
                'total_revenue': data['Amount'].sum(),
                'avg_transaction': data['Amount'].mean(),
                'median_transaction': data['Amount'].median(),
                'min_transaction': data['Amount'].min(),
                'max_transaction': data['Amount'].max()
            },
            'customer_statistics': {
                'avg_transactions_per_customer': len(data) / data['CustomerID'].nunique(),
                'avg_revenue_per_customer': data['Amount'].sum() / data['CustomerID'].nunique()
            }
        }
        
        return summary
    
    def prepare_rfm_data(self) -> pd.DataFrame:
        """
        Prepare data for RFM analysis by aggregating customer-level metrics
        
        Returns:
            DataFrame with customer-level aggregated data
        """
        if self.processed_data is None:
            raise ValueError("No processed data available.")
        
        if self.analysis_date is None:
            self.set_analysis_date()
        
        data = self.processed_data
        
        # Calculate RFM metrics
        rfm_data = data.groupby('CustomerID').agg({
            'InvoiceDate': 'max',  # Last purchase date
            'InvoiceNo': 'nunique',  # Number of unique invoices (frequency)
            'Amount': 'sum'  # Total monetary value
        }).reset_index()
        
        # Rename columns
        rfm_data.columns = ['CustomerID', 'LastPurchaseDate', 'Frequency', 'Monetary']
        
        # Calculate Recency
        rfm_data['Recency'] = (self.analysis_date - rfm_data['LastPurchaseDate']).dt.days
        
        # Reorder columns
        rfm_data = rfm_data[['CustomerID', 'Recency', 'Frequency', 'Monetary']]
        
        print(f"RFM data prepared for {len(rfm_data)} customers")
        
        return rfm_data
