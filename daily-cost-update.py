import pandas as pd
import glob
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import pandas as pd
from datetime import date
from pathlib import Path
from datetime import datetime


path = './products/'

def getCost(driver,link,source):
    try:
        if source == 'flipkart':
            driver.get(link)
            soup = BeautifulSoup(driver.page_source,'html.parser')
            return  soup.find_all('div',class_='_30jeq3 _16Jk6d')[0].text
        else:
            driver.get(link)
            soup = BeautifulSoup(driver.page_source,'html.parser')
            return soup.find_all('span',id='priceblock_ourprice')[0].text
    except Exception as err:
        print(err)
        return 'Nan'
        
if __name__=="__main__":
    products = pd.concat([pd.read_csv(f) for f in glob.glob(path+'*.csv')]).drop_duplicates('name_hash')
    driver = webdriver.Chrome('/home/tricon/Downloads/chromedriver')
    for i in range(products.shape[0]):
        driver = webdriver.Chrome('/home/tricon/Downloads/chromedriver')
        print(products.iloc[i]['price'])
        products.price.iloc[[i]] = getCost(driver,products.iloc[i]['product_link'],products.iloc[i]['soure'])
    driver.quit()
    date  = datetime.now().strftime('%Y%m%d')
    date_formatted = datetime.now().strftime('%D')
    products_cost = products[['product','price','name_hash']] 
    products_cost['date'] = date_formatted
    products_cost.to_csv(f'product_cost/{date}_product_cost.csv')