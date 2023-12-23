import typing
from .scraper import ScraperManager,ScraperInitialNode,ScraperNode,ProductScraperNode,ScraperCallable
from .requests_handler import RequestsHandler

class ScraperManagerBuilder:
    
    def __init__(self,
                 requests_handler : RequestsHandler ,
                 initial_url : str ,
                 initial_node_function : typing.Callable,
                 node_functions : list[typing.Callable],
                 product_functions : typing.Callable
                 ) -> None:
        self.requests_handler = requests_handler
        self.manager = ScraperManager()
        self.initial_url = initial_url
        self.initial_node_function = initial_node_function
        self.node_functions = node_functions
        self.product_functions =product_functions
    
    def _create_scraper_callable(self,raw_callable:typing.Callable):
        
        return ScraperCallable(requests_handler = self.requests_handler,
                               extract_data_callable = raw_callable
                               )
    def create_initiation_point(self):
        initial_point = ScraperInitialNode(initial_url = self.initial_url,
                                           extract_data_callable = self._create_scraper_callable(self.initial_node_function)
                                           )
        self.manager.append(node=initial_point)
    
    def _create_node(self,function : typing.Callable):
        
        node = ScraperNode(extract_data_callable = self._create_scraper_callable(function))
        
        self.manager.append(node=node)
    
    def create_node_layers(self):
        
        for function in self.node_functions :
            
            self._create_node(function = function)
    def create_product_layer(self):
        
        product_node = ProductScraperNode(extract_data_callable = self._create_scraper_callable(self.product_functions))
        
        self.manager.append(node = product_node)
    
    def build(self) -> ScraperManager:
        self.create_initiation_point()
        self.create_node_layers()
        self.create_product_layer()
        
        return self.manager