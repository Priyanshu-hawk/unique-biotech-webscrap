import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

df = pd.read_csv('WebScrapingAssignment.csv')

clg_names = []
def url_maker(college_name):
    url = 'https://www.google.com/search?q='
    college_name = college_name.replace(' ', '+')
    college_name = college_name.replace('&', '%26')
    college_name = college_name.replace(',', '%2C')
    url += college_name + ' address'
    
    return url

def find_addr(clg_name):
    url = url_maker(clg_name)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        html_text = soup.find_all(class_='BNeawe iBp4i AP7Wnd')
        print(html_text[0].text)
        clg_names.append(html_text[0].text)
    except Exception as e:
        clg_names.append(0)


for i in df.index:
    df.at[i,'ADRESS'] = clg_names[i]

df.to_excel('WebScrapingAssignment_non_threading.xlsx', index=False)
