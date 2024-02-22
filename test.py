from ecommerce.src_base_scraper.scraper_builder import ScraperManagerBuilder
from ecommerce.src_base_scraper.requests_handler import RequestsHandler
from ecommerce.scraper_data.functions import get_pages,get_product,get_product_data
from ecommerce.data_parsing.iterator_parser import EcommerceFuncGenerator
handler = RequestsHandler.create_instance(None)
scrfunc = EcommerceFuncGenerator(requests_handler=handler,
                                 first_url = 'https://fragrancewholesale.co.uk/collections/chatler?page={2}',
                                 max_page = 6
                                 )
func = scrfunc.generate_url_function()
builder = ScraperManagerBuilder(requests_handler = handler,
                      initial_url='https://fragrancewholesale.co.uk/collections/chatler?page=1',
                      initial_node_function = get_pages,
                      node_functions=[get_product],
                      product_functions = get_product_data
                      )
scraper = builder.build()
a = scraper.get_data(parallel_processing_flag=False)
from ecommerce.src_base_scraper.product_info import ProductData

import requests
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

import requests
import os

def download_url(url, destination_folder):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(destination_folder, url.split("/")[-1])
            with open(filename, 'wb') as file:
                file.write(response.content)
                print(f"Downloaded: {url}")
        else:
            print(f"Failed to download: {url} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def download_all_urls(urls, destination_folder):
    for url in urls:
        download_url('https://'+url, destination_folder)

if __name__ == "__main__":
    # Example usage
    urls_generator = (i.product_info.get('image') for i in a)
    destination_folder = "downloads"

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    download_all_urls(urls_generator, destination_folder)