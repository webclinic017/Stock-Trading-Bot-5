import os
import shutil
import requests 
import pandas as pd 

from typing import Dict
from pytz import timezone
from datetime import datetime
from config.config import FOLDER_STRUCTURE, POLYGONE_SERVICE


def read_stock_data(file, to_numpy=True):
    read_file = pd.read_csv(file, index_col=0, parse_dates=True)
    return read_file.to_numpy() if to_numpy else read_file
    
def save_dataframe_as_csv(df, file_name):
    df.to_csv(file_name, index=False)
    
def get_column_indices(dataframe, parameters):
    column_indices = {}
    for param in parameters:
        if param in dataframe.columns:
            column_indices[param] = dataframe.columns.get_loc(param)
        else:
            raise ValueError(f"Parameter '{param}' not found in DataFrame columns.")
    return column_indices.values()

# Generate reports
def generate_reports(metrics, report_name):
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv(f'reports/{report_name}.csv', index=False)
    
def extract_symbol_from_filename(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def get_market_status() -> Dict[ str, str ]: 
    try:
        url = f'{POLYGONE_SERVICE.MARKET_STATUS}/now?apiKey={POLYGONE_SERVICE.API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        received_server_time = data['serverTime']
        server_time =  ":".join( received_server_time.split("T")[1].split("-")[0] )

        return {
            "status": data['exchanges']['nasdaq'], 
            "server_time": server_time
        }
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {}

def get_stock_path(stock, time_frame):
    # To Be Modified 
    return os.path.join(os.getcwd(), f'scanners/{time_frame}mins/stocks/{stock}')

def remove_files(directory_path):
    # remove all files in the given directory
    for i in os.listdir(directory_path):
        os.remove(i)

def extract_hour_from_date(date):
    # input example: 07:25:00-04:00
    # output example: 08:35:00
    return date.split(" ")[1].split("-")[0]

def get_current_time(is_hour=1):
    tz = timezone('EST')
    dt = datetime.now(tz)
    if is_hour == 2:
        return dt.strftime("%Y-%m-%d %H:%M")
    return dt.strftime('%H:%M') if is_hour else dt.strftime("%Y-%m-%d")

def error_report(stock):
    with open(f'errors.txt', 'a') as file:
        file.writelines(stock + '\n')

def is_stock_missing_data(date, timeframe ):
    try:
        date = date.tolist()
        # example of one row : 2022-05-11 09:05:00-04:00
        first_time = first_index = None
        for index, row in enumerate(date):
            time = extract_hour_from_date(row)
            # check if timerange is 5 mins or 1 min
            if time in ['09:30:00', '09:35:00']:
                first_time = row
                first_index = index
                break

        # print("First time: ", first_time)
        # print("First Index: ", first_index)

        if None in [first_index, first_time]:
            # print("I am being returned here")
            return 0  # something wrong here
        last_time = datetime.fromisoformat(first_time.replace("-04:00", ""))
        # print("last_time: ", last_time)
        current_time = datetime.fromisoformat(
            get_current_time(2))  # date + hour and mins
        # print("current_time: ", current_time)
        minutes_diff = (
            (current_time - last_time).total_seconds() / 60.0)
        # print("minutes_diff: ", minutes_diff)

        number_of_required_rows = minutes_diff // timeframe
        # print("number_of_required_rows: ", number_of_required_rows)

        # check the length of the dates starting from the first candle after the market opens
        numbers_of_logged_dates = len(date[first_index:])
        # print("numbers_of_logged_dates: ", numbers_of_logged_dates)
        return numbers_of_logged_dates == number_of_required_rows
    except:
        return False
    