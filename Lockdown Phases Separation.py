#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 20:09:21 2023

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

# Separate dates into 8 phases
# Phase 1: 20200615 - 20200913; Phase 2: 20200914 - 20201201
# Phase 3: 20201202 - 20210105; Phase 4: 20210106 - 20210307
# Phase 5: 20210308 - 20210718; Phase 6: 20210719 - 20211207
# Phase 7: 20211208 - 20220316
# Ease of First Lockdown; Second Lockdown; Ease of Second Lockdown; Third Lockdown
# Stepwise ease of 3rd Lockdown; Freeday; Omicron




















