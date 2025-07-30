class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def hello(self):
        return "Hello World from CIQ SDK!"
