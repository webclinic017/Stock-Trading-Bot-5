import os
import pandas as pd 

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from config.config import FOLDER_STRUCTURE
from strategies.moving_average import MovingAverageCrossover 
from utils.utils import read_stock_data, extract_symbol_from_filename, save_dataframe_as_csv, get_column_indices

# Apply strategy to stock
def apply_strategy(stock_data, strategy_class, strategy_params, symbol):
    strategy = strategy_class(stock_data, *strategy_params, symbol)
    signals = strategy.generate_signals()
    return signals

def main():
    stocks_folder = os.path.join(FOLDER_STRUCTURE.STOCKS_MAIN_PATH.value, '5mins_ta') 
    stock_files = [os.path.join(stocks_folder, f) for f in os.listdir(stocks_folder) if f.endswith('.csv')][:10]

    parameters = [ 'Close', 'EMA_9', 'EMA_20']

    test_df = pd.read_csv(stock_files[0], nrows=3)

    close_price_idx, short_window_idx, long_window_idx = get_column_indices(test_df, parameters)
    strategy_params = (close_price_idx, short_window_idx, long_window_idx)

    with ThreadPoolExecutor() as executor:
        # Read stock data in parallel
        stock_data_list = list(tqdm(executor.map(read_stock_data, stock_files)))

        # Extract stock symbols from file names
        symbols = [extract_symbol_from_filename(file) for file in stock_files]

        # Apply strategy to each stock in parallel
        stocks_analysis = list(tqdm(executor.map(apply_strategy, stock_data_list, [MovingAverageCrossover]*len(stock_data_list), [strategy_params]*len(stock_data_list), symbols), total=len(stock_data_list), desc="Applying strategy"))

        # Save DataFrames as CSV files in parallel
        output_folder = 'output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        output_file_names = [os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file))[0]}_signals.csv') for file in stock_files]
        list(tqdm(executor.map(save_dataframe_as_csv, stocks_analysis, output_file_names)))

if __name__ == '__main__':
    main()