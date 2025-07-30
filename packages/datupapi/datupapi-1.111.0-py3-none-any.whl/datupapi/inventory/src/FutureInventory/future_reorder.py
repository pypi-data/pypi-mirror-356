import pandas as pd
import os
import ast
import numpy as np
from datetime import timedelta
from datupapi.utils.utils import Utils
from datupapi.inventory.src.SuggestedForecast.suggested_forecast import SuggestedForecast
from datupapi.inventory.src.FutureInventory.daily_usage_future import DailyUsageFuture


class FutureReorder():
    """
    A class for calculating future inventory reorder points and quantities.
    
    This class implements a sophisticated inventory management system that:
    - Calculates optimal reorder points based on forecasted demand
    - Manages in-transit inventory and arrival schedules
    - Determines safety stock levels using statistical or reference methods
    - Generates reorder recommendations for multiple future periods
    - Supports both single-location and multi-location inventory
    
    The system uses dynamic coverage strategies to optimize inventory levels
    while maintaining adequate safety stock to prevent stockouts.
    
    Output Fields:
    - FutureInventoryTransit: Total future inventory (stock + transit)
    - FutureInventory: Future inventory in stock only
    - FutureTransit: Future inventory in transit only
    - FutureInventoryTransitArrival: Future inventory in stock + arrivals in the period
    """

    def __init__(self, df_inv, df_lead_time, df_prep, df_fcst, periods, start_date, location=False, security_stock_ref=False, df_transit=None, integer=True, complete_suggested=False, start_date_zero=None):
        """
        Initialize the FutureReorder instance.
        
        Args:
            df_inv (pd.DataFrame): Current inventory data with columns:
                - Item: Item identifier
                - Location: Location identifier (if location=True)
                - Inventory: Current on-hand stock
                - Transit: In-transit quantity
                - PurchaseFactor: Minimum order multiple
            
            df_lead_time (pd.DataFrame): Lead time and reorder parameters:
                - Item: Item identifier
                - Location: Location identifier (if location=True)
                - ReorderFreq: Days between reorders (default: 30)
                - AvgLeadTime: Average lead time in days
                - MaxLeadTime: Maximum lead time in days
                - Coverage: Total coverage days (optional)
                - SecurityStockDaysRef: Reference days for safety stock (optional)
            
            df_prep (pd.DataFrame): Preparation data for forecast calculations
            
            df_fcst (pd.DataFrame): Forecast data containing demand predictions
            
            periods (int): Number of future periods to calculate
            
            start_date (str): Starting date for calculations (format: 'YYYY-MM-DD')
            
            location (bool, optional): Whether to process by location. Defaults to False.
            
            security_stock_ref (bool, optional): Use reference days method for safety stock
                calculation instead of statistical method. Defaults to False.
                
            df_transit (pd.DataFrame, optional): Transit arrival schedule with columns:
                - Item: Item identifier
                - Location: Location identifier (if location=True)
                - Transit: Partial transit quantity
                - ArrivalDate: Arrival date (format: 'YYYY-MM-DD')
                If None, complete transit arrives in period 1. Defaults to None.
                
            integer (bool, optional): Controls numeric formatting of quantity fields.
                When True, quantity fields are displayed as integers.
                When False, quantity fields are displayed with decimals.
                Defaults to True.
                
            complete_suggested (bool, optional): When True, uses the last calculated
                SuggestedForecast value for periods without forecast data instead of
                raising an error. Defaults to False.
                
            start_date_zero (str, optional): Custom start date for period 0 (format: 'YYYY-MM-DD').
                When None (default), uses the current system date for period 0.
                When specified, uses this date as the starting point for period 0 instead
                of the current system date. Defaults to None.
        """
        self.df_inv = df_inv
        self.df_lead_time = df_lead_time
        self.df_prep = df_prep
        self.df_fcst = df_fcst
        self.default_coverage = 30
        self.periods = periods
        self.start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
        self.location = location
        self.security_stock_ref = security_stock_ref
        self.df_transit = df_transit
        self.integer = integer
        self.complete_suggested = complete_suggested
        self.start_date_zero = start_date_zero
        
        # Initialize metadata columns based on location usage
        self.metadata = ['Item']
        if self.location:
            self.metadata.append('Location')


    def _format_value(self, value, field_name):
        """
        Apply appropriate formatting based on field type and integer setting.
        
        Args:
            value: The numeric value to format (scalar or Series)
            field_name: The name of the field to determine formatting rules
            
        Returns:
            Formatted value (int or float with 2 decimals)
        """
        # Handle pandas Series - extract scalar value
        if isinstance(value, pd.Series):
            if len(value) == 1:
                value = value.iloc[0]
            else:
                raise ValueError(f"Expected scalar value for {field_name}, got Series with {len(value)} elements")
        
        # Handle NaN, None, and infinite values
        if pd.isna(value) or value is None:
            return 0
        if np.isinf(value):
            return 0
            
        # Fields that are ALWAYS integers
        always_integer_fields = [
            'PurchaseFactor', 'AvgLeadTime', 'MaxLeadTime',
            'ReorderQtyDays', 'ReorderFreq', 'Coverage', 'FutureStockoutDays'
        ]
        
        # Fields that are ALWAYS decimals (2 decimal places)
        always_decimal_fields = ['AvgDailyUsage', 'MaxDailyUsage']
        
        # Fields that change based on self.integer setting
        quantity_fields = [
            'FutureInventoryTransit', 'FutureInventory', 'FutureTransit',
            'FutureInventoryTransitArrival', 'SuggestedForecast', 'SuggestedForecastPeriod',
            'ReorderPoint', 'ReorderQtyBase', 'ReorderQty', 'SecurityStock', 'Inventory', 'Transit'
        ]
        
        if field_name in always_integer_fields:
            return int(round(value))
        elif field_name in always_decimal_fields:
            return round(value, 2)
        elif field_name in quantity_fields:
            if self.integer:
                return int(round(value))
            else:
                return round(value, 2)
        else:
            # Default: return as is
            return value


    def future_date(self):
        """
        Generate future reorder dates for each item based on reorder frequency.
        
        This method creates a schedule of dates when reorders should be evaluated
        for each item (or item-location combination). The schedule includes:
        1. Current date (always first)
        2. Start date (if after current date)
        3. Subsequent dates at reorder frequency intervals
        
        This optimized version groups items by reorder frequency for better performance
        with large datasets.
        
        Returns:
            dict: Dictionary mapping item (or (item, location) tuple) to list of
                  reorder dates in 'YYYYMMDD' format.
                  
        Example:
            {
                'ITEM001': ['20240101', '20240115', '20240214', ...],
                ('ITEM002', 'LOC1'): ['20240101', '20240120', '20240219', ...]
            }
        """
        # Determine the starting date for period 0
        if self.start_date_zero is not None:
            # Use custom start date for period 0
            actual_date = pd.to_datetime(self.start_date_zero, format='%Y-%m-%d')
        else:
            # Use current system date for period 0 (original behavior)
            DOCKER_CONFIG_PATH = os.path.join('/opt/ml/processing/input', 'config.yml')
            utils = Utils(config_file=DOCKER_CONFIG_PATH, logfile='data_io', log_path='output/logs')
            timestamp = utils.set_timestamp()
            actual_date = pd.to_datetime(str(int(float(timestamp[0:8]))), format='%Y%m%d')
        
        end_date = actual_date + pd.DateOffset(months=self.periods)

        # Get unique items with their reorder frequencies
        columns = self.metadata + ['ReorderFreq']
        df_unique = self.df_lead_time[columns].drop_duplicates().copy()
        
        # Process ReorderFreq values
        df_unique['ReorderFreq'] = df_unique['ReorderFreq'].fillna(self.default_coverage)
        df_unique.loc[df_unique['ReorderFreq'] == 0, 'ReorderFreq'] = self.default_coverage
        df_unique['ReorderFreq'] = df_unique['ReorderFreq'].astype(int)
        
        # Pre-allocate result dictionary
        item_dates = {}
        
        # Group by ReorderFreq for batch processing - more efficient for large datasets
        for freq, group in df_unique.groupby('ReorderFreq'):
            # Generate date range for this frequency
            date_range = []
            
            # Always include actual date
            date_range.append(actual_date)
            
            # Include start_date if after actual_date
            if self.start_date > actual_date:
                date_range.append(self.start_date)
            
            # Generate subsequent dates using pandas date_range for efficiency
            num_periods = int((end_date - self.start_date).days / freq) + 1
            future_dates = pd.date_range(
                start=self.start_date + timedelta(days=freq),
                periods=num_periods,
                freq=f'{freq}D'
            )
            date_range.extend(future_dates[future_dates <= end_date])
            
            # Convert to string format
            date_strings = [d.strftime('%Y%m%d') for d in date_range]
            
            # Assign to all items in this group
            for _, row in group.iterrows():
                if self.location:
                    key = (row['Item'], row['Location'])
                else:
                    key = row['Item']
                item_dates[key] = date_strings
        
        return item_dates


    def _get_current_dataframes(self, item, location=None):
        """
        Get filtered dataframes for current item/location combination.
        
        Args:
            item (str): Item identifier to filter for
            location (str, optional): Location identifier if using multi-location mode
            
        Returns:
            tuple: (current_df_lead_time, current_df_inv)
                - current_df_lead_time: Lead time data filtered for item/location
                - current_df_inv: Inventory data filtered for item/location
        """
        # Create filter mask based on item
        mask_lead_time = self.df_lead_time['Item'] == item
        mask_inv = self.df_inv['Item'] == item
        
        # Add location filter if needed
        if self.location and location is not None:
            mask_lead_time &= self.df_lead_time['Location'] == location
            mask_inv &= self.df_inv['Location'] == location
        
        # Apply filters using boolean indexing
        current_df_lead_time = self.df_lead_time[mask_lead_time]
        current_df_inv = self.df_inv[mask_inv]
        
        return current_df_lead_time, current_df_inv


    def _calculate_suggested_forecast(self, current_df_lead_time, current_df_inv, date, last_suggested_value=None):
        """
        Calculate suggested forecast for the given date using the SuggestedForecast class.
        
        This method now validates that sufficient forecast data exists to cover the
        required coverage period. If forecast data doesn't extend far enough into
        the future, it either raises an error or uses the last calculated value
        based on the complete_suggested parameter.
        
        Args:
            current_df_lead_time (pd.DataFrame): Lead time data for current item
            current_df_inv (pd.DataFrame): Inventory data for current item
            date (str): Date for forecast calculation in 'YYYYMMDD' format
            last_suggested_value (float, optional): Last calculated SuggestedForecast value
                to use when complete_suggested is True and forecast data is insufficient
            
        Returns:
            pd.DataFrame: DataFrame containing suggested forecast values
            
        Raises:
            ValueError: If forecast data doesn't extend far enough to cover the required period
                and complete_suggested is False or no previous value is available
        """
        # Convert current date to datetime
        current_date = pd.to_datetime(date, format='%Y%m%d')
        
        # Get the maximum forecast date available
        max_forecast_date = self.df_fcst['Date'].max()
        
        # Get coverage value for this item
        coverage = current_df_lead_time['Coverage'].iloc[0]
        
        # Calculate the required forecast end date
        required_forecast_end_date = current_date + timedelta(days=int(coverage))
        
        # Check if we have sufficient forecast data
        if max_forecast_date < required_forecast_end_date:
            # Get item identifier for error message
            item = current_df_inv['Item'].iloc[0]
            location_msg = ""
            if self.location and 'Location' in current_df_inv.columns:
                location = current_df_inv['Location'].iloc[0]
                location_msg = f" at location {location}"
            
            if self.complete_suggested:
                if last_suggested_value is not None:
                    # Use the last calculated SuggestedForecast value
                    # Create a DataFrame with the same structure as the normal output
                    result_df = current_df_inv[self.metadata].copy()
                    result_df['SuggestedForecast'] = last_suggested_value
                    
                    # Add PurchaseFactor and ItemDescription from inventory data
                    if 'PurchaseFactor' in current_df_inv.columns:
                        result_df['PurchaseFactor'] = current_df_inv['PurchaseFactor'].iloc[0]
                    else:
                        result_df['PurchaseFactor'] = 1  # Default value if not present
                    
                    if 'ItemDescription' in current_df_inv.columns:
                        result_df['ItemDescription'] = current_df_inv['ItemDescription'].iloc[0]
                    else:
                        result_df['ItemDescription'] = ''  # Default value if not present

                    return result_df
                else:
                    # For the first period when complete_suggested=True but no previous value exists,
                    # try to calculate with available data up to max_forecast_date
                    # This allows at least the first period to be calculated
                    try:
                        return SuggestedForecast(
                            df_LeadTimes=current_df_lead_time,
                            df_Forecast=self.df_fcst,
                            df_Prep=self.df_prep,
                            df_inv=current_df_inv,
                            column_forecast='SuggestedForecast',
                            columns_metadata=self.metadata,
                            frequency_='M',
                            location=self.location,
                            actualdate=date,
                            default_coverage_=self.default_coverage,
                            join_='left'
                        ).suggested_forecast()
                    except Exception as e:
                        # If even the basic calculation fails, raise a more informative error
                        error_msg = (
                            f"Cannot calculate initial forecast for item {item}{location_msg}. "
                            f"Forecast data extends only to {max_forecast_date.strftime('%Y-%m-%d')}, "
                            f"but coverage of {int(coverage)} days from {current_date.strftime('%Y-%m-%d')} "
                            f"requires forecast data until {required_forecast_end_date.strftime('%Y-%m-%d')}. "
                            f"Original error: {str(e)}"
                        )
                        raise ValueError(error_msg)
            else:
                error_msg = (
                    f"Insufficient forecast data for item {item}{location_msg}. "
                    f"Forecast data extends only to {max_forecast_date.strftime('%Y-%m-%d')}, "
                    f"but coverage of {int(coverage)} days from {current_date.strftime('%Y-%m-%d')} "
                    f"requires forecast data until {required_forecast_end_date.strftime('%Y-%m-%d')}."
                )
                raise ValueError(error_msg)
        
        # If validation passes, proceed with the original calculation
        return SuggestedForecast(
            df_LeadTimes=current_df_lead_time,
            df_Forecast=self.df_fcst,
            df_Prep=self.df_prep,
            df_inv=current_df_inv,
            column_forecast='SuggestedForecast',
            columns_metadata=self.metadata,
            frequency_='M',
            location=self.location,
            actualdate=date,
            default_coverage_=self.default_coverage,
            join_='left'
        ).suggested_forecast()


    def _calculate_daily_usage(self, suggested_forecast_df, date):
        """
        Calculate average and maximum daily usage rates.
        
        This method computes both average and maximum daily consumption rates
        which are used for inventory planning and safety stock calculations.
        
        Args:
            suggested_forecast_df (pd.DataFrame): DataFrame with forecast data
            date (str): Current calculation date in 'YYYYMMDD' format
            
        Returns:
            tuple: (df_avg, df_max)
                - df_avg: DataFrame with average daily usage
                - df_max: DataFrame with maximum daily usage
        """
        df_avg = DailyUsageFuture(
            location=self.location,
            column_forecast='SuggestedForecast',
            date=date,
            df_fcst=self.df_fcst
        ).daily_usage(suggested_forecast_df, 'AvgDailyUsage').fillna(0)

        df_max = DailyUsageFuture(
            location=self.location,
            column_forecast='SuggestedForecast',
            date=date,
            df_fcst=self.df_fcst
        ).daily_usage(df_avg, 'MaxDailyUsage').fillna(0)
        
        return df_avg, df_max


    def _calculate_security_stock_data(self, df_max, current_df_lead_time, period_index=None, dates=None):
        """
        Calculate security stock related data and prepare for reorder calculations.
        
        This method:
        1. Merges daily usage with lead time data
        2. Determines effective reorder frequency and coverage
        3. Calculates SuggestedForecastPeriod based on coverage ratio
        4. For period 0, uses days to next period instead of reorder frequency
        
        Args:
            df_max (pd.DataFrame): DataFrame with maximum daily usage
            current_df_lead_time (pd.DataFrame): Lead time data for current item
            period_index (int, optional): Current period index (0, 1, 2, ...)
            dates (list, optional): List of dates for this item
            
        Returns:
            pd.DataFrame: DataFrame with merged data and calculated fields:
                - All fields from df_max
                - AvgLeadTime, MaxLeadTime from lead time data
                - SuggestedForecastPeriod: Adjusted forecast for the period
        """
        merge_columns = ['Item', 'Location', 'AvgLeadTime', 'MaxLeadTime'] if self.location else ['Item', 'AvgLeadTime', 'MaxLeadTime']
        df_sstock = pd.merge(df_max, current_df_lead_time[merge_columns], on=self.metadata, how='inner').drop_duplicates()
        
        # Get ReorderFreq and Coverage
        reorder_freq = current_df_lead_time['ReorderFreq'].values[0]
        if pd.isnull(reorder_freq) or reorder_freq == 0:
            reorder_freq = self.default_coverage
            
        coverage = self.default_coverage
        if 'Coverage' in current_df_lead_time.columns:
            coverage_val = current_df_lead_time['Coverage'].values[0]
            if not pd.isnull(coverage_val):
                coverage = coverage_val
            else:
                coverage = reorder_freq + df_sstock['AvgLeadTime'].values[0]
        else:
            coverage = reorder_freq + df_sstock['AvgLeadTime'].values[0]
        
        # Calculate SuggestedForecastPeriod
        if period_index == 0 and dates is not None and len(dates) > 1:
            # For period 0, use days to next period instead of reorder frequency
            # This allows uniform consumption calculation in all future periods
            current_date = pd.to_datetime(dates[0], format='%Y%m%d')
            next_date = pd.to_datetime(dates[1], format='%Y%m%d')
            days_to_next_period = (next_date - current_date).days
            
            # Formula: SuggestedForecast × (days_to_next_period / coverage)
            # This represents the forecasted consumption from period 0 to period 1
            suggested_forecast_period = np.ceil(df_sstock['SuggestedForecast'] * (days_to_next_period / coverage))
        else:
            # For other periods, use the original calculation with reorder frequency
            # Formula: SuggestedForecast × (reorder_freq / coverage)
            suggested_forecast_period = np.ceil(df_sstock['SuggestedForecast'] * (reorder_freq / coverage))
        
        df_sstock['SuggestedForecastPeriod'] = df_sstock.apply(
            lambda row: self._format_value(suggested_forecast_period.iloc[row.name], 'SuggestedForecastPeriod'),
            axis=1
        )
        
        return df_sstock


    def _calculate_security_stock(self, df):
        """
        Calculate security stock using configured method.
        
        Two methods are available:
        1. Statistical method (default):
           SecurityStock = (MaxDailyUsage × MaxLeadTime) - (AvgDailyUsage × AvgLeadTime)
           This represents the difference between worst-case and average scenarios.
           
        2. Reference days method (if security_stock_ref=True):
           SecurityStock = SecurityStockDaysRef × AvgDailyUsage
           Uses a predefined number of days of coverage.
        
        Args:
            df (pd.DataFrame): DataFrame containing required calculation fields
            
        Returns:
            pd.Series: Calculated security stock values
        """
        if self.security_stock_ref:
            security_stock = df['SecurityStockDaysRef'] * df['AvgDailyUsage']
        else:
            security_stock = (df['MaxDailyUsage'] * df['MaxLeadTime']) - (df['AvgDailyUsage'] * df['AvgLeadTime'])
        
        # Apply formatting
        return security_stock.apply(lambda x: self._format_value(x, 'SecurityStock'))


    def _calculate_inventory_days(self, df):
        """
        Calculate inventory days using configured method.
     
        FutureStockoutDays = (FutureInventoryTransitArrival - SecurityStock) / AvgDailyUsage
        
        Args:
            df (pd.DataFrame): DataFrame containing required calculation fields
            
        Returns:
            pd.Series: Calculated future stockout days
        """
        # Calculate future stockout days with safe division
        # Avoid division by zero by checking AvgDailyUsage
        future_stockout_days = np.where(
            df['AvgDailyUsage'] > 0,
            (df['FutureInventoryTransitArrival'] - df['SecurityStock']) / df['AvgDailyUsage'],
            0  # If no daily usage, return 0 days
        )

        # Apply formatting
        return pd.Series(future_stockout_days).apply(lambda x: self._format_value(x, 'FutureStockoutDays'))


    def _sum_transit_arrivals(self, transit_arrivals_str):
        """
        Calculate the total quantity from TransitArrival string.
        
        Args:
            transit_arrivals_str (str): String representation of transit arrivals list
                                       e.g., '[{"quantity": 100.0, "arrival_date": "2024-01-15"}]'
            
        Returns:
            float: Total quantity of all arrivals in the period
        """
        
        if transit_arrivals_str == '[]' or not transit_arrivals_str:
            return 0.0
            
        try:
            arrivals = ast.literal_eval(transit_arrivals_str)
            return sum(arrival.get('quantity', 0) for arrival in arrivals)
        except:
            return 0.0


    def _prepare_transit_schedule(self, key, transit_amount, dates):
        """
        Prepare transit schedule based on df_transit or default logic.
        
        Args:
            key (tuple or str): Item identifier (item) or (item, location)
            transit_amount (float): Total transit amount from df_inv
            dates (list): List of dates for this item
            
        Returns:
            list: List of transit orders with 'quantity' and 'arrival_date'
        """
        if transit_amount <= 0:
            return []
            
        transit_schedule = []
        
        if self.df_transit is None:
            # Default logic: complete transit arrives in period 1
            if len(dates) > 1:
                arrival_date = pd.to_datetime(dates[1], format='%Y%m%d')
                transit_schedule.append({
                    'quantity': transit_amount,
                    'arrival_date': arrival_date
                })
        else:
            # Use provided transit schedule
            if self.location:
                item, location = key
                mask = (self.df_transit['Item'] == item) & (self.df_transit['Location'] == location)
            else:
                mask = self.df_transit['Item'] == key
                
            transit_data = self.df_transit[mask].copy()
            
            if not transit_data.empty:
                # Validate total matches
                total_scheduled = transit_data['Transit'].sum()
                if abs(total_scheduled - transit_amount) > 0.01:  # Allow small floating point differences
                    raise ValueError(f"Transit schedule total ({total_scheduled}) does not match inventory transit ({transit_amount}) for {key}")
                
                # Create transit orders
                for _, row in transit_data.iterrows():
                    arrival_date = pd.to_datetime(row['ArrivalDate'], format='%Y-%m-%d')
                    transit_schedule.append({
                        'quantity': float(row['Transit']),
                        'arrival_date': arrival_date
                    })
            else:
                # If no transit data provided for this item, use default logic
                if len(dates) > 1:
                    arrival_date = pd.to_datetime(dates[1], format='%Y%m%d')
                    transit_schedule.append({
                        'quantity': transit_amount,
                        'arrival_date': arrival_date
                    })
                    
        return transit_schedule


    def _process_current_period(self, current_df_inv, df_sstock, key, date, transit_orders, dates):
        """
        Process inventory for the current period (i=0).
        
        This optimized version uses vectorized operations where possible and
        minimizes redundant calculations.
        
        Args:
            current_df_inv (pd.DataFrame): Current inventory data
            df_sstock (pd.DataFrame): Security stock calculation data
            key (tuple or str): Item identifier (item) or (item, location)
            date (str): Current date in 'YYYYMMDD' format
            transit_orders (dict): Dictionary tracking in-transit orders
            dates (list): List of all dates for this item
            
        Returns:
            pd.DataFrame: Processed inventory data for the current period
        """
        inventory_columns = ['Item', 'Location', 'Inventory', 'Transit', 'PurchaseFactor'] if self.location else ['Item', 'Inventory', 'Transit', 'PurchaseFactor']
        df_inventory = current_df_inv[inventory_columns].copy()
        
        # Vectorized initialization of inventory values with formatting
        df_inventory['FutureInventory'] = df_inventory['Inventory'].apply(
            lambda x: self._format_value(x, 'FutureInventory')
        )
        df_inventory['FutureTransit'] = df_inventory['Transit'].apply(
            lambda x: self._format_value(x, 'FutureTransit')
        )
        df_inventory['FutureInventoryTransit'] = df_inventory.apply(
            lambda row: self._format_value(row['Inventory'] + row['Transit'], 'FutureInventoryTransit'),
            axis=1
        )
        
        # Initialize transit orders for this item
        if key not in transit_orders:
            transit_orders[key] = []
        
        # Handle initial transit
        transit_qty = float(df_inventory['Transit'].iloc[0])
        
        # Prepare transit schedule
        transit_schedule = self._prepare_transit_schedule(key, transit_qty, dates)
        
        # Add scheduled transits to transit_orders
        transit_orders[key].extend(transit_schedule)
        
        # For period 0, TransitArrival should always be empty list
        df_inventory['TransitArrival'] = '[]'
        
        # Select relevant columns
        df_inventory = df_inventory[self.metadata + ['FutureInventoryTransit', 'FutureInventory', 'FutureTransit', 'TransitArrival']]
        
        # Merge with stock data
        df = pd.merge(df_inventory, df_sstock, on=self.metadata, how='inner')
        
        # Vectorized calculations for all rows at once
        df['SuggestedForecastPeriod'] = df_sstock['SuggestedForecastPeriod']
        df['SecurityStock'] = self._calculate_security_stock(df)
        
        # Apply formatting to calculated fields
        df['SuggestedForecast'] = df['SuggestedForecast'].apply(
            lambda x: self._format_value(x, 'SuggestedForecast')
        )
        df['ReorderPoint'] = df.apply(
            lambda row: self._format_value(max(0, row['SuggestedForecast'] + row['SecurityStock']), 'ReorderPoint'),
            axis=1
        )
        df['ReorderQtyBase'] = df.apply(
            lambda row: self._format_value(max(0, row['ReorderPoint'] - row['FutureInventoryTransit']), 'ReorderQtyBase'),
            axis=1
        )
        
        # First period has no reorder - vectorized assignment
        df['ReorderQty'] = 0
        df['ReorderQtyDays'] = 0
        df['ArrivalDate'] = ''  # No order in period 0
        
        # Note: FutureInventoryTransitArrival and FutureStockoutDays are calculated later
        # in _process_item_optimized after all periods are processed
        
        return df


    def _process_transit_orders(self, transit_orders, key, current_date, previous_date):
        """
        Process transit orders and calculate arrivals for the current period.
        
        This optimized method uses vectorization for better performance with large
        numbers of transit orders. It manages the lifecycle of transit orders:
        1. Identifies orders arriving in the current period
        2. Moves arrived quantities from transit to stock
        3. Updates remaining transit orders
        4. Maintains arrival history for reporting
        
        Args:
            transit_orders (dict): Dictionary of active transit orders by item/location
            key (tuple or str): Item identifier (item) or (item, location)
            current_date (pd.Timestamp): Current period date
            previous_date (pd.Timestamp): Previous period date
            
        Returns:
            tuple: (stock_from_arrivals, new_transit, transit_arrivals)
                - stock_from_arrivals: Total quantity arriving in this period
                - new_transit: Total quantity still in transit
                - transit_arrivals: List of arrival records for this period
        """
        # Get orders for this key, return early if none
        orders = transit_orders.get(key, [])
        if not orders:
            return 0, 0, []
        
        # For small numbers of orders, use loops implementation
        # as it has less overhead
        if len(orders) < 10:
            new_transit = 0
            remaining_orders = []
            transit_arrivals = []
            stock_from_arrivals = 0
            
            for order in orders:
                if order['arrival_date'] > previous_date and order['arrival_date'] <= current_date:
                    # Order arrives in this period
                    stock_from_arrivals += order['quantity']
                    transit_arrivals.append({
                        'quantity': float(order['quantity']),
                        'arrival_date': order['arrival_date'].strftime('%Y-%m-%d')
                    })
                else:
                    # Order still in transit
                    new_transit += order['quantity']
                    remaining_orders.append(order)
            
            transit_orders[key] = remaining_orders
            return stock_from_arrivals, new_transit, transit_arrivals
        
        # For larger numbers of orders, use vectorized approach
        # Extract data into numpy arrays for faster processing
        quantities = np.array([order['quantity'] for order in orders], dtype=np.float64)
        arrival_dates = np.array([order['arrival_date'] for order in orders])
        
        # Vectorized date comparison
        mask_arrived = (arrival_dates > previous_date) & (arrival_dates <= current_date)
        
        # Calculate totals using numpy operations
        stock_from_arrivals = float(quantities[mask_arrived].sum()) if mask_arrived.any() else 0
        new_transit = float(quantities[~mask_arrived].sum()) if (~mask_arrived).any() else 0
        
        # Create transit arrivals list
        transit_arrivals = []
        if mask_arrived.any():
            arrived_indices = np.where(mask_arrived)[0]
            transit_arrivals = [
                {
                    'quantity': float(quantities[i]),
                    'arrival_date': arrival_dates[i].strftime('%Y-%m-%d')
                }
                for i in arrived_indices
            ]
        
        # Update transit orders with remaining orders
        if (~mask_arrived).any():
            remaining_indices = np.where(~mask_arrived)[0]
            transit_orders[key] = [orders[i] for i in remaining_indices]
        else:
            transit_orders[key] = []
        
        return stock_from_arrivals, new_transit, transit_arrivals


    def _process_future_period(self, current_df_inv, df_sstock, df_previous, key, date, dates, i, transit_orders):
        """
        Process inventory for future periods (i>0).
        
        This method:
        1. Calculates consumption using SuggestedForecastPeriod from previous period
        2. Updates stock levels considering consumption and arrivals
        3. Determines if reorder is needed
        4. Calculates reorder quantity if needed
        5. Adds new orders to transit tracking
                
        Args:
            current_df_inv (pd.DataFrame): Current inventory data
            df_sstock (pd.DataFrame): Security stock calculation data
            df_previous (pd.DataFrame): Previous period's results
            key (tuple or str): Item identifier (item) or (item, location)
            date (str): Current date in 'YYYYMMDD' format
            dates (list): List of all dates for this item
            i (int): Current period index
            transit_orders (dict): Dictionary tracking in-transit orders
            
        Returns:
            pd.DataFrame: Processed inventory data for the period including:
                - Updated inventory levels
                - Reorder recommendations
                - Transit arrival information
        """
        inventory_columns = ['Item', 'Location', 'PurchaseFactor'] if self.location else ['Item', 'PurchaseFactor']
        df_inventory = current_df_inv[inventory_columns].copy()
        df = pd.merge(df_inventory, df_sstock, on=inventory_columns, how='inner')
        df['SuggestedForecastPeriod'] = df_sstock['SuggestedForecastPeriod']
        
        # Calculate consumption using SuggestedForecastPeriod from previous period
        consumption = df_previous['SuggestedForecastPeriod'].values[0]
        
        previous_stock = df_previous['FutureInventory'].values[0] - consumption
        
        # Process transit orders
        current_date = pd.to_datetime(date, format='%Y%m%d')
        previous_date = pd.to_datetime(dates[i-1], format='%Y%m%d')
        
        stock_from_arrivals, new_transit, transit_arrivals = self._process_transit_orders(
            transit_orders, key, current_date, previous_date
        )
        
        # Update inventory values with formatting
        future_stock = max(0, previous_stock + stock_from_arrivals)
        df['FutureInventory'] = self._format_value(future_stock, 'FutureInventory')
        df['FutureTransit'] = self._format_value(new_transit, 'FutureTransit')
        df['FutureInventoryTransit'] = self._format_value(
            future_stock + new_transit,
            'FutureInventoryTransit'
        )
        df['TransitArrival'] = str(transit_arrivals) if transit_arrivals else '[]'
        
        # Calculate security stock and reorder values
        df['SecurityStock'] = self._calculate_security_stock(df)
        
        # Apply formatting to calculated fields
        df['SuggestedForecast'] = df['SuggestedForecast'].apply(
            lambda x: self._format_value(x, 'SuggestedForecast')
        )
        df['ReorderPoint'] = df.apply(
            lambda row: self._format_value(max(0, row['SuggestedForecast'] + row['SecurityStock']), 'ReorderPoint'),
            axis=1
        )
        df['ReorderQtyBase'] = df.apply(
            lambda row: self._format_value(max(0, row['ReorderPoint'] - row['FutureInventoryTransit']), 'ReorderQtyBase'),
            axis=1
        )
        
        # Calculate ReorderQty only if ReorderQtyBase > 0
        reorder_qty = np.where(
            df['ReorderQtyBase'] > 0,
            ((df['ReorderQtyBase'] / df['PurchaseFactor']).apply(np.ceil)) * df['PurchaseFactor'],
            0
        )
        df['ReorderQty'] = df.apply(
            lambda row: self._format_value(reorder_qty[row.name], 'ReorderQty'),
            axis=1
        )
        
        # Calculate ReorderQtyDays, avoiding division by zero
        reorder_qty_days = np.where(
            (df['ReorderQty'] > 0) & (df['AvgDailyUsage'] > 0),
            df['ReorderQty'] / df['AvgDailyUsage'],
            0
        )
        df['ReorderQtyDays'] = df.apply(
            lambda row: self._format_value(reorder_qty_days[row.name], 'ReorderQtyDays'),
            axis=1
        )
        
        # Add new order to transit if needed
        if df['ReorderQty'].values[0] > 0:
            avg_lead_time = df['AvgLeadTime'].values[0]
            arrival_date = current_date + timedelta(days=int(avg_lead_time))
            # Store the raw value for transit calculations
            transit_orders[key].append({
                'quantity': float(df['ReorderQty'].values[0]),
                'arrival_date': arrival_date
            })
            # Store arrival date for this period's order
            df['ArrivalDate'] = arrival_date.strftime('%Y-%m-%d')
        else:
            # No order in this period
            df['ArrivalDate'] = ''
        
        
        # Note: FutureInventoryTransitArrival and FutureStockoutDays are calculated later
        # in _process_item_optimized after all periods are processed
        
        return df


    def _prepare_final_dataframe(self, data_frame):
        """
        Prepare the final output dataframe with proper formatting and column selection.
        
        This method:
        1. Merges with lead time data to add reorder parameters
        2. Formats dates to YYYY-MM-DD format
        3. Renames columns for clarity
        4. Rounds numeric values to 2 decimal places
        5. Selects and orders final columns
        
        Args:
            data_frame (pd.DataFrame): Raw calculation results
            
        Returns:
            pd.DataFrame: Formatted output with columns:
                - PurchaseDate, Item, ItemDescription, (Location)
                - Forecast metrics: SuggestedForecast, SuggestedForecastPeriod
                - Inventory levels: FutureInventoryTransit (total), FutureInventory (stock), FutureTransit (transit)
                - FutureInventoryTransitArrival: FutureInventory + arrivals in the period
                - FutureStockoutDays: Days of inventory coverage
                - Transit information: TransitArrival
                - Reorder metrics: ReorderQtyBase, ReorderQty, ReorderQtyDays
                - Order information: ArrivalDate (arrival date of current period's order)
                - Planning parameters: PurchaseFactor, ReorderPoint, SecurityStock
                - Usage rates: AvgDailyUsage, MaxDailyUsage
                - Lead times: AvgLeadTime, MaxLeadTime
                - Coverage parameters: ReorderFreq, Coverage
        """
        leadtimes_columns = ['Item', 'Location', 'ReorderFreq', 'Coverage'] if self.location else ['Item', 'ReorderFreq', 'Coverage']
        leadtimes = self.df_lead_time[leadtimes_columns]
        df_final = pd.merge(data_frame, leadtimes, on=self.metadata, how='left').fillna(0)
        
        # Format date and rename to PurchaseDate
        df_final['PurchaseDate'] = pd.to_datetime(df_final['Date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        df_final = df_final.drop('Date', axis=1)
        
        # Ensure ArrivalDate is present (in case some records don't have it)
        if 'ArrivalDate' not in df_final.columns:
            df_final['ArrivalDate'] = ''
        
        # Apply formatting to fields that are ALWAYS integers
        always_integer_fields = ['PurchaseFactor', 'AvgLeadTime', 'MaxLeadTime', 'ReorderQtyDays', 'ReorderFreq', 'Coverage']
        for field in always_integer_fields:
            if field in df_final.columns:
                df_final[field] = df_final[field].apply(lambda x: self._format_value(x, field))
        
        # Apply formatting to fields that are ALWAYS decimals
        always_decimal_fields = ['AvgDailyUsage', 'MaxDailyUsage']
        for field in always_decimal_fields:
            if field in df_final.columns:
                df_final[field] = df_final[field].apply(lambda x: self._format_value(x, field))
        
        # Select final columns
        if self.location:
            final_cols = [
                'PurchaseDate', 'Item', 'ItemDescription', 'Location', 'SuggestedForecast',
                'SuggestedForecastPeriod', 'FutureInventoryTransit', 'FutureInventory',
                'FutureTransit', 'FutureInventoryTransitArrival', 'FutureStockoutDays', 'TransitArrival',
                'ReorderQtyBase', 'ReorderQty', 'ReorderQtyDays', 'ArrivalDate', 'PurchaseFactor',
                'ReorderPoint', 'SecurityStock', 'AvgDailyUsage', 'MaxDailyUsage', 'AvgLeadTime',
                'MaxLeadTime', 'ReorderFreq', 'Coverage'
            ]
        else:
            final_cols = [
                'PurchaseDate', 'Item', 'ItemDescription', 'SuggestedForecast',
                'SuggestedForecastPeriod', 'FutureInventoryTransit', 'FutureInventory',
                'FutureTransit', 'FutureInventoryTransitArrival', 'FutureStockoutDays', 'TransitArrival',
                'ReorderQtyBase', 'ReorderQty', 'ReorderQtyDays', 'ArrivalDate', 'PurchaseFactor',
                'ReorderPoint', 'SecurityStock', 'AvgDailyUsage', 'MaxDailyUsage', 'AvgLeadTime',
                'MaxLeadTime', 'ReorderFreq', 'Coverage'
            ]
        
        return df_final[final_cols]


    def reorder(self):
        """
        Main method to calculate future reorder recommendations.
        
        This optimized version uses batch processing and vectorization to improve
        performance, especially for large datasets. The method:
        1. Generates future dates based on reorder frequencies
        2. Groups items for batch processing when possible
        3. Pre-allocates data structures to minimize memory operations
        4. Uses vectorized calculations where applicable
        5. Formats and returns consolidated results
        
        Returns:
            pd.DataFrame: Complete reorder recommendations for all items/locations
                         and time periods. See _prepare_final_dataframe() for
                         detailed column descriptions.
                         
        Example usage:
            >>> reorder_system = FutureReorder(
            ...     df_inv=inventory_df,
            ...     df_lead_time=lead_time_df,
            ...     df_prep=prep_df,
            ...     df_fcst=forecast_df,
            ...     periods=6,
            ...     start_date='2024-01-01'
            ... )
            >>> results = reorder_system.reorder()
            >>> results.head()
            # Returns DataFrame with reorder recommendations
        """
        
        item_dates = self.future_date()
        
        # Pre-allocate list for results instead of concatenating DataFrames
        all_results = []
        
        # Group items by number of periods for potential batch processing
        items_by_period_count = {}
        for key, dates in item_dates.items():
            period_count = len(dates)
            if period_count not in items_by_period_count:
                items_by_period_count[period_count] = []
            items_by_period_count[period_count].append((key, dates))
        
        # Process each group
        for period_count, items_group in items_by_period_count.items():
            # For each item in the group
            for key, dates in items_group:
                if self.location:
                    item, location = key
                else:
                    item = key
                    location = None
                
                # Get current dataframes
                current_df_lead_time, current_df_inv = self._get_current_dataframes(item, location)
                
                if current_df_lead_time.empty or current_df_inv.empty:
                    continue
                
                # Process this item using optimized approach
                item_results = self._process_item_optimized(
                    key, item, location, dates, current_df_lead_time, current_df_inv
                )
                
                if item_results is not None and not item_results.empty:
                    all_results.append(item_results)
        
        # Combine all results efficiently
        if all_results:
            data_frame = pd.concat(all_results, ignore_index=True)
        else:
            columns = ['Date', 'Item'] + (['Location'] if self.location else [])
            data_frame = pd.DataFrame(columns=columns)
        
        # Prepare and return final dataframe
        return self._prepare_final_dataframe(data_frame)
    
    
    def _process_item_optimized(self, key, item, location, dates, current_df_lead_time, current_df_inv):
        """
        Process a single item through all periods using optimized approach.
        
        This method pre-allocates arrays and uses vectorized operations where possible
        to improve performance.
        
        Args:
            key: Item key (item or (item, location))
            item: Item identifier
            location: Location identifier (if applicable)
            dates: List of dates to process
            current_df_lead_time: Lead time data for this item
            current_df_inv: Inventory data for this item
            
        Returns:
            pd.DataFrame: Results for all periods of this item
        """
        
        # Pre-allocate dictionaries for intermediate results
        suggested_forecasts = {}
        df_avgs = {}
        df_maxs = {}
        df_sstocks = {}
        period_results = {}
        
        # Initialize transit orders for this item
        transit_orders = {key: []}
        
        # Track last suggested forecast value for complete_suggested feature
        last_suggested_value = None
                
        # Process each period
        for i, date in enumerate(dates):
            # Calculate suggested forecast (cached if possible)
            suggested_forecasts[i] = self._calculate_suggested_forecast(
                current_df_lead_time, current_df_inv, date, last_suggested_value
            )
            
            # Update last_suggested_value for next iteration
            if 'SuggestedForecast' in suggested_forecasts[i].columns:
                last_suggested_value = suggested_forecasts[i]['SuggestedForecast'].iloc[0]
            
            # Calculate daily usage
            df_avgs[i], df_maxs[i] = self._calculate_daily_usage(
                suggested_forecasts[i], date
            )
            
            # Calculate security stock data
            df_sstocks[i] = self._calculate_security_stock_data(
                df_maxs[i], current_df_lead_time, period_index=i, dates=dates
            )
            
            # Process period based on whether it's current or future
            if i == 0:
                period_results[i] = self._process_current_period(
                    current_df_inv, df_sstocks[i], key, date, transit_orders, dates
                )
            else:
                period_results[i] = self._process_future_period(
                    current_df_inv, df_sstocks[i], period_results[i-1],
                    key, date, dates, i, transit_orders
                )
            
            # Add metadata columns efficiently
            period_results[i]['Date'] = date
            period_results[i]['Item'] = item
            if self.location:
                period_results[i]['Location'] = location
        
        # After processing all periods, update FutureInventoryTransitArrival with next period's TransitArrival
        for i in range(len(dates)):
            if i < len(dates) - 1:  # If there's a next period
                # Get next period's TransitArrival
                next_transit_arrival = period_results[i + 1]['TransitArrival'].iloc[0]
                transit_arrival_sum = self._sum_transit_arrivals(next_transit_arrival)
            else:  # Last period - no next period
                transit_arrival_sum = 0
            
            # Update FutureInventoryTransitArrival
            period_results[i]['FutureInventoryTransitArrival'] = self._format_value(
                period_results[i]['FutureInventory'].iloc[0] + transit_arrival_sum,
                'FutureInventoryTransitArrival'
            )
            
            # Recalculate FutureStockoutDays with the updated FutureInventoryTransitArrival
            period_results[i]['FutureStockoutDays'] = self._calculate_inventory_days(period_results[i])
        
        # Combine all periods for this item
        if period_results:
            # Stack all period results at once
            item_df = pd.concat(period_results.values(), ignore_index=True)
            
            # Reorder columns for consistency
            cols = ['Date', 'Item']
            if self.location:
                cols.append('Location')
            other_cols = [col for col in item_df.columns if col not in cols]
            item_df = item_df[cols + other_cols]
            
            return item_df
        
        return None