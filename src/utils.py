# Global Variables
# each of these assumes you have shortcuts to your external and team drive
# in your "MyDrive"
PATH_EXTERNAL = "/content/drive/MyDrive/[EXTERNAL] breakthrough_tech_ai_f24/data"
PATH_INTERNAL = "/content/drive/MyDrive/Team-Fermata-Energy/processed_data"
BUILDING_PATH = PATH_EXTERNAL + "/building_data"

from google.colab import drive

import os
import pandas as pd
import numpy as np

import metpy.calc as mpcalc # For calculating heat index.
from metpy.units import units

import holidays # For US holidays

"""
The Utils class holds common functions that can be used in:
- Initalizing Google Drive
- Encoding
- Preprocessing
"""
class Utils():
    # assumes the path is a shortcut in your "MyDrive"
    def __init__(self, using_colab : True):
        """
        Initialize the Utils class.

        Parameters
        ----------
        using_colab : bool
            If true, attempt to mount Google Drive in Google Colab environment.
            If false, currently does not support local files.

        Returns
        -------
        None
        """
        if using_colab == False:
            print("Currently does not support local files.")
        else:
            try:
                drive.mount('/content/drive')
            except Exception as e:
                print(f"Failed to mount drive: {e}")


    # metadata cleaning 
    def remove_lost_l_and_w_from_metadata(self):
        """
        Remove metadata entries for buildings that don't have associated data in the "building_data" folder.

        The output file is saved in the "processed_data" folder within the Google Drive folder, and is named
        "metadata_removed_lost_l_and_w.csv".

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        md_uncleaned = pd.read_csv(PATH_EXTERNAL + "/metadata.csv")
        BUILDING_DATA_PATH = PATH_EXTERNAL + "/building_data"
        existing_ids = set(map(int, os.listdir(BUILDING_DATA_PATH)))
        md_cleaned = md_uncleaned[md_uncleaned['bldg_id'].isin(existing_ids)]
        try:
            md_cleaned.to_csv(PATH_INTERNAL + "/metadata_removed_lost_l_and_w.csv")
            print("Successfully saved cleaned metadata to Team-Fermata-Energy/processed_data")
        except Exception as e:
            print(f"Failed to save metadata: {e}")
    
    def load_cleaned_metadata(self):
        """
        Loads the cleaned metadata from the "processed_data" folder within the Google Drive folder.
        
        The cleaned metadata is the result of removing metadata entries for buildings that don't have associated data in the "building_data" folder.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        pd.DataFrame
        """
        try:
            return pd.read_csv(PATH_INTERNAL + "/metadata_removed_lost_l_and_w.csv")
        except Exception as e:
            print(f"Failed to load metadata: {e}")

    # CURRENTLY DOESNT WORK AS EXPECTED
    def max_min_load_temp(self, df):
        """
        Adds a max load, max temp, min temp to the combined weather/load df.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        pd.DataFrame
        """
        df['max_load_hourly'] = df.groupby(['hour', 'day', 'month', 'year'])['out.electricity.total.energy_consumption'].transform('max')
        df['max_temp_hourly'] = df.groupby(['hour', 'day', 'month', 'year'])['Dry Bulb Temperature [°C]'].transform('max')
        df['min_temp_hourly'] = df.groupby(['hour', 'day', 'month', 'year'])['Dry Bulb Temperature [°C]'].transform('min')
        return df

    # Combines the load and weather files that have the same building_id
    def match_l_and_w_from_building_id(self, building_id):
      """
        Combines the load and weather files that have the same building_id.

        Parameters
        ----------
        building_id : int
            The building_id to match load and weather data for.

        Returns
        -------
        pd.DataFrame or None
            The merged DataFrame with load and weather data for the given building_id, or None if there is an error.
      """
      # file paths for load.csv and weather.csv
      load_file = os.path.join(BUILDING_PATH, str(building_id), 'load.csv')
      weather_file = os.path.join(BUILDING_PATH,str(building_id), 'weather.csv')

      try:
          # read the load and weather CSV files
          load_df = pd.read_csv(load_file)
          weather_df = pd.read_csv(weather_file)

          # update load so its encoded
          load_df = self.convert_column_to_datetime(load_df, 'timestamp').reset_index()
          # update weather to have interpolation and heat index
          weather_df = self.w_interpolation_and_heat_index(weather_df)

          # check if 'timestamp' is in the load DataFrame and rename 'date_time' in the weather DataFrame
          if 'timestamp' not in load_df.columns:
              raise ValueError("The 'timestamp' column is missing from the load DataFrame.")

          if 'date_time' in weather_df.columns:
              weather_df.rename(columns={'date_time': 'timestamp'}, inplace=True)

          # relevant columns
          load_df = load_df[['timestamp', 'out.electricity.total.energy_consumption']]
          weather_df = weather_df[['timestamp', 'Dry Bulb Temperature [°C]', 'Relative Humidity [%]', 'heat_index']]

          # merge df on the 'timestamp' column
          merged_df = pd.merge(load_df, weather_df, on='timestamp', how='inner')

          final_df = merged_df[['timestamp',
                                'out.electricity.total.energy_consumption',
                                'Dry Bulb Temperature [°C]',
                                'Relative Humidity [%]',
                                'heat_index']]
          # encode the datetime
          final_df = self.extract_values_from_datetime(final_df, 'timestamp')
          # find max load and max/min temperature per hour
          final_df = self.max_min_load_temp(final_df)
          final_df.drop(columns=['timestamp', 'day', 'year'], inplace=True)
          return final_df

      except FileNotFoundError:
          print(f"Files for building {building_id} not found.")
          return None
      except ValueError as ve:
          print(f"ValueError: {ve}")
          return None
    
    # Using a list of building ids, returns the merged load and weather in
    # a list
    def collect_w_and_l_matches(self, building_ids):
        """
        Using a list of building ids, returns the merged load and weather in
        a dictionary of {building_id: merged_df}.

        Parameters
        ----------
        building_ids : list
            A list of building ids.

        Returns
        -------
        dict
            A dictionary of building ids to their merged load and weather DataFrames.
        """
        matches = {}
        for building_id in building_ids:
            try:
                merged_match = self.match_l_and_w_from_building_id(building_id)
                if merged_match is not None:
                    matches[building_id] = merged_match
            except Exception as e:
                print(f"Error processing building_id {building_id}: {e}")
        return matches
# Common Categorical Encoding Functions

# Convert column to datetime 
    def convert_column_to_datetime(self, df, column_name):
        """
        Converts the given column to datetime and sets it as the index of the dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to modify.
        column_name : str
            The name of the column to convert.

        Returns
        -------
        pd.DataFrame
            The modified dataframe.
        """
        try:
            df[column_name] = pd.to_datetime(df[column_name])
            df.set_index(column_name, inplace=True)
            return df
        except Exception as e:
            print(f"Error converting column to datetime: {e}")

    # Extract Values from Datetime
    def extract_values_from_datetime(self, df, column_name):
        try:
            if not np.issubdtype(df[column_name].dtype, np.datetime64):
                df[column_name] = pd.to_datetime(df[column_name])

            # Extract time-based features from the timestamp
            df['hour'] = df[column_name].dt.hour
            df['day'] = df[column_name].dt.day # this is removed after the hourly rate is calculated
            df['month'] = df[column_name].dt.month
            df['year'] = df[column_name].dt.year

            # Weekday/Weekend binary indicator (1 for weekday, 0 for weekend)
            df['is_weekday'] = df[column_name].dt.dayofweek < 5

            # US Holidays binary indicator
            us_holidays = holidays.US()  # Get a list of US holidays
            df['is_holiday'] = df[column_name].dt.date.isin(us_holidays)

        except Exception as e:
            print(f"Error extracting values from datetime: {e}")

        return df

# Weather interpolation from 1 hour to 15 minute intervals
    def w_interpolation_and_heat_index(self, weather):
        """
        Interpolates the given weather data to 15-minute intervals and adds a
        calculated column for heat index.

        Parameters
        ----------
        weather : pd.DataFrame
            The DataFrame to interpolate and modify. Must have columns 'date_time',
            'Dry Bulb Temperature [°C]', and 'Relative Humidity [%]'.

        Returns
        -------
        pd.DataFrame
            The modified DataFrame with the interpolated values and a new 'heat_index'
            column in degrees Fahrenheit.
        """
        weather = self.convert_column_to_datetime(weather, 'date_time')
        weather = weather.resample('15min').asfreq().interpolate(method='linear').reset_index()

        weather['heat_index'] = mpcalc.heat_index(
            weather['Dry Bulb Temperature [°C]'].values * units.degC,
            weather['Relative Humidity [%]'].values * units.percent
        )
        
        return weather.rename(columns={"date_time":"timestamp"})

# Common Timeseries Encoding Functions
    
    # encodes 
    def load_to_fourier():        
        print("Load to Fourier happens here")
    

"""
Benchmark holds different benchmarking functions
"""
class Benchmark():
    def __init__(self):
        pass
    
    # Implement persistence forcast
    
    # Implement rolling average
    
    # implement simple linear regression
    