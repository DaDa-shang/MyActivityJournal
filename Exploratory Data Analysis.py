#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 19:52:10 2023

@author: root
"""

# Import Packages for Data-analysis and visualisation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython import display 
display.set_matplotlib_formats('svg')

# Read csv datafile and check the dataframe
activities_data = pd.read_csv('/Users/shangziyue/Desktop/IRDR dPHE Project/Journal App Data/activities.csv')
test = activities_data.head()

activities_data.shape  # data size
activities_data.dtypes # data type
activities_data.describe() #describe the data mean/counts/std/min/max

# Convert date and time information into str object and delete all str will not be used
time = ['createdAt']
for c in time:
    activities_data[c] = activities_data[c].replace(
        r'[-, :, ., T, Z]', '', regex=True).astype(str)

# Create empty dataframe
activities_data['Year'], activities_data['Month'], activities_data['Day'], activities_data['Hour'], activities_data['Date'] = [0, 0, 0, 0, 0]

# Seprate date information into Year, Month, Day, Hour
activities_data['Year'] = activities_data['createdAt'].str[0:4]
activities_data['Month'] = activities_data['createdAt'].str[4:6]
activities_data['Day'] = activities_data['createdAt'].str[6:8]
activities_data['Hour'] = activities_data['createdAt'].str[8:10]
activities_data['Date'] = activities_data['createdAt'].str[0:8]

# Drop useless column
# Activity_data = activities_data.drop('date', axis=1)
Activity_data = activities_data.drop('createdAt', axis=1)
Activity_data = Activity_data.drop('__v', axis=1)

Activity_data['Year'] = pd.to_numeric(Activity_data['Year'], errors='coerce')
Activity_data['Month'] = pd.to_numeric(Activity_data['Month'], errors='coerce')
Activity_data['Day'] = pd.to_numeric(Activity_data['Day'], errors='coerce')
Activity_data['Hour'] = pd.to_numeric(Activity_data['Hour'], errors='coerce')
Activity_data['Date'] = pd.to_numeric(Activity_data['Date'], errors='coerce')

Activity_data.describe()
Activity_data.dtypes
test1 = Activity_data.head()

# Histogram of Month and Hour
ax = sns.histplot(Activity_data['Month'])
ax.set_xlim([1,12])
ax.set_xticks(range(1,12))
ax.set_xticklabels(['%.0e'%a for a in 10**ax.get_ticks()]);

ax = sns.histplot(Activity_data['Hour'])
# Very Strange!!! 

# Different Catergories and Types of activities
Activity_data['category'].value_counts()
Activity_data['type'].value_counts()[0:20]     #Top 20 
Activity_data['type'].value_counts()[450:461]  #Last 15

# Data Cleaning ideas
#   1. Put activities into 3 or more phases by Date, and give each activities a number feature to show the phases
#   2. Input the User information into the datasheet (Age, Gender, Country, City) 


# Visualisation ideas
#   1. Catergories and types of activity rating distribution in different phases (Phase 1,2,3)
#   2. Activities counts distribution over the year and among the day
#   3. Different types rating comparison 
#   4. Correlations between some features (for instance, rating vs frequency/counts, others include age)
#   5. Geographic distribution inside UK and abroad to do compare 

# Draft visualisation
# Catergory and types of activity counts against time/ratings
category = Activity_data['category'].isin(['Create', 'Other', 'Social', 'Home', 'Sports', 'Work'])
sns.displot(pd.DataFrame({'Date': Activity_data[category]['Date'],
                          'Category': Activity_data[category]['category']}),
            x='Date', hue='Category', kind='kde')

# Catergory and types of activity counts against ratings
sns.displot(pd.DataFrame({'Rating': Activity_data['rating'],
                          'Category': Activity_data['category']}),
            x='Rating', hue='Category', kind='hist')

ax2 = sns.boxplot(x=Activity_data['rating'],y=Activity_data['category'], data=Activity_data['category'])

# Compare rating
Com = Activity_data[Activity_data['type'].isin(
    Activity_data['type'].value_counts()[:20].keys())]
ax3 = sns.boxplot(x='type', y='rating', data=Com)
ax3.set_ylim([0,5])
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90);

# Further Data Analysis
#   1. Statistical Test between different nuemerical/binary features (Age, Gender, Location 
#   Activities categories/Types, Ratings, COVID-19 phases, activities counts/frequencies, Time)
#   2. Text/NLP analysis of comments and follow-up questions


Comment_data = activities_data.dropna(subset=['commentBox'])
Comment_data.describe()






