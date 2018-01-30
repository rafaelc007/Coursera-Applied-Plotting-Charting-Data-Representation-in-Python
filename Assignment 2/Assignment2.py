
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[3]:

import pandas as pd

data = pd.read_csv("data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv")
## reorganizing data
data.sort_values(["Date","ID"], inplace = True)
## adjusting data
data["Data_Value"] *= 0.1
## visualizing the data
data.set_index(["Date","ID", "Element"]).head(10)


# In[91]:

'''Once the data has been loaded... (ops)'''

## separate data
data1 = data.set_index("Date").loc[:"2014-12-31"].reset_index().copy()
data2 = data.set_index("Date").loc["2015-01-01":].reset_index().copy()


## create nem shapped dataframe
n_data = pd.DataFrame()
n_data["Day"] = list(map(lambda x: x[-5:],pd.date_range(start = "01/01/2005", end = "31/12/2005").astype('str')))
n_data["Tmin"] = [1000]*n_data.shape[0]
n_data["Tmax"] = [-277]*n_data.shape[0]
n_data.set_index("Day", inplace = True)

for date, frame in data1.groupby("Date"):
    try:
        ## get min and max values
        n_data.loc[date[-5:], "Tmin"] = min([min(frame["Data_Value"].values), n_data.loc[date[-5:], "Tmin"]])
        n_data.loc[date[-5:], "Tmax"] = max([max(frame["Data_Value"].values), n_data.loc[date[-5:], "Tmax"]])
    except KeyError:
        ## in case day 02-29 appear
        continue
    
n_data.reset_index(inplace = True)   
Rec_temp = n_data.loc[:,["Tmin", "Tmax"]].values
Rec_dates = n_data.loc[:,"Day"].values


# In[110]:

'''Now organizing data from 2015'''

## create nem shapped dataframe
n_data["Tmin 2015"] = [1000]*n_data.shape[0]
n_data["Tmax 2015"] = [-277]*n_data.shape[0]
n_data.set_index("Day", inplace = True)

for date, frame in data2.groupby("Date"):
    ## get min and max values
    n_data.loc[date[-5:], "Tmin 2015"] = min([min(frame["Data_Value"].values), n_data.loc[date[-5:], "Tmin"]])
    n_data.loc[date[-5:], "Tmax 2015"] = max([max(frame["Data_Value"].values), n_data.loc[date[-5:], "Tmax"]])
 
n_data.reset_index(inplace = True)   
Rec_temp2_min = n_data.loc[n_data["Tmin 2015"] < n_data["Tmin"],"Tmin 2015"].values
Rec_temp2_max = n_data.loc[n_data["Tmax 2015"] > n_data["Tmax"],"Tmax 2015"].values

Rec_dates2_min = n_data.loc[n_data["Tmin 2015"] < n_data["Tmin"],"Tmin 2015"].index
Rec_dates2_max = n_data.loc[n_data["Tmax 2015"] > n_data["Tmax"],"Tmax 2015"].index


# In[82]:

'''Once the data is selected'''
get_ipython().magic('matplotlib notebook')
import matplotlib.pyplot as plt

colors = ["blue", "red"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

plt.figure(1)
for i in range(2):
    ## ploting data
    plt.plot(Rec_temp[:,i], '-', color = colors[i], alpha = 0.8)
    
## add dates to the xticks labels
plt.xticks(range(0,len(Rec_dates),31), months, ha='left', rotation = 0)
    
## set title
plt.title("Maximum and Minimum temperatures per date from 2005 to 2014")
## remove the frame of the chart
for spine in plt.gca().spines.values():
    spine.set_visible(False)

## remove all the ticks (both axes), and tick labels on the Y axis
plt.tick_params(top='off', bottom='off', left='off', right='off', labelbottom='on')

# fill the area between the linear data and exponential data
plt.gca().fill_between(range(len(Rec_temp[:,0])), 
                       Rec_temp[:,0], Rec_temp[:,1], 
                       facecolor='gray', 
                       alpha=0.25)

plt.gca().yaxis.grid(True)
lim_val = np.max(np.abs(Rec_temp))+10
plt.axis([-0.1, len(Rec_dates)+0.1, -lim_val, lim_val])

# adjust the subplot so the text doesn't run off the image
plt.subplots_adjust(bottom=0.25)

plt.show()


# In[112]:

'''Now with the 2015 data'''
get_ipython().magic('matplotlib notebook')
import matplotlib.pyplot as plt

colors = ["blue", "red"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

plt.figure(1)
for i in range(2):
    ## ploting data
    plt.plot(Rec_temp[:,i], '-', color = colors[i], alpha = 0.8)
    
## add dates to the xticks labels
plt.xticks(range(0,len(Rec_dates),31), months, ha='left', rotation = 0)
    
## set title
plt.title("Maximum and Minimum temperatures per date from 2005 to 2014")

## remove the frame of the chart
for spine in plt.gca().spines.values():
    spine.set_visible(False)

## remove all the ticks (both axes), and tick labels on the Y axis
plt.tick_params(top='off', bottom='off', left='off', right='off', labelbottom='on')

# fill the area between the linear data and exponential data
plt.gca().fill_between(range(len(Rec_temp[:,0])), 
                       Rec_temp[:,0], Rec_temp[:,1], 
                       facecolor='gray', 
                       alpha=0.25)

plt.gca().yaxis.grid(True)
lim_val = np.max(np.abs(Rec_temp))+10
plt.axis([-0.1, len(Rec_dates)+0.1, -lim_val, lim_val])

# adjust the subplot so the text doesn't run off the image
plt.subplots_adjust(bottom=0.25)

plt.scatter(Rec_dates2_min, Rec_temp2_min)
plt.scatter(Rec_dates2_max, Rec_temp2_max)

plt.show()


# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[ ]:



