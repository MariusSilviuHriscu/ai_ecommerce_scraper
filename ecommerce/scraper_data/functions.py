from bs4 import BeautifulSoup
from typing import Generator

def get_pages(_):
    
    return (f'https://www.dedeman.ro/ro/hote-bucatarie-si-accesorii/c/669?page={x}' for x in range(1,4))

def get_product(input_html_str:str) -> Generator:
    
    soup = BeautifulSoup(input_html_str,'lxml')
    
    return (x.find('a',class_='product-item-link')['href'] for x in soup.find_all('li',class_='item product product-item'))

def get_product_data(input_html_str):
    
    soup = BeautifulSoup(input_html_str,'lxml')
    
    yield soup.find('h1',attrs={'class':'page-title','itemprop':'name'}).text