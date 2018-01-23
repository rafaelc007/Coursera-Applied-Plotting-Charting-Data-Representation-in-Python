# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:11:43 2018

@author: rafael

Part of the cousera assignment from data science with python project
"""
import pandas as pd

def clean_univ_data(data):
    names = list()
    for txt in data.split("\n"):
        if txt[-6:] == "[edit]":
            state = txt[:-6]
        else:
            names.append([state, txt.split("(" )[0]])
    df = pd.DataFrame(names, columns = ["States", "University Towns"])
    return df.drop(df.index.size-1)


if __name__ == "__main__" :
    with open("data/university_towns.txt") as f:
        data = f.read()
        print(clean_univ_data(data))