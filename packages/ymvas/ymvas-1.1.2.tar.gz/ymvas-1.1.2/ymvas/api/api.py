import requests

class API:
    url = 'https://api.ymvas.com'

    def __init__(
        self,
        auth:str ,
        is_ssh:bool = False
    ):
        
        self.auth = auth
        pass
