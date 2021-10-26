import edgar
import pandas as pd
import numpy as np
import os
from dateutil.parser import parse
import requests
import datetime as dt
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import codecs

def getoneyearshtml (link, selectedreport):
    options = webdriver.ChromeOptions()
    options.add_argument('--start maximized')
    options.add_argument("--disable extensions")
    #options.add_argument("headless")
    chrome_driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    chrome_driver.get(link)
    index_html = chrome_driver.page_source
    first_html_dataframe = pd.read_html(index_html)
    first_html_dataframe = first_html_dataframe[0]
    first_html_link = first_html_dataframe[first_html_dataframe['Description'].str.contains(selectedreport)]
    first_html_link = first_html_link['Document'].str.split(' ')
    first_html_link = first_html_link[0][0]
    report_formatted = mylink.replace('-', '').replace('index.html', '')
    url = report_formatted + '/' + first_html_link
    chrome_driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    chrome_driver.get(url)
    data_html = chrome_driver.page_source
    actual_data = pd.read_html(data_html)
    return actual_data

def extractdata (data):
    Balance_Sheet = {}
    Income_Statement = {}
    Cash_Flow = {}
    i = 0
    ii = 0
    iii = 0
    for x in data:
        if x.dtypes[0] == object:
            BS = x[0].str.contains("Retained earnings") | x[0].str.contains("Total assets")
            if BS.any():
                Balance_Sheet[i] = x
                i = i + 1
            IS = x[0].str.contains("Basic") | x[0].str.contains("sales")
            if IS.any():
                Income_Statement[ii] = x
                ii = ii + 1
            CF = x[0].str.contains("INVESTING ACTIVITIES") | x[0].str.contains("OPERATING ACTIVITIES")
            if CF.any():
                Cash_Flow[iii] = x
                iii = iii + 1
    return Balance_Sheet, Income_Statement, Cash_Flow

mylink = "https://www.sec.gov/Archives/edgar/data/1018724/0001018724-21-000004-index.html"
html_data = getoneyearshtml(mylink, "10-K")
Balance_Sheet, Income_Statement, Cash_Flow = extractdata(html_data)

Balance_Sheet = Balance_Sheet[1]
print(Balance_Sheet)
Balance_Sheet.to_csv("Balance_Sheet.csv")

Income_Statement = Income_Statement[8]
print(Income_Statement)
Income_Statement.to_csv("Income_Statement.csv")

Cash_Flow = Cash_Flow[0]
print(Cash_Flow)
Cash_Flow.to_csv("Cash_Flow.csv")

