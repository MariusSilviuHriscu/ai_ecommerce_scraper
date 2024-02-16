import typing
from dataclasses import dataclass


ProductInfo = typing.Dict[str,str]

@dataclass
class ProductData:
    
    url : str
    product_info : dict
    raw_text_response : str = ''
    @property
    def product_info_keys(self):
        return self.product_info.keys()
