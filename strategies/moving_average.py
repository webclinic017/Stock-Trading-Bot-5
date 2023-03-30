from base_strategy import BaseStrategy 
from backtest.transactions import Transactions

class MovingAverageCrossover(BaseStrategy):
    def __init__(self, data, short_window: str, long_window: str, symbol: str ):
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window
        self.symbol = symbol 

    def generate_signals(self):
        short_mavg = self.data[self.short_window]
        long_mavg = self.data[self.long_window]

        transactions = Transactions() 

        bought_price = 0 
        for i in range(1, len(short_mavg)):
            if short_mavg[i - 1] < long_mavg[i - 1] and short_mavg[i] > long_mavg[i]:
                bought_price = self.data['Close'][i] 
                transactions.append_buy( self.data['Date'][i],  self.symbol,  'buy', bought_price )
            elif short_mavg[i - 1] > long_mavg[i - 1] and short_mavg[i] < long_mavg[i]:
                transactions.append_sell( self.data['Date'][i],  self.symbol,  'sell', bought_price, self.data['Close'][i])

        return transactions.get_transactions()