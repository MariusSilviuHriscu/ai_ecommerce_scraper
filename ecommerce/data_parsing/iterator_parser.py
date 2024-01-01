from ..src_base_scraper.requests_handler import RequestsHandler

import typing
import re


class EcommerceFuncGenerator():
    
    def __init__(self, requests_handler: RequestsHandler, first_url : str , max_page : int | None = None):
        
        self.requests_handler = requests_handler
        self.url_generator_string:str = self._remove_page_number_placeholder(first_url)
        self.max_page = max_page
                
    def _remove_page_number_placeholder(self,url_with_placeholder:str) -> str:

        pattern = r'{(\d+)}'
        replaced_url = re.sub(pattern, '{}', url_with_placeholder)
        
        return replaced_url
    
    def generate_url(self,page_number:int) -> str:
        return self.url_generator_string.format(page_number)
    
    def _validate_url(self,url:str):
        
        response = self.requests_handler.get(url=url,params=None,raw_response=True,cache_flag=False)
        print(f'{url} is {response.status_code}')
        return response.status_code == 200
    def set_max_page(self):
        i = 1
        while True:
            if self._validate_url(url=self.generate_url(page_number=i)):
                self.max_page = i
            else:
                break
            i += 1
    def generate_url_function(self) -> typing.Callable[[str],typing.Generator[str,None,None]]:
        
        if self.max_page is None:
            self.set_max_page()
        return lambda _ : (self.generate_url(page_number=x) for x in range(1,self.max_page + 1))
        
