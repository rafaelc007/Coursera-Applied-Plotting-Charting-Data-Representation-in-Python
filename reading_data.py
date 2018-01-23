# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:11:43 2018

@author: rafael

Part of the cousera assignment from data science with python project
"""
import pandas as pd

def clean_univ_data(data):
    state_names = list()
    uni_towns = list()
    for txt in data.split("\n"):
        if txt[-6:] == "[edit]":
            state = txt[:-6]
        else:
            uni_towns.append(txt.split("(" )[0])
            state_names.append(state)
    df = pd.DataFrame([state_names, uni_towns]).T
    df.columns = ["States", "University Towns"]
    return df


if __name__ == "__main__" :
    with open("data/university_towns.txt") as f:
        data = f.read()
        print(clean_univ_data(data))