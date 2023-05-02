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
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import seaborn as sns
from datetime import datetime

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
Activity_data['Phase'] = 0

def assign_phase(activity_date):
    phase_dates = [
        (20200615, 20200913),
        (20200914, 20201201),
        (20201202, 20210105),
        (20210106, 20210307),
        (20210308, 20210718),
        (20210719, 20211207),
        (20211208, 20220316),
    ]

    for i, (start_date, end_date) in enumerate(phase_dates):
        if activity_date >= start_date and activity_date <= end_date:
            return i + 1
    return 0

# Assign phases using the 'assign_phase' function
Activity_data['Phase'] = Activity_data['Date'].apply(assign_phase)

#Line chart



# Assuming your DataFrame is named 'df'
# Make a copy of the DataFrame
df_copy = Activity_data.copy()

# Ensure that the 'Date' column in the copied DataFrame is in datetime format
df_copy['Date'] = pd.to_datetime(df_copy['Date'], format='%Y%m%d')

# Aggregate the data by week and count the number of activities for each week
df_copy['Week'] = df_copy['Date'].dt.to_period('W').dt.to_timestamp()
df_agg = df_copy.groupby('Week').size().reset_index(name='activity_count')

# Define the phase dates
phase_dates = [
    ('20200615', '20200913'),
    ('20200914', '20201201'),
    ('20201202', '20210105'),
    ('20210106', '20210307'),
    ('20210308', '20210718'),
    ('20210719', '20211207'),
    ('20211208', '20220316')
]

# Convert phase dates to datetime format
phase_dates = [(pd.to_datetime(start, format='%Y%m%d'), pd.to_datetime(end, format='%Y%m%d')) for start, end in phase_dates]

# Generate color list using YlGn colormap from seaborn
color_list = sns.color_palette("YlGn", n_colors=len(phase_dates))

# Generate colormap using YlGn
# cmap = mcolors.LinearSegmentedColormap.from_list("", ["#ffffcc", "#1a9641"])
# color_list = [cmap(i) for i in range(len(phase_dates))]

fig, ax = plt.subplots(figsize=(10, 6))

# Plot the line chart for activity counts
ax.plot(df_agg['Week'], df_agg['activity_count'], label='Activity Count', linewidth=2)

# Color the background based on the phases
for (start, end), color in zip(phase_dates, color_list):
    ax.axvspan(start, end, color=color, alpha=0.3)

# Set the x-axis to display dates with custom tick locations and formatting
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

# Set x-axis limits to start at the first phase and end at the last phase
ax.set_xlim(phase_dates[0][0], phase_dates[-1][1])

# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Activity Count (Weekly)')
ax.set_title('Activity recorded during 7 Phases')

# Display the legend
ax.legend()

plt.tight_layout()
plt.show()
plt.savefig("activity_chart.png", dpi=300)

# Bar chart by activity and categories
# Create 3405; Other 2270; Social 2163; Home 1598; Sports 1255; Work 1206
Activity_data['category'].value_counts() 
top_75_act = Activity_data['type'].value_counts()[0:75]     #Top 75 

# Count  
'''
A bar chart that 1) one bar to one phase (7 phases in total), 2) each bar has 
different section, each section's width shows its frequency during the phases,
3) the color of the bar varies according to the mode of 
'''


























