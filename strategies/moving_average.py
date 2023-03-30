from strategies.base_strategy import BaseStrategy 
from backtest.transactions import Transactions

class MovingAverageCrossover(BaseStrategy):
    def __init__(self, data, close_price_idx: int, short_window_idx: str, long_window_idx: str, symbol: str ):
        super().__init__(data)
        self.short_window_idx = short_window_idx
        self.long_window_idx = long_window_idx
        self.symbol = symbol 
        self.close_price_idx = close_price_idx

    def generate_signals(self):
        short_mavg = self.data[:, self.short_window_idx]
        long_mavg = self.data[:, self.long_window_idx]

        transactions = Transactions()

        bought_price = 0
        for i in range(1, len(short_mavg)):
            if short_mavg[i - 1] < long_mavg[i - 1] and short_mavg[i] > long_mavg[i]:
                bought_price = self.data[i, self.close_price_idx]
                transactions.append_buy(self.data[i, 0], self.symbol, 'buy', bought_price)
            elif short_mavg[i - 1] > long_mavg[i - 1] and short_mavg[i] < long_mavg[i]:
                transactions.append_sell(self.data[i, 0], self.symbol, 'sell', bought_price, self.data[i, self.close_price_idx])
        return transactions.get_transactions()