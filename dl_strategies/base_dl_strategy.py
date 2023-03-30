import torch

class BaseDLStrategy:
    def __init__(self, data, device="cpu"):
        self.data = data
        self.device = torch.device(device)

    def preprocess_data(self):
        raise NotImplementedError("Subclasses must implement the preprocess_data method")

    def build_model(self):
        raise NotImplementedError("Subclasses must implement the build_model method")

    def train(self, epochs, batch_size, learning_rate):
        raise NotImplementedError("Subclasses must implement the train method")

    def evaluate(self, batch_size):
        raise NotImplementedError("Subclasses must implement the evaluate method")

    def generate_signals(self):
        raise NotImplementedError("Subclasses must implement the generate_signals method")

    def save_model(self, filepath):
        raise NotImplementedError("Subclasses must implement the save_model method")

    def load_model(self, filepath):
        raise NotImplementedError("Subclasses must implement the load_model method")