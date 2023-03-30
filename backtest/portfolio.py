import pandas as pd
from pandas import DataFrame


class PortfolioManagement:
    def __init__(self, config):
        self._portfolio = {}
        self._budget = config["initial_equity"] * (1 - config["per_cash"])
        self._portfolio_history = {}
        self._budget_history = {}
        self._daily_return = []


    @property
    def portfolio(self):
        return self._portfolio
    
    @property
    def budget(self):
        return self._budget