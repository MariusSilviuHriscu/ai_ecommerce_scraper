import typing
from typing import Protocol

from .requests_handler import RequestsHandler
from .product_info import ProductData


ScraperExecutableReturnable = typing.Generator[str,None,None] | typing.Generator[ProductData,None,None]

class ScraperCallable:
    
    def __init__(self, requests_handler : RequestsHandler ,
                 extract_data_callable : typing.Callable[[str] , ScraperExecutableReturnable] 
                 ):
        self.requests_handler = requests_handler
        self.extract_data_callable = extract_data_callable
    
    def get_url_data(self,url : str,params : dict[str,str]={}) -> ScraperExecutableReturnable:
        
        response_text = self.requests_handler.get(url, params)
        
        return self.extract_data_callable(response_text)
    

class ScrapingNodeTemplate(Protocol):
    extract_data_callable : ScraperCallable
    def get_data(self) -> typing.Generator[typing.Any,None,None]:
        pass
    def get_data_threading(self):
        pass
    def set_previous_node(self):
        pass
    
class ScraperInitialNode :
    def __init__(self , initial_url : str , extract_data_callable : ScraperCallable ):
        
        self.initial_url  = initial_url
        self.extract_data_callable = extract_data_callable

    def get_data(self) -> typing.Generator[str,None,None]:
        
        data_generator = self.extract_data_callable.get_url_data(url = self.initial_url)
        
        return data_generator
    def set_previous_node(self):
        raise ValueError('cannot set another node as previous to this')

class ScraperNode:
    
    def __init__(self ,
                 extract_data_callable : ScraperCallable ,
                 previous_node: ScrapingNodeTemplate | None = None
    ):
        self.extract_data_callable = extract_data_callable
        self.previous_node = previous_node
        
    def get_data(self) -> typing.Generator[str,None,None]:    
        previous_node_data_generator = self.previous_node.get_data()
        for data_point in previous_node_data_generator:
            
            yield from self.extract_data_callable.get_url_data(url = data_point)
    def set_previous_node(self,node : ScrapingNodeTemplate):
        self.previous_node = node

class ProductScraperNode :
    
    def __init__(self ,
                 extract_data_callable : ScraperCallable ,
                 previous_node: ScrapingNodeTemplate | None = None):
        self.extract_data_callable = extract_data_callable
        self.previous_node = previous_node

    def get_data(self) -> typing.Generator[ProductData, None,None]:
        
        previous_node_data_generator = self.previous_node.get_data()
        for data_point in previous_node_data_generator:
            
            product_generator = self.extract_data_callable.get_url_data(url = data_point)
            for product_info in product_generator:
            #product generator has only one yielded data , it's just for consistency
                yield ProductData(url = data_point,
                                  product_info = product_info
                                  )
            
    def set_previous_node(self,node : ScrapingNodeTemplate):
        self.previous_node = node


class ScraperManager :
    
    def __init__(self , current_final_node : ScrapingNodeTemplate | None = None):
        
        self.current_final_node = current_final_node
    
    def append(self, node :ScrapingNodeTemplate):
        if self.current_final_node is not None:
            node.set_previous_node(self.current_final_node)
        
        self.current_final_node = node
    
    def get_data(self, parallel_processing_flag : bool , depth_parallelism:int=1) -> typing.Generator[ProductData, None,None] :
        if parallel_processing_flag:
            return self.current_final_node.get
        return self.current_final_node.get_data()