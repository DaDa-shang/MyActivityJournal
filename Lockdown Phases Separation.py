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
import ast
import json
import matplotlib.patches as mpatches

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
#
#
#
#

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

# Define the phase names
phase_names = [
    'Phase 1: Ease of First Lockdown',
    'Phase 2: Second Lockdown',
    'Phase 3: Ease of Second Lockdown',
    'Phase 4: Third Lockdown',
    'Phase 5: Stepwise ease of 3rd Lockdown',
    'Phase 6: Freeday',
    'Phase 7: Omicron'
]

# Create custom legend entries
custom_entries = [plt.Rectangle((0, 0), 1, 1, fc=color, alpha=0.3) for color in color_list]
custom_entries.append(plt.Line2D([0], [0], color='blue', lw=2))  # Add the line for the activity count

# Add the custom legend to the plot
ax.legend(custom_entries, phase_names + ['Activity Count'], loc='upper right')

plt.tight_layout()
plt.show()
plt.savefig("activity_chart.png", dpi=300)




# Bar chart by activity and categories
# Create&Chill 3405; Other 2270; Social&Caring 2163; Home&Shop 1598; Sports 1255; Work&Learn 1206
Activity_data['category'].value_counts() 
top_75_act = Activity_data['type'].value_counts()[0:75]     #Top 75 

# Count  
#
#



df = Activity_data.copy()

# Filter out rows with both 'followUpAnswers' answers undefined

'''
def filter_undefined_answers(x):
    x = json.loads(x)
    if len(x) < 2:
        return False
    if x[0] is None or x[1] is None:
        return False
    answer1 = x[0]['answer'].lower()
    answer2 = x[1]['answer'].lower()
    if "undefined" in answer1 or "undefined" in answer2:
        return False
    if any(keyword in answer1 for keyword in ['alone', 'online at home', 'on my own', 'online', 'at home', 'other location', 'tv', 'radio', 'social media', 'podcasts', 'other']) and \
       not any(keyword in answer1 for keyword in ['with others', 'at the gym', 'in public outside', 'in person', 'community delivery', 'at place of work', 'over the phone', 'virtually']):
        return True
    elif any(keyword in answer1 for keyword in ['with others', 'at the gym', 'in public outside', 'in person', 'community delivery', 'at place of work', 'over the phone', 'virtually']):
        return True
    else:
        return False

df_filtered = df[df['followUpAnswers'].apply(filter_undefined_answers)]



def extract_alone_or_with_others(answer):
    answer = ast.literal_eval(answer)
    alone_keywords = ['(alone)', 'online at home', 'on my own', 'online', 'at home', 'other location', 'tv', 'radio', 'social media', 'podcasts', 'other']
    with_others_keywords = ['(with others)', 'at the gym', 'in public outside', 'in person', 'community delivery', 'at place of work', 'over the phone', 'virtually']
    answer_text = answer[0]['answer'].lower()
    if any(keyword in answer_text for keyword in alone_keywords):
        return 'Alone'
    elif any(keyword in answer_text for keyword in with_others_keywords):
        return 'With Others'
    else:
        return 'Unidentified'

df_filtered['alone_or_with_others'] = df_filtered['followUpAnswers'].apply(extract_alone_or_with_others)

def extract_alone_or_with_others(answer):
    answer = ast.literal_eval(answer)
    if '(alone)' in answer[0]['answer'].lower():
        return 'Alone'
    elif '(with others)' in answer[0]['answer'].lower():
        return 'With Others'
    else:
        # look for parentheses and check for "alone" or "with others" inside
        re_result = re.search(r'\(([^)]+)\)', answer[0]['answer'])
        if re_result:
            if 'alone' in re_result.group(1).lower():
                return 'Alone'
            elif 'with others' in re_result.group(1).lower():
                return 'With Others'
        return 'Unidentified'
'''

def filter_undefined_answers(x):
    x = json.loads(x)
    if len(x) < 2:
        return False
    if x[0] is None or x[1] is None:
        return False
    answer1 = x[0]['answer'].lower()
    answer2 = x[1]['answer'].lower()
    if "undefined" in answer1 or "undefined" in answer2:
        return False
    if any(keyword in answer1 for keyword in ['(alone)', 'on my own', 'other location', 'tv', 'radio', 'social media', 'podcasts']):
        return True
    elif any(keyword in answer1 for keyword in ['(with others)', 'at the gym', 'in public outside', 'in person', 'community delivery', 'at place of work', 'over the phone']):
        return True
    else:
        return False

df_filtered = df[df['followUpAnswers'].apply(filter_undefined_answers)]

def extract_alone_or_with_others(answer):
    answer = ast.literal_eval(answer)
    alone_keywords = ['(alone)', 'on my own', 'other location', 'tv', 'radio', 'social media', 'podcasts']
    with_others_keywords = ['(with others)', 'at the gym', 'in public outside', 'in person', 'community delivery', 'at place of work', 'over the phone']
    answer_text = answer[0]['answer'].lower()
    if any(keyword in answer_text for keyword in alone_keywords):
        return 'Alone'
    elif any(keyword in answer_text for keyword in with_others_keywords):
        return 'With Others'
    else:
        return 'Unidentified'

df_filtered['alone_or_with_others'] = df_filtered['followUpAnswers'].apply(extract_alone_or_with_others)








# Extract 'alone' and 'with others' information from the first answer
#def extract_alone_or_with_others(answer):
#    answer = ast.literal_eval(answer)
#    if 'alone' in answer[0]['answer']:
#        return 'Alone'
#    elif 'with others' in answer[0]['answer']:
#       return 'With Others'
#    else:
#       return 'Unidentified'

# df_filtered['alone_or_with_others'] = df_filtered['followUpAnswers'].apply(extract_alone_or_with_others)


# Extract the second answer information
def extract_second_answer(answer):
    answer = ast.literal_eval(answer)
    if 'same amount' in answer[1]['answer']:
        return 'Same Amount'
    elif 'more often' in answer[1]['answer']:
        return 'More'
    elif 'less often' in answer[1]['answer']:
        return 'Less'
    elif 'not do this pre-lockdown' in answer[1]['answer']:
        return 'New Activity'
    else:
        return 'undefined'

df_filtered['second_answer'] = df_filtered['followUpAnswers'].apply(extract_second_answer)


# Create a pivot table with the proportion of samples by phase, category, second_answer, and alone_or_with_others
pivot_table = df_filtered.groupby(['Phase', 'category', 'second_answer', 'alone_or_with_others']).size().reset_index(name='count')
pivot_table['total'] = pivot_table.groupby(['Phase', 'category'])['count'].transform('sum')
pivot_table['proportion'] = pivot_table['count'] / pivot_table['total']

# Filter out the 'Other' category
pivot_table = pivot_table[pivot_table['category'] != 'Other']

# Set the categories order and the corresponding title names
categories_order = ['Create', 'Social', 'Home', 'Sports']
category_titles = ['Create&Chill', 'Social&Caring', 'Home&Shop', 'Sports', 'Work&Learn']

# Create a 2x3 canvas for the plots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Iterate over the categories and create a stacked bar chart for each one
for i, (category, ax) in enumerate(zip(categories_order, axes.flatten()[:-1])):
    # Filter the data for the current category
    category_data = pivot_table[pivot_table['category'] == category]

    # Create a stacked bar chart with the proportion of samples
    bar_width = 0.35
    bottoms = np.zeros(7)
    colors = ['gold', 'limegreen', 'lightgray']

    for alone_or_with_others, color in zip(['Alone', 'With Others', 'Unidentified'], colors):
        proportions = []

        for phase in range(1, 8):
            phase_proportions = category_data[(category_data['Phase'] == phase) & (category_data['alone_or_with_others'] == alone_or_with_others)]['proportion'].values
            proportions.append(phase_proportions[0] if len(phase_proportions) > 0 else 0)

        ax.bar(np.arange(1, 8), proportions, bar_width, bottom=bottoms, color=color, label=alone_or_with_others)
        bottoms += np.array(proportions)

    # Set plot title, labels and ticks
    ax.set_title(category_titles[i])
    ax.set_xlabel('Phases')
    ax.set_ylabel('Proportion of Samples')
    ax.set_xticks(np.arange(1, 8))
    ax.set_xticklabels([f'Phase {i}' for i in range(1, 8)])
    ax.set_ylim(0, 1)

# Create the legend in the top right plot
axes.flatten()[-1].legend(*axes[0, 0].get_legend_handles_labels(), title='Legend', loc='center')
axes.flatten()[-1].axis('off')

# Adjust the layout
plt.tight_layout()

# Save the figure
plt.savefig("stacked_bar_chart.png", dpi=300)

# Display the plot
plt.show()



df_filtered.to_csv('/Users/shangziyue/Desktop/IRDR dPHE Project/filtereddata.csv', sep='|', index=False)


df_filtered.to_excel('/Users/shangziyue/Desktop/IRDR dPHE Project/filtereddata.xlsx', index=False)






