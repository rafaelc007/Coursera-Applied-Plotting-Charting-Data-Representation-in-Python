# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:11:43 2018

@author: rafael

Part of the cousera assignment from data science with python project
"""
import pandas as pd
from scipy import stats

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
                names.append([state, txt.split(" (" )[0]])
        df = pd.DataFrame(names, columns = ["State", "RegionName"])
    return df.drop(df.index.size-1)
    
def get_GDP_values(quarter = True):
    if quarter:
        GDP = pd.read_excel("data/gdplev.xlsx", "Sheet1", header = 5, skiprows = 2, parse_cols = [4,6])
        GDP.columns = ["year", "GDP"]
    else:
        GDP = pd.read_excel("data/gdplev.xlsx", "Sheet1", header = 5, skiprows = 2, parse_cols = [0,2], skip_footer=195)
        GDP.columns = ["year", "GDP"]
    return GDP
    
def detect_recession(data, cut_before_2000 = False):
    ## use data from year 2000 onwards
    if cut_before_2000:
        data = data.iloc[212:]
    
    flag1, flag2, flag3 = [False]*3
    Q1 = ""
    ## copying data and setting index
    n_data = data.copy()
    data.set_index("year", inplace = True)
    
    ## create new recession column
    data["recession"] = [False]*data.index.size
    ## get difference between lines in data
    n_data.iloc[:,1] = n_data.iloc[:,1].diff()
    ## remove first year
    n_data.iloc[0,1] = 0
    for index, frame in n_data.groupby("year"):
        if flag1 :
            if flag2 :
                if flag3 :
                    if frame.iloc[0,1] > 0:
                        data.loc[Q1:index, "recession"] = [True]*4
                    flag1 = False
                    flag2 = False
                    flag3 = False
                else:
                    if frame.iloc[0,1] > 0:
                        flag3 = True  
                    else:
                        flag1, flag2, flag3 = [False]*3
            else:
                if frame.iloc[0,1] < 0:
                    flag2 = True
                else:
                    flag2, flag3 = [False]*2
                    Q1 = index
        else:
            if frame.iloc[0,1] < 0:
                flag1 = True
                Q1 = index
            else:
                flag1, flag2, flag3 = [False]*3
                    
    return data
    
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    data = detect_recession(get_GDP_values(), True)
    
    ## separate recession data
    res_data = data[data.loc[:,"recession"]].copy()
    
    ## returning the start
    start = list()
    for idx in range(0, res_data.index.size):
        if idx % 4 == 0:
            start.append(res_data.index[idx])
        
    return start
    
def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    data = detect_recession(get_GDP_values(), True)
    
    ## separate recession data
    res_data = data[data.loc[:,"recession"]].copy()
    
    ## returning the end
    end = list()
    for idx in range(0, res_data.index.size):
        if idx % 4 == 0:
            end.append(res_data.index[idx+3])
        
    return end
    
def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    data = detect_recession(get_GDP_values(), True)
    
    ## separate recession data
    res_data = data[data.loc[:,"recession"]].copy()
    res_data.reset_index(inplace = True)
    
    ## returning the end
    bottom = list()
    for idx in range(0, int(res_data.index.size/4)):
        bottom.append(res_data.iloc[res_data.iloc[4*idx:4*idx+4,1].argmin(),0])
        
    return bottom
    
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    
    ## reading the data
    housing_data = pd.read_csv("data/City_Zhvi_AllHomes.csv")
    
    ## getting data from year 2000 onward
    drop_cols = housing_data.loc[:,"1996-04":"1999-12"].columns
    housing_data = housing_data.drop(drop_cols, axis = 1)
    
    ## determining quarters
    quarter_data = housing_data.loc[:,["State","RegionName"]].copy()
    quarter_data.replace({"State":states}, inplace = True)
    
    for period in housing_data.loc[:,"2000-01":].columns[::3]:
        year, month = period.split("-")
        if month == "01":
            ## we are in first quarter
            quarter_data[year+"Q1"] = housing_data.loc[:,year+"-01":year+"-03"].sum(axis = 1)
        if month == "04":
            ## we are in second quarter
            quarter_data[year+"Q2"] = housing_data.loc[:,year+"-04":year+"-06"].sum(axis = 1)
        if month == "07":
            ## we are in third quarter
            quarter_data[year+"Q3"] = housing_data.loc[:,year+"-07":year+"-09"].sum(axis = 1)
        if month == "07":
            ## we are in fourth quarter
            quarter_data[year+"Q4"] = housing_data.loc[:,year+"-10":year+"-12"].sum(axis = 1)
        #quarter_data.sort_values(["State", "RegionName"], inplace = True)
    return quarter_data.set_index(["State","RegionName"])


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    
    ## reading the data values    
    data_uni = get_list_of_university_towns()

    data_uni = pd.merge(data_uni, convert_housing_data_to_quarters(), how='outer', right_index=True, left_on=['State', 'RegionName'], indicator=True)
    
    ## separating values
    data_housing = data_uni[data_uni.loc[:,"_merge"] != "left_only" ].copy()
    data_uni = data_uni[data_uni.loc[:,"_merge"] != "right_only" ]
    
    ## getting only recession start values
    data_rec_uni = data_uni.loc[:,get_recession_start()].dropna()
    data_rec_house = data_housing.loc[:,get_recession_start()].dropna()

    return stats.ttest_ind(data_rec_uni,data_rec_house, equal_var = False)

if __name__ == "__main__" :
    print(run_ttest())

