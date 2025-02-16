
class Movie:

    def __init__(self, name: str, data: dict):

        self.name = name
        self.data = data

    def get_datapoint(self, input_key: str) -> str:
        
        for data_key in self.data.keys():

            if data_key == input_key:
                return self.data[data_key]
            

    def update_datapoint(self, input_key:str, new_value: str) -> None:

        for data_key in self.data.keys():

            if data_key == input_key:
                self.data[data_key] = new_value
