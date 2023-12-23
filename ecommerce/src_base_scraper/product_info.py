import typing
from dataclasses import dataclass


ProductInfo = typing.Dict[str,str]

@dataclass
class ProductData:
    
    url : str
    product_info : ProductInfo
    raw_text_response : str = ''
