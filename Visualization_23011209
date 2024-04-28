# importing relevant libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Loading the CSV data into a DataFrame
df = pd.read_csv('uk_hpi_pp2.csv')

############################# Comparative Bar CHart ######################################

# Converting relevant columns to numeric data types
numeric_columns = ['DetachedPrice', 'SemiDetachedPrice', 'TerracedPrice', 'FlatPrice']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Dropping rows with missing values in numeric columns
df.dropna(subset=numeric_columns, inplace=True)

# Filtering the DataFrame to include only the specified regions
regions_to_include = ['Stafford', 'Staffordshire', 'Stoke-on-Trent']
df = df[df['RegionName'].isin(regions_to_include)]

# Grouping the data by region ID and calculate the average prices for each house type
avg_prices = df.groupby('RegionName')[numeric_columns].mean()

# Reseting index to make 'RegionID' a column again
avg_prices.reset_index(inplace=True)

# Merging with original region names
avg_prices = avg_prices.merge(df[[ 'RegionName']], how='left')

# Melting the DataFrame to long format for easier plotting
melted_df = pd.melt(avg_prices, id_vars=['RegionName'], var_name='HouseType', value_name='AveragePrice')

# Defining custom colors for the bars
custom_palette = ['#534666', '#138086', '#cd7672', '#ffba32']

# Plotting using Seaborn with custom palette
plt.figure(figsize=(12, 6))
sns.barplot(data=melted_df, x='RegionName', y='AveragePrice', hue='HouseType', palette=custom_palette)

plt.title('Average House Prices by Type and Region')
plt.xlabel('Region')
plt.ylabel('Average Price (£)')
plt.xticks(rotation=90)  # Rotating x-axis labels for better readability
plt.tight_layout()
plt.show()

######################################### Stacked Column #####################################

# Converting Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%d-%m')

# Calculating the average old and new sales volume for each month
df['Month'] = df['Date'].dt.month
avg_sales = df.groupby('Month')[['OldSalesVolume', 'NewSalesVolume']].mean().reset_index()

# Plotting using Seaborn as a stacked column chart
plt.figure(figsize=(12, 6))
sns.barplot(data=avg_sales, x='Month', y='OldSalesVolume', color='#b1e4e3', label='Old Sales Volume')
sns.barplot(data=avg_sales, x='Month', y='NewSalesVolume', color='#2e008b', label='New Sales Volume')

plt.title('Average Monthly Old and New Sales Volume')
plt.xlabel('Month')
plt.ylabel('Average Volume')
plt.xticks(range(0, 12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])  # Customize x-axis labels
plt.legend(title='Sale Type', loc='upper left')
plt.tight_layout()
plt.show()

######################################## Scatter Plot ####################################################

# Filtering the DataFrame to include only the specified regions
regions_to_include = ['Stafford', 'Staffordshire', 'Stoke-on-Trent', 'Dudley', 'Newcastle-under-Lyme']
filtered_df = df[df['RegionName'].isin(regions_to_include)]

# Defining custom colors for the bars
custom_palette = ['#534666', '#138086', '#cd7672', '#0072ce', '#89813d', '#4ec3e0']

# Plotting the scatter plot using Seaborn
plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered_df, x='AveragePrice', y='SalesVolume', hue='RegionName', palette=custom_palette)

plt.title('Average Price vs. Sales Volume')
plt.xlabel('Average Price')
plt.ylabel('Sales Volume')
plt.grid(True)
plt.legend(title='Region')
plt.tight_layout()
plt.show()

######################################### Stacked Area Chart ###############################################

# Converting Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Filtering the DataFrame to include only Stafford and the years 2004 to 2023
filtered_df = df[(df['RegionName'] == 'Stafford') & (df['Date'].dt.year >= 2004) & (df['Date'].dt.year <= 2023)]

# Calculating the average NewPrice and OldPrice for each year
avg_prices = filtered_df.groupby(filtered_df['Date'].dt.year)[['NewPrice', 'OldPrice']].mean().reset_index()

# Converting the year column to integer
avg_prices['Date'] = avg_prices['Date'].astype(int)

# Plotting the lines for NewPrice and OldPrice
plt.figure(figsize=(10, 6))
sns.lineplot(data=avg_prices, x='Date', y='NewPrice', label='NewPrice', color='#cd7672')
sns.lineplot(data=avg_prices, x='Date', y='OldPrice', label='OldPrice', color='#534666')

# Filling the area below the NewPrice line
plt.fill_between(avg_prices['Date'], avg_prices['NewPrice'], color='#cd7672', alpha=0.4)

# Filling the area below the OldPrice line
plt.fill_between(avg_prices['Date'], avg_prices['OldPrice'], color='#534666', alpha=1.0)

plt.title('Average NewPrice and OldPrice in Stafford (2004-2023)')
plt.xlabel('Year')
plt.ylabel('Average Price')
plt.xticks(rotation=75)
plt.tight_layout()
plt.legend(title='Price Type')
plt.show()

############################# Apache Spark ######################################################

#importing relevant libraries
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("UK HPI Analysis") \
    .getOrCreate()

# Load CSV data into a DataFrame
df = spark.read.csv('uk_hpi_pp2.csv', header=True, inferSchema=True)

# Perform basic analysis (e.g., count rows, show schema)
df.show()
df.printSchema()

# Perform data aggregation or analysis using Spark DataFrame operations
# For example, calculate average prices by region or year
avg_prices_by_region = df.groupBy('RegionName').avg('AveragePrice')
avg_prices_by_region.show()

# Visualize the results using Matplotlib
avg_prices_by_region_df = avg_prices_by_region.toPandas()
plt.figure(figsize=(10, 6))
plt.bar(avg_prices_by_region_df['RegionName'], avg_prices_by_region_df['avg(AveragePrice)'])
plt.xlabel('Region')
plt.ylabel('Average Price')
plt.title('Average House Prices by Region')
plt.xticks(rotation=90)
plt.xticks(fontsize=5)
plt.tight_layout()
plt.show()

# Stop SparkSession
spark.stop()
