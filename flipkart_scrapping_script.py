from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import pandas as pd
from datetime import date
from pathlib import Path

def getUrl(item,index):
    template = 'https://www.flipkart.com/search?q={}&page={}'
    search_term = item.replace(' ','+')
    return template.format(search_term,index)
    
def findList(item,iterations):
    returnList =[]
    titles =[]
    for i in range(1,iterations+1):
        flag = 1
        print(i)
        driver.get(getUrl(item,i))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        result = soup.find_all('div',class_='_4ddWXP')
        flag = 1
        for idx,i in enumerate(result):
            try:
                title = i.find('a',class_='s1Q9rs').text
                price = i.find('div',class_='_30jeq3').text
                mrp = i.find('div',class_='_3I9_wc').text
                userBase = i.find('span',class_='_2_R_DZ').text.replace(',','').replace('(','').replace(')','')
                rating = i.find('div',class_='_3LWZlK').text
                link = 'https://www.flipkart.com'+i.find('a',class_='s1Q9rs')['href']
                if title not in titles:
                    titles.append(title)
                    returnList.append({'product':title,'price':price,'rating':float(rating),'userBase':int(userBase.replace(',','')),'product_link':link})
                    flag =0
            except Exception as err:
                print(err)
                continue
        if flag == 1:
            return returnList
    return returnList

def saveToPath(df,path,fileName):
    output_dir = Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / fileName)
    
def getResult(product,iterationCount,location):
    result = findList(product,iterationCount)
    df =pd.DataFrame(result)
    path = location +product.replace(' ','_')+'/'+str(date.today()).replace('-','/')
    file = product.replace(' ','_') + '.csv'
    saveToPath(df.sort_values(by=['userBase','rating'],ascending=False),path,file)
    d = {}
    for i in df['product']:
        for word in i.split(' '):
            if word in  d:
                d[word] = d[word]+1
            else:
                d[word] = 1
    frequecyDataFrame = pd.DataFrame(d.items(),columns=['word','frequency'])
    path = location +product.replace(' ','_')+'/'+str(date.today()).replace('-','/')
    fileName = product.replace(' ','_') + '_frequency_frequency.csv'
    saveToPath(frequecyDataFrame.sort_values(by=['frequency'],ascending=False),path,fileName)
 
if __name__=="__main__":
    categoryList = ['cooking oil']
    driver = webdriver.Chrome('/home/tricon/Downloads/chromedriver')
    for category in categoryList:
        getResult(category,5,'/home/tricon/labyrinth/projects/scrapping_outputs/flipkart/')
    driver.close()
