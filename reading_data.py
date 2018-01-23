# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:11:43 2018

@author: rafael

Part of the cousera assignment from data science with python project
"""
import pandas as pd

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    with open("data/university_towns.txt") as f:
        data = f.read()
        names = list()
        for txt in data.split("\n"):
            if txt[-6:] == "[edit]":
                state = txt[:-6]
            else:
                names.append([state, txt.split("(" )[0]])
        df = pd.DataFrame(names, columns = ["States", "University Towns"])
    return df.drop(df.index.size-1)
    
def get_GDP_values(quarter = True):
    if quarter:
        GDP = pd.read_excel("data/gdplev.xlsx", "Sheet1", header = 5, skiprows = 2, parse_cols = [4,6])
        GDP.columns = ["Quarter year", "GDP in bi of 2009 dollars Quarter"]
    else:
        GDP = pd.read_excel("data/gdplev.xlsx", "Sheet1", header = 5, skiprows = 2, parse_cols = [0,2], skip_footer=195)
        GDP.columns = ["year", "GDP in bi of 2009 dollars"]
    return GDP


if __name__ == "__main__" :
    print(get_GDP_values(quarter = False))