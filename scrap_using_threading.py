import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np

df = pd.read_csv('WebScrapingAssignment.csv')
df = df.drop('ADRESS', axis=1)

clg_names = []
def url_maker(college_name):
    url = 'https://www.google.com/search?q='
    college_name = college_name.replace(' ', '+')
    college_name = college_name.replace('&', '%26')
    college_name = college_name.replace(',', '%2C')
    url += college_name + ' address'
    
    return url

def find_addr(i):
    clg_name = df.iloc[i]['COLLEGE NAME']
    url = url_maker(clg_name)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        html_text = soup.find_all(class_='BNeawe iBp4i AP7Wnd')
        print(html_text[0].text)
        clgN = html_text[0].text
    except Exception as e:
        print("Error")
        clgN = 0
    
    df.at[i,'ADDRESS'] = clgN
        
from threading import Thread

class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

thread_v = 20
ii = 0
while(ii < len(df.index)):

    thread = []
    for i in range(ii,ii+thread_v):
        print(i)
        x = ThreadWithReturnValue(target=find_addr,args=(i,))
        thread.append(x)
        x.start()
    for j in thread:
        j.join()
    time.sleep(5)
    ii += thread_v

df.to_excel('WebScrapingAssignment_threading.xlsx', index=False)