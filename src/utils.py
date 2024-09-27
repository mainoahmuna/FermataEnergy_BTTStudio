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

"""
The Utils class holds common functions that can be used in:
- Initalizing Google Drive
- Encoding
- Preprocessing
"""
class Utils():
    # assumes the path is a shortcut in your "MyDrive"
    def __init__(self, using_colab : True):
        if using_colab == False:
            print("Currently does not support local files.")
        else:
            try:
                drive.mount('/content/drive')
            except Exception as e:
                print(f"Failed to mount drive: {e}")

    # metadata cleaning 
    def remove_lost_l_and_w_from_metadata(self):
        md_uncleaned = pd.read_csv(PATH_EXTERNAL + "/metadata.csv")
        BUILDING_DATA_PATH = PATH_EXTERNAL + "/building_data"
        existing_ids = set(map(int, os.listdir(BUILDING_DATA_PATH)))
        md_cleaned = md_uncleaned[md_uncleaned['bldg_id'].isin(existing_ids)]
        try:
            md_cleaned.to_csv(PATH_INTERNAL + "metadata_removed_lost_l_and_w.csv")
            print("Successfully saved cleaned metadata to Team-Fermata-Energy/processed_data")
        except Exception as e:
            print(f"Failed to save metadata: {e}")
    
    def load_cleaned_metadata(self):
      try:
        return pd.read_csv(PATH_INTERNAL + "/metadata_removed_lost_l_and_w.csv")
      except Exception as e:
        print(f"Failed to load metadata: {e}")

    # Combines the load and weather files that have the same building_id
    def match_l_and_w_from_building_id(self, building_id):
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
          # print(weather_df.head())

          # # the first few rows and the columns of each DataFrame
          # print(f"Load DataFrame for building {building_id}:")
          # print(load_df.head())
          # print("Load DataFrame columns:", load_df.columns.tolist())

          # print(f"Weather DataFrame for building {building_id}:")
          # print(weather_df.head())
          # print("Weather DataFrame columns:", weather_df.columns.tolist())

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

          # print(f"---------------------------------------------------")
          # print(f"Merged DataFrame for building {building_id}:")

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
        try:
            df[column_name] = pd.to_datetime(df[column_name])
            df.set_index(column_name, inplace=True)
            return df
        except Exception as e:
            print

# Weather interpolation from 1 hour to 15 minute intervals
    def w_interpolation_and_heat_index(self, weather):
        weather = self.convert_column_to_datetime(weather, 'date_time')
        weather = weather.resample('15T').asfreq().interpolate(method='linear').reset_index()

        weather['heat_index'] = mpcalc.heat_index(
            weather['Dry Bulb Temperature [°C]'].values * units.degC,
            weather['Relative Humidity [%]'].values * units.percent
        ).to('degF')
        
        return weather.rename(columns={"date_time":"timestamp"})

# Common Timeseries Encoding Functions
    
    # encodes 
    def load_to_fourier():
        print("Load to Fourier happens here")
    