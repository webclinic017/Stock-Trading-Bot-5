class BaseStrategy:
    def __init__(self, data):
        self.data = data

    def generate_signals(self):
        raise NotImplementedError("This Method is not yet implemented")