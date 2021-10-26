import numpy as np
import pandas as pd

def basic_info (dataframe):
    print(dataframe.head(5))
    print(dataframe.columns)
    print(dataframe.describe())
    dataframe.info()


# add a drop collumn depending on the number of NaN
def dropduplicatecolumns (dataframe):
    for x in dataframe.columns.tolist():
        temp_dataframe = dataframe.drop([str(x)], axis=1)
        for y in temp_dataframe.columns.tolist():
            z = dataframe[str(x)] == temp_dataframe[str(y)]
            if z.any():
                nan1 = dataframe[str(x)].isna().sum()
                nan2 = temp_dataframe[str(y)].isna().sum()
                i = 0
                z = z.to_frame(name="0")
                z["1"] = np.NaN
                for item in z["0"]:
                    if item:
                        z.at[i, "1"] = 1
                        i = i + 1
                    else:
                        z.at[i, "1"] = 0
                        i = i + 1
                sumation = z["1"].sum()
                if sumation >= 6:
                    if nan1 >= nan2:
                        dataframe = dataframe.drop([str(x)], axis=1)
                        break
                    if nan2 > nan1:
                        dataframe = dataframe.drop([str(y)], axis=1)
                        break
    return dataframe

def dropcolumnswithnan(dataframe, typeoffinantal):
    if typeoffinantal == "BS":
        number = 15
    elif typeoffinantal == "IS":
        number = 7
    elif typeoffinantal == "CF":
        number = 10
    else:
        print("Financial type not available")
        return
    for x in dataframe.columns.tolist():
        numberofnan = dataframe[str(x)].isna().sum()
        if numberofnan >= number:
            dataframe = dataframe.drop([str(x)], axis=1)
    return dataframe

#accept number of years and number of columns different
def rename_columns (dataframe):
    i = 0
    for x in dataframe.columns.tolist():
        if i == 0:
            dataframe = dataframe.rename(columns={x: "Index"})
            i = i + 1
        elif i == 1:
            dataframe = dataframe.rename(columns={x: "Account"})
            i = i + 1
        elif i == 2:
            dataframe = dataframe.rename(columns={x: "2019"})
            i = i + 1
        elif i == 3:
            dataframe = dataframe.rename(columns={x: "2020"})
            i = i + 1
    return dataframe


Balance_Sheet = pd.read_csv("Balance_Sheet.csv")
Income_Statement = pd.read_csv("Income_Statement.csv")
Cash_Flow = pd.read_csv("Cash_Flow.csv")

Balance_Sheet = Balance_Sheet.dropna(how="all", axis=1)
Balance_Sheet = Balance_Sheet.dropna(how="all", axis=0)
Balance_Sheet = dropduplicatecolumns(Balance_Sheet)
Balance_Sheet = dropcolumnswithnan(Balance_Sheet, "BS")
Balance_Sheet = rename_columns(Balance_Sheet)
Balance_Sheet = Balance_Sheet.iloc[3:, :]
Balance_Sheet.to_csv("Balance_SheetU.csv")

Income_Statement = Income_Statement.dropna(how="all", axis=1)
Income_Statement = dropduplicatecolumns(Income_Statement)
Income_Statement = dropcolumnswithnan(Income_Statement, "BS")
Income_Statement = rename_columns(Income_Statement)
Income_Statement = Income_Statement.iloc[3:, :]
basic_info(Income_Statement)
Income_Statement.to_csv("Income_StatementU.csv")

Cash_Flow = Cash_Flow.dropna(how="all", axis=1)
Cash_Flow = dropduplicatecolumns(Cash_Flow)
Cash_Flow = dropcolumnswithnan(Cash_Flow, "BS")
Cash_Flow = rename_columns(Cash_Flow)
Cash_Flow = Cash_Flow.iloc[3:, :]
basic_info(Cash_Flow)
Cash_Flow.to_csv("Cash_FlowU.csv")



