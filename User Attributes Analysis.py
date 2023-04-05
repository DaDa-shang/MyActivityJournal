#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 17:10:07 2023

@author: root
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython import display 
display.set_matplotlib_formats('svg')

# Read csv datafile and check the dataframe
Users_data = pd.read_csv('/Users/shangziyue/Desktop/IRDR dPHE Project/Journal App Data/Users.csv')
test = Users_data.head()

Users_data.shape  # data size
Users_data.dtypes # data type
Users_data.describe() #describe the data mean/counts/std/min/max

# Count the age range
Age_range = Users_data.groupby('ageRange')['_id'].count().reset_index().rename(columns={'_id':'num'})
Age_range.drop([2], axis=0, inplace=True)
Age_range.drop([7], axis=0, inplace=True)
Age_range.ageRange[6]= 65
Age_range.ageRange[0]= 18
Age_range.ageRange[1]= 25
Age_range.ageRange[3]= 35
Age_range.ageRange[4]= 45
Age_range.ageRange[5]= 55
int(Age_range['ageRange'])

# Categrise the age range, 18-24, 25-34, 35-44, 45-54, 55-64
bins = [18,25,35,45,55,65,80]
group = ['18-24', '25-34', '35-44', '45-54', '55-64', '65']
Age_range['age_group'] = pd.cut(Age_range['ageRange'], bins, labels=group, right=False)
age_dist = Age_range.groupby('age_group')['num'].sum().reset_index()
age_dist

plt.bar(age_dist['age_group'],age_dist['num'])
plt.title('Users Age Distribution')
plt.xlabel('Age Range')
plt.ylabel('Group Size')



