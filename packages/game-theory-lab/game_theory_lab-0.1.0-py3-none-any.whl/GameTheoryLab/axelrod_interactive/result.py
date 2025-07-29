import pandas as pd

class Result:
    def __init__(self, data):
        self.data = data

    def to_csv(self, file_name: str):
        df = pd.DataFrame(self.data)
        df.to_csv(file_name, index=False)