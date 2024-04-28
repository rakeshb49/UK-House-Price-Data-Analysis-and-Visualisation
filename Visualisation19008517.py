import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates

# Load the dataset
data = pd.read_csv('uk_hpi_pp2.csv')
# Convert 'Date' to datetime
data['Date'] = pd.to_datetime(data['Date'])
data['Year'] = data['Date'].dt.year

##################### Bar Chart #####################################
# Bar Plot of Average Prices by Region (Top 10) across all regions
plt.figure(figsize=(10, 8), facecolor='white')
region_prices = data.groupby('RegionName')['AveragePrice'].mean().sort_values(ascending=False).head(10)
region_prices.plot(kind='barh', color='skyblue')
plt.title('Top 10 Regions by Average Property Prices')
plt.xlabel('Average Property Price (£)')
plt.ylabel('Region Name')
plt.tight_layout()
plt.show()

# Filter for UK data only
uk_data = data[data['RegionName'] == 'United Kingdom'].copy()
# Convert 'Date' from datetime to a numeric format for plotting
uk_data['Date_num'] = mdates.date2num(uk_data['Date'])

# Functions for formatting the axis
def millions_formatter(x, pos):
    return f'£{int(x / 1e6)}M'

def hundtho_formatter(x, pos):
    return f'£{int(x / 1e3)}k'

# Style settings
sns.set(style="whitegrid")
plt.rc('grid', linestyle="--", color='grey', linewidth=0.7)

##################### Hexbin Density Plot ###########################
# Hexbin Plot of Average Price Changes Over Time for UK data
plt.figure(figsize=(14, 7), facecolor='white')
hb = plt.hexbin(uk_data['Date_num'], uk_data['AveragePrice'], gridsize=50, cmap='Blues', bins='log', mincnt=1)
cb = plt.colorbar(hb, spacing='proportional')
cb.set_label('log10(N)')
plt.gca().set_facecolor('whitesmoke')
plt.gca().yaxis.set_major_formatter(FuncFormatter(hundtho_formatter))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.title('Density of Average Property Prices Over Time in the UK')
plt.xlabel('Date (Year)')
plt.ylabel('Average Property Price (£100k)')
plt.tight_layout()
plt.show()

##################### Violin Plot ###################################
# Prepare property data for violin plots
property_types = ['DetachedPrice', 'SemiDetachedPrice', 'TerracedPrice', 'FlatPrice']
uk_property_data = pd.melt(uk_data, id_vars=['Date', 'Year'], value_vars=property_types, var_name='PropertyType', value_name='Price')
uk_property_data['PropertyType'] = uk_property_data['PropertyType'].str.replace('Price', '')
# Violin Plot for Each Property Type Prices
plt.figure(figsize=(12, 8), facecolor='white')
sns.violinplot(x='PropertyType', y='Price', data=uk_property_data, cut=0)
plt.gca().set_facecolor('whitesmoke')
plt.gca().yaxis.set_major_formatter(FuncFormatter(hundtho_formatter))
plt.title('Price Distribution by Property Type in the UK')
plt.xlabel('Property Type')
plt.ylabel('Property Price (£)')
plt.show()

###################### Line PLot ####################################
# Filter for UK data only and for years 2005 onwards
uk_data_from_2005 = data[(data['RegionName'] == 'United Kingdom') & (data['Year'] >= 2005)].copy()
uk_data_from_2005['Year'] = uk_data_from_2005['Date'].dt.year  # Extract the year from the 'Date' column
# Group by 'Year' and sum the 'SalesVolume'
annual_sales_volume_sum = uk_data_from_2005.groupby('Year')['SalesVolume'].sum().reset_index()
# Now plot using the 'Year' for the x-axis
plt.figure(figsize=(16, 7))
ax = plt.gca()
ax.set_facecolor('whitesmoke')
ax.yaxis.set_major_formatter(FuncFormatter(hundtho_formatter))  # Apply the hundreds of thousands formatter
ax.plot(annual_sales_volume_sum['Year'], annual_sales_volume_sum['SalesVolume'], marker='o', linestyle='-')
ax.set_title('Annual Sales Volume in the UK (2005 Onwards)')
ax.set_xlabel('Year')
ax.set_ylabel('Total Sales Volume (in £100k)')
ax.set_xticks(annual_sales_volume_sum['Year'])  # Ensure every year is shown on the x-axis
ax.tick_params(axis='x', rotation=45)  # Rotate the x-axis labels for better readability
plt.tight_layout()  # Adjust the layout
plt.show()
