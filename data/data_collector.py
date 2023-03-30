import os 
import pathlib
import requests
import pandas as pd

from tqdm import tqdm
from typing import cast 
from ..config.config import POLYGONE_SERVICE, FOLDER_STRUCTURE


def is_valid_time(row):
    time_range = ("09:30", "15:55")
    time = ":".join(str(row['Date']).split(" ")[1].split(":")[:2])
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

def fetch_data(ticker = 'ATHX', _range = '5', time_unit= 'minute', _from = '2022-01-01', _to = '2022-02-04'):
    year, month, _ = _from.split("-")
    # Make sure nothing wrong here, I feel stocks folder is missed
    folder_path = f'{FOLDER_STRUCTURE.MAIN_FOLDER}/{_range}{time_unit}/{ticker}'
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True) 

    download_path = cast( str , POLYGONE_SERVICE.TICKER_LINK)
    download_path += f'{ticker}/range/{_range}/{time_unit}/{_from}/{_to}?adjusted=true&limit={POLYGONE_SERVICE.LIMIT}&apiKey={POLYGONE_SERVICE.API_KEY}'     

    try:
        response = requests.get(download_path, timeout=15)
        response = response.json()
        if 'results' in response:
            data = []
            for row in response['results']:
                timestamp, volume,  _open, _close, _height, _low = row['t'], row['v'], row['o'], row['c'], row['h'], row['l']    
                returned_obj = {
                    'Date':  pd.Timestamp(timestamp, unit='ms', tz='UTC'), 
                    'Open': _open,
                    'Close': _close,
                    'high': _height, 
                    'Low': _low, 
                    'Volume': volume, 
                }
                data.append(returned_obj)
            else:
                df = (  pd.DataFrame(data)
                        .assign(
                            Date=lambda x: x.Date.dt.tz_convert("US/Eastern"),
                            Close=lambda x: x["Close"].map("{:.4f}".format),
                            isValidRecord=lambda x: x.apply(is_valid_time, axis=1)
                        )
                        .query("isValidRecord == True")
                        .drop("isValidRecord", axis=1)
                )
                if not df.empty:
                    csv_path = f"{FOLDER_STRUCTURE.MAIN_FOLDER}/{_range}{time_unit}/{ticker}/{ticker}-{year}-{month}.csv"
                    df.to_csv(csv_path, index=False)
        else:
            with open(f"logs-{_range}.txt", 'a') as file:
                file.writelines(f'Ticker: {ticker} month: ' +  month + ' year: ' + year + '\n')
    except:
        print("Something wrong happened with ticker: ", ticker)