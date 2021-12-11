from bs4 import  BeautifulSoup
import requests
htmlText = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text

soup = BeautifulSoup(htmlText,'lxml')
jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
print(len(jobs))
