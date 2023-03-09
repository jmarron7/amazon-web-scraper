from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import amazon_scraper as amzn_scrpr

if __name__ == '__main__':

    # User Agent to be used with BeautifulSoup later
    # You can get your User-Agent from websites like http://httpbin.org/get or https://explore.whatismybrowser.com/useragents/parse/
    USER_AGENT = ''
    
    HEADERS = ({'User-Agent': USER_AGENT, 'Accept-Language': 'en-US, en;q=0.5', 'Accept-Language': 'en-US, en;q=0.5'})

    # The keywords to search for
    KEYWORDS = ""

    # Cleaning Keywords to add to Amazon search URL
    KEYWORDS = KEYWORDS.lower().strip().replace(" ", "+")

    # The complete webpage URL to scrape
    URL = "https://www.amazon.com/s?k=" + KEYWORDS

    print("Preparing to scrape " + URL)
    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    # Store the product links
    links_list = []

    links_length = len(links)
    print("Gathering a total of " + str(links_length) + " links...")

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    # Dictionary to store info being scraped from Amazon
    products_dict = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
    
    # Loop for extracting product details from each link 
    for index,link in enumerate(links_list):
        print("Scraping link " + str(index + 1) + " of " + str(links_length))
        product_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        product_soup = BeautifulSoup(product_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        products_dict['title'].append(amzn_scrpr.get_title(product_soup))
        products_dict['price'].append(amzn_scrpr.get_price(product_soup))
        products_dict['rating'].append(amzn_scrpr.get_rating(product_soup))
        products_dict['reviews'].append(amzn_scrpr.get_review_count(product_soup))
        products_dict['availability'].append(amzn_scrpr.get_availability(product_soup))

    print("Web scraping finished...")
    
    amazon_df = pd.DataFrame.from_dict(products_dict)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    
    print("Saving to CSV...")
    amazon_df.to_csv("data/amazon_data.csv", header=True, index=False)
   