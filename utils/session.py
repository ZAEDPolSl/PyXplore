import requests
import json
import random
import time
from bs4 import BeautifulSoup
from lxml import html
from utils.logger import ILogger

class Session(requests.Session):
    '''Session object based on requests.Session'''
    
    def __init__(self, logger: ILogger = None) -> None:
        '''
        Web session for http communication based on requests.Session
        -------
        Parameters:
        - logger: ILogger
            Interface based on ILogger, responsible for logging. It has higher priority than the logger passed in ISettings
        '''
        super().__init__()
        self.logger = logger  
        if not self.logger:
            raise Exception('Not initalized logger - LonginusClient!')
        
    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, *args):
        #Detach proxy_configuration
        return super().__exit__(*args)

    def update_headers(self, headers_dict:dict):
        """method that will set or update headers"""
        self.headers.update(headers_dict)

    def get_soup(self, url: str):
        """method that will get soup from http"""
        response = self.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def post_json(self, url: str, **kwargs):
        content = self.post(url, timeout=180, **kwargs)
        if content.status_code != 200:
            time.sleep(random.randint(5,15))
            content = self.post(url, timeout=240, **kwargs)
        return json.loads(content.text)