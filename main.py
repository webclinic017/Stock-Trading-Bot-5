import os

from concurrent.futures import ThreadPoolExecutor
from backtest.report import Report
from config.config import FOLDER_STRUCTURE
from typing import cast 
from strategies.moving_average import MovingAverageCrossover 
from utils.utils import read_stock_data, generate_reports, save_dataframe_as_csv

# Apply strategy to stock
def apply_strategy(stock_data, strategy_class, strategy_params):
    strategy = strategy_class(stock_data, *strategy_params)
    signals = strategy.generate_signals(stock_data)
    return signals

def main():
    stocks_folder = cast(str, FOLDER_STRUCTURE.STOCKS_MAIN_PATH )

    stock_files = [os.path.join(stocks_folder, f) for f in os.listdir(stocks_folder) if f.endswith('.csv')]

    short_window = 'EMA_9'
    long_window = 'EMA_20'
    
    strategy_params = (short_window, long_window)

    with ThreadPoolExecutor() as executor:
        # Read stock data in parallel
        stock_data_list = list(executor.map(read_stock_data, stock_files))

        # Apply strategy to each stock in parallel
        signals_list = list(executor.map(apply_strategy, stock_data_list, [MovingAverageCrossover]*len(stock_data_list), [strategy_params]*len(stock_data_list)))

        # Save DataFrames as CSV files in parallel
        output_folder = 'output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        output_file_names = [os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file))[0]}_signals.csv') for file in stock_files]
        
        list(executor.map(save_dataframe_as_csv, signals_list, output_file_names))

if __name__ == '__main__':
    main()