import edgar
import pandas as pd
import os
from dateutil.parser import parse
import requests
import datetime as dt

pd.pandas.set_option('display.max_columns', None)
edgar.download_index('All Financial Statements', 1993, skip_all_present_except_last=False,
                     user_agent="your-user-agent")

def foreachfile (filepath, company, report):
    final_data = pd.DataFrame()
    for x in os.listdir(filepath):
        dataframe = pd.read_csv(f'{filepath}/{x}', sep='\t', lineterminator='\n', names=None)
        dataframe.columns.values[0] = 'Item'
        dataframe = dataframe[(dataframe['Item'].str.contains(company)) & (dataframe['Item'].str.contains(report))]
        final_data = pd.concat([final_data, dataframe])
    return final_data

def is_date(string, fuzzy=True):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def info_dataframe (data, company, report):
    data["Item"] = data["Item"].str.split("|")
    final_dataframe = pd.DataFrame(columns=["Company_Name", "Filing", "Date", "Url"])
    i = 0
    link = "https://www.sec.gov/Archives/"
    for lists in data["Item"]:
        for sublists in lists:
            if company in sublists:
                final_dataframe.at[i, "Company_Name"] = sublists
            if report in sublists:
                final_dataframe.at[i, "Filing"] = sublists
            if is_date(str(sublists)):
                final_dataframe.at[i, "Date"] = sublists
            if 'htm' in sublists:
                final_dataframe.at[i, "Url"] = link + str(sublists)
        i = i + 1
    final_dataframe.to_csv("dataframe.csv")
    final_dataframe["Date"] = pd.to_datetime(final_dataframe["Date"])
    return final_dataframe

def SelectFinantialStatement (Data, Date):
    url = Data[Data["Date"] == Date]
    url = url["Url"]
    return url


selectedcompany = 'AMAZON COM INC'
selectedreport = '10-K'
year = dt.datetime(2021, 2, 3)

filePath1 = "All Financial Statements"
csv = foreachfile(filePath1, selectedcompany, selectedreport)
info = info_dataframe(csv, "AMAZON COM INC", "10-K")
mylink = SelectFinantialStatement(info, year)
