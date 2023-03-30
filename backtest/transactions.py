import pandas as pd


class Transactions:
    def __init__(self):
        self._transactions = []

    def append_buy(self, date: str, symbol: str, type: str, bought_price: float):
        self._transactions.append({'date': date,
                                   'symbol': symbol,
                                   'type': type,
                                   'bought_price': bought_price,
                                   'sold_price': None,
                                   'avg_sold_price': None,
                                   'profit_rate': None
                                })

    def append_sell(self, date, symbol, type, bought_price, sold_price):
        self._transactions.append({'date': date,
                                   'symbol': symbol,
                                   'type': type,
                                   'bought_price': bought_price,
                                   'sold_price': sold_price,
                                   'profit_rate': ((sold_price - bought_price) / bought_price) * 100
                                })

    def get_transactions(self):
        return pd.DataFrame(self._transactions)