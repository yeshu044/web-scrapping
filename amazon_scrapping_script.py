from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import pandas as pd
from datetime import date
from pathlib import Path

def getUrl(item,index):
    template = 'https://www.amazon.in/s?k={}&page={}'
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
        result = soup.find_all('div',{'data-component-type':'s-search-result'})
        flag = 1
        for idx,i in enumerate(result):
            try:
                title = i.find('span',class_='a-size-base-plus a-color-base a-text-normal').text
                price = i.find('span',class_='a-offscreen').text
                rating = i.find('span',class_='a-icon-alt').text.split(' ')[0]
                userBase = i.find('span',class_='a-size-base').text
                link = 'https://www.amazon.in/'+i.find('a',class_='a-link-normal s-no-outline')['href']
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
def createConnection():
    engine = create_engine('postgresql://yeshwanth:12345@localhost:5432/product_data')
    return engine
def getProductId(productName,engine):
    query = f"select * from product_type where product_type = '{productName}'" 
    c = engine.execute(query)
    l = c.fetchall()
    if len(l) > 1:
        return l[0][0]
    else:
        id= str(uuid.uuid4())
        query = f"insert into product_type values(\'{id}\',\'{productName}\')"
        engine.execute(query)
        return id
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
        getResult(category,5,'/home/tricon/labyrinth/projects/scrapping_outputs/amazon/')
    driver.close()
