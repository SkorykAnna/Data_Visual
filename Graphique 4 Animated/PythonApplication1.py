import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches

# Define colors
MEDIUM_BLUE = '#0000CD'
ORANGE = '#F8AD07'
LIGHT_ORANGE = '#ffd485'
GREEN = '#008000'
NAVY = '#000080'
CORN_FLOWER_BLUE = '#6495ED'
LIGHT_GREY = '#D3D3D3'
DIM_GREY = 'dimgrey'

# Data for plotting
data_employees = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    'Females': [10.7, 11.2, 11.7, 7.8, 6.8, 7.2, 6.9, 6.4, 6.5, 6.4, 16.3, 17.2, 12.0],
    'Males': [5.8, 6.0, 6.2, 2.7, 2.6, 2.8, 2.9, 3.0, 3.1, 3.1, 12.7, 14.0, 8.9]
}

# Create a DataFrame for employees data
df_employees = pd.DataFrame(data_employees)

# Normalize Females data
norm_females = (df_employees['Females'] - df_employees['Females'].min()) / (
    df_employees['Females'].max() - df_employees['Females'].min())

# Normalize Males data
norm_males = (df_employees['Males'] - df_employees['Males'].min()) / (
    df_employees['Males'].max() - df_employees['Males'].min())

# Set color for scatter points
colors_females = [ORANGE if year >= 2017 else DIM_GREY for year in df_employees['Year']]  # Updated here
colors_males = [CORN_FLOWER_BLUE if year >= 2017 else DIM_GREY for year in df_employees['Year']]  # Updated here


# Create custom legend handles
female_patch = mpatches.Patch(color=ORANGE, label='Females')
male_patch = mpatches.Patch(color=CORN_FLOWER_BLUE, label='Males')

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Set frame and axes color
ax.spines['top'].set_color('gray')
ax.spines['bottom'].set_color('gray')
ax.spines['left'].set_color('gray')
ax.spines['right'].set_color('gray')

ax.tick_params(axis='x', colors=DIM_GREY)
ax.tick_params(axis='y', colors=DIM_GREY)

# Set table title color
ax.title.set_color(DIM_GREY)
ax.title.set_multialignment('center')  # Set the title to center alignment

# Initialize scatter plots with empty data
scatter_females = ax.scatter([], [], alpha=0.5, color=colors_females[:1], s=0)  # Updated here
scatter_males = ax.scatter([], [], alpha=0.5, color=colors_males[:1], s=0)  # Updated here


# Update function for the animation
def update(frame):
    # Update scatter plot data
    scatter_females.set_offsets(df_employees.loc[:frame, ['Year', 'Females']].values)
    scatter_males.set_offsets(df_employees.loc[:frame, ['Year', 'Males']].values)

    # Update scatter plot sizes
    scatter_females.set_sizes((norm_females[:frame] * 2000 + 10).tolist())
    scatter_males.set_sizes((norm_males[:frame] * 2000 + 10).tolist())

    # Update scatter plot colors for the years 2017-2022
    scatter_females.set_color(colors_females[:frame + 1])
    scatter_males.set_color(colors_males[:frame + 1])

    return scatter_females, scatter_males


# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(df_employees), interval=500, blit=True)

# Plotting
df_employees.loc[df_employees['Year'] <= 2017].plot(
    kind='line', x='Year', y='Females', linestyle='--', color=LIGHT_GREY, ax=ax)
df_employees.loc[df_employees['Year'] <= 2017].plot(
    kind='line', x='Year', y='Males', linestyle='--', color=LIGHT_GREY, ax=ax)
df_employees.loc[df_employees['Year'] >= 2017].plot(
    kind='line', x='Year', y='Females', linestyle='--', color=ORANGE, ax=ax)
df_employees.loc[df_employees['Year'] >= 2017].plot(
    kind='line', x='Year', y='Males', linestyle='--', color=CORN_FLOWER_BLUE, ax=ax)

ax.set_xlabel('Year', color=DIM_GREY)
ax.set_ylabel('Percentage', color=DIM_GREY)
ax.set_title('Percentage of employees working from home as a percentage\n of the total employment in France (2010-2022) by sex',
             fontweight='bold', color=DIM_GREY)
ax.legend(handles=[female_patch, male_patch], loc='upper left', fontsize='x-large', labelcolor=DIM_GREY)

# Add value labels to scatter points
for i, row in df_employees.iterrows():
    if row['Year'] == 2020:
        ax.text(row['Year'] - 0.2, row['Females'] - 1.5, f"{row['Females']}%",
                 color=colors_females[i], ha='right', va='top', fontsize='small')
        ax.text(row['Year'] + 0.2, row['Males'] - 1.5, f"{row['Males']}%",
                 color=colors_males[i], ha='left', va='top', fontsize='small')
    else:
        if row['Year'] >= 2020:
            y_offset = -2
        else:
            y_offset = 1
        ax.text(row['Year'], row['Females'] + y_offset, f"{row['Females']}%",
                 color=colors_females[i], ha='center', va='bottom', fontsize='small')
        ax.text(row['Year'], row['Males'] + y_offset, f"{row['Males']}%",
                 color=colors_males[i], ha='center', va='bottom', fontsize='small')

plt.show()
