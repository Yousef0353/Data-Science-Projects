# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 18:54:45 2022

@author: balas
"""

import requests 
from bs4 import BeautifulSoup
import pandas as pd

def extract(location,tag, page):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"}
    url = f"https://www.jobindex.dk/jobsoegning/{location}?page={page}&q={tag}"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html.parser")
    
    return soup

joblist = []

def transform(soup):
    divs = soup.find_all("div", class_="jobsearch-result")
    for item in divs:
        title = item.find_all("b")[0].text.strip()
        company = item.find_all("b")[1].text.strip()
        published_date = item.find("time").text.strip()
        summary = item.find_all("p")[1].text.strip()
        job_location = item.find_all("p")[0].text.strip()
        job_url =  item.select_one('[data-click*="u="]:has(> b)')['href']
        
        job = {
            "title" : title, 
            "company" : company,
            "published_date" : published_date,
            "summary" : summary,
            "job_location" : job_location,
            "Job_url" : job_url
        }
        joblist.append(job)
    return


keywords1 = input("Hvor søger du?: ") 
keywords2 = input("Hvad søger du?: ")

#Applying function
for x in range(1,10):
    c = extract(keywords1, keywords2, 0)
    transform(c)
    
#Converting list to dataframe
df = pd.DataFrame(joblist)
df.to_csv('Jobpost_ '+str(keywords2)+'.csv', index=False, encoding='utf-8-sig')
print("Finished")



#https://stackoverflow.com/questions/25788037/pandas-df-to-csvfile-csv-encode-utf-8-still-gives-trash-characters-for-min


