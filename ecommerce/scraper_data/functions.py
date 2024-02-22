from bs4 import BeautifulSoup
from typing import Generator

from ..src_base_scraper.product_info import ProductData

def get_pages(_):
    
    return (f'https://www.dedeman.ro/ro/mobilier-birou/c/96?page={x}' for x in range(1,19))

def get_product(input_html_str:str) -> Generator:
    
    soup = BeautifulSoup(input_html_str,'lxml')
    
    return (x.find('a',class_='product-item-link')['href'] for x in soup.find_all('li',class_='item product product-item'))

def get_product_data(input_html_str):
    
    soup = BeautifulSoup(input_html_str,'lxml')
    
    yield soup.find('h1',attrs={'class':'page-title','itemprop':'name'}).text

def get_pages(_):
    
    return (f'https://fragrancewholesale.co.uk/collections/chatler?page={i}' for i in range(1,7))

def get_product(input_html:str) -> Generator:
    
    soup = BeautifulSoup(input_html,'lxml')
    return ('https://fragrancewholesale.co.uk/'+ x.get('href') for x in soup.find_all('a',class_='title') if x.get('href'))
    return ('https://fragrancewholesale.co.uk/'+x.href for x in soup.find('div',attrs={'class':'products products-grid  full-width'}).find_all('a',attrs = {'product-image'}))

def get_product_data(input_html):
    
    soup = BeautifulSoup(input_html,'lxml')
    
    name = soup.find('div',class_='product-title').h1.text
    price = soup.find('span',class_='money',attrs={'id':'ProductPrice'}).text
    
    description = soup.find('div',class_='description rte')
    picture  =  soup.find('div',class_='featured-container').find('img').get('src')[2::]
    print(f'found {picture}')
    yield {'name':name,'price':price,'description':description,'image':picture}