
# coding: utf-8

# # Assignment 3 - Building a Custom Visualization
# 
# ---
# 
# In this assignment you must choose one of the options presented below and submit a visual as well as your source code for peer grading. The details of how you solve the assignment are up to you, although your assignment must use matplotlib so that your peers can evaluate your work. The options differ in challenge level, but there are no grades associated with the challenge level you chose. However, your peers will be asked to ensure you at least met a minimum quality for a given technique in order to pass. Implement the technique fully (or exceed it!) and you should be able to earn full grades for the assignment.
# 
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ferreira, N., Fisher, D., & Konig, A. C. (2014, April). [Sample-oriented task-driven visualizations: allowing users to make better, more confident decisions.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 571-580). ACM. ([video](https://www.youtube.com/watch?v=BI7GAs-va-Q))
# 
# 
# In this [paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) the authors describe the challenges users face when trying to make judgements about probabilistic data generated through samples. As an example, they look at a bar chart of four years of data (replicated below in Figure 1). Each year has a y-axis value, which is derived from a sample of a larger dataset. For instance, the first value might be the number votes in a given district or riding for 1992, with the average being around 33,000. On top of this is plotted the 95% confidence interval for the mean (see the boxplot lectures for more information, and the yerr parameter of barcharts).
# 
# <br>
# <img src="readonly/Assignment3Fig1.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Figure 1 from (Ferreira et al, 2014).</h4>
# 
# <br>
# 
# A challenge that users face is that, for a given y-axis value (e.g. 42,000), it is difficult to know which x-axis values are most likely to be representative, because the confidence levels overlap and their distributions are different (the lengths of the confidence interval bars are unequal). One of the solutions the authors propose for this problem (Figure 2c) is to allow users to indicate the y-axis value of interest (e.g. 42,000) and then draw a horizontal line and color bars based on this value. So bars might be colored red if they are definitely above this value (given the confidence interval), blue if they are definitely below this value, or white if they contain this value.
# 
# 
# <br>
# <img src="readonly/Assignment3Fig2c.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  Figure 2c from (Ferreira et al. 2014). Note that the colorbar legend at the bottom as well as the arrows are not required in the assignment descriptions below.</h4>
# 
# <br>
# <br>
# 
# **Easiest option:** Implement the bar coloring as described above - a color scale with only three colors, (e.g. blue, white, and red). Assume the user provides the y axis value of interest as a parameter or variable.
# 
# 
# **Harder option:** Implement the bar coloring as described in the paper, where the color of the bar is actually based on the amount of data covered (e.g. a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained, to dark red if the value is certainly not contained as the distribution is above the axis).
# 
# **Even Harder option:** Add interactivity to the above, which allows the user to click on the y axis to set the value of interest. The bar colors should change with respect to what value the user has selected.
# 
# **Hardest option:** Allow the user to interactively set a range of y values they are interested in, and recolor based on this (e.g. a y-axis band, see the paper for more details).
# 
# ---
# 
# *Note: The data given for this assignment is not the same as the data used in the article and as a result the visualizations may look a little different.*

# In[45]:

# Use the following data for this assignment:

import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

dfStat = df.T.describe()

dfStat


# In[58]:

'''Plotting the chart bar graph'''
get_ipython().magic('matplotlib notebook')

import matplotlib.pyplot as plt

yerr = 1.96 * dfStat.T['std'] / np.sqrt(dfStat.T['count'])

plt.figure()
plt.bar(np.arange(1,5),df.mean(1), yerr = yerr)
plt.xticks(np.arange(1,5), map(str,df.index))

## remove the frame of the chart
for spine in plt.gca().spines.values():
    spine.set_visible(False)

## remove all the ticks (both axes), and tick labels on the Y axis
plt.tick_params(top='off', bottom='off', left='on', right='off', labelbottom='on')

## putting a horizontal grid
#plt.gca().yaxis.grid(True)

plt.show()


# In[86]:

def get_color(pos, n_mean, error):    
    ## intensities
    dist = [pos]*len(m_val)-m_val
    norm = matplotlib.colors.Normalize(vmin=min(abs(dist)), vmax=max(abs(dist)))
    
    colors = list()
    for (d,err) in zip(dist,yerr):
        if d<0:
            ## define colors
            cmap = plt.cm.Reds
        if d>=0:
            ## define colors
            cmap = plt.cm.Blues
        colors.append(cmap(norm(abs(d))))
            
    return colors
        
            


# In[115]:

'''colouring the graph according to a given value'''
get_ipython().magic('matplotlib notebook')

## value given by the user
given = 40000
x_val = np.arange(1,5)
import matplotlib.pyplot as plt

## calculate means
m_val = df.mean(1)

## calculate 95% percentile
yerr = 1.96 * dfStat.T['std'] / np.sqrt(dfStat.T['count'])

## plot bar graph of the data
plt.figure()
plt.bar(x_val, m_val, yerr = yerr, color=get_color(given, m_val,yerr))
plt.xticks(x_val, map(str,df.index))

## plot horizontal line for the chosen value
plt.plot(np.arange(0,6), [given]*6, 'r')
plt.annotate('y: {}'.format(given), [4.5, given+1000])

## restrain axis visuaization
plt.axis([0, 5.5, 0, 55000])

## remove the frame of the chart
for spine in plt.gca().spines.values():
    spine.set_visible(False)

## remove all the ticks (both axes), and tick labels on the Y axis
plt.tick_params(top='off', bottom='off', left='on', right='off', labelbottom='on')

## putting a horizontal grid
#plt.gca().yaxis.grid(True)

plt.show()


# In[112]:

'''colouring the graph according to a value captured via interaction'''
get_ipython().magic('matplotlib notebook')

## value given by the user
given = 39000
x_val = np.arange(1,5)
import matplotlib.pyplot as plt

## calculate means
m_val = df.mean(1)

## calculate 95% percentile
yerr = 1.96 * dfStat.T['std'] / np.sqrt(dfStat.T['count'])

## plot bar graph of the data
plt.figure()
plt.bar(x_val, m_val, yerr = yerr, color=get_color(given, m_val,yerr), picker = True)
plt.xticks(x_val, map(str,df.index))

## restrain axis visuaization
plt.axis([0, 5.5, 0, 55000])

## remove the frame of the chart
for spine in plt.gca().spines.values():
    spine.set_visible(False)

## remove all the ticks (both axes), and tick labels on the Y axis
plt.tick_params(top='off', bottom='off', left='on', right='off', labelbottom='on')

## putting a horizontal grid
#plt.gca().yaxis.grid(True)

plt.show()

## pick the event
def onpick(event):
    line = event.artist
    ydata = line.get_ydata()
    ind = event.ind
    ## plot horizontal line for the chosen value
    #plt.plot(np.arange(0,6), [given]*6, 'r')
    #plt.annotate('y: {}'.format(given), [4.5, given+1000])
    plt.gca().set_title('Selected item came from {}'.format(ydata[ind]))
    
plt.gcf().canvas.mpl_connect('pick_event', onpick)


# In[111]:

fig = plt.figure()
ax = plt.plot(np.random.rand(100), 'o', picker=5)  # 5 points tolerance
plt.show()

def on_pick(event):
    line = event.artist
    xdata, ydata = line.get_data()
    ind = event.ind
    plt.gca().set_title('Selected item came from {}'.format(ydata[ind]))

cid = fig.canvas.mpl_connect('pick_event', on_pick)


# In[108]:




# In[ ]:



