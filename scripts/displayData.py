import numpy
import polars as pl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ExpSineSquared, RationalQuadratic, WhiteKernel

# Read the CSV file using Polars
df = pl.read_csv("data/transformed/transformed_parking_status.csv")

# Convert the date_time column to datetime type using the correct format
df = df.with_columns(pl.col("datetime").str.to_datetime())
#.strptime(pl.datetime, format="%Y-%m-%d %H:%M"))

# Sort the DataFrame by date_time (optional, but often useful)
df = df.sort("datetime")

# Extract the date_time and value columns
dates = df["datetime"].to_list()
southValues = df["south%"].to_list()
westValues = df["west%"].to_list()
northValues = df["north%"].to_list()
southCampusValues = df["southcampus%"].to_list()

# Plot the data using Matplotlib
#plt.figure(figsize=(10, 6))

# Scatter plot
#plt.scatter(dates, southValues, color='blue', label='south %')
#plt.scatter(dates, westValues, color='red', label='west %')
#plt.scatter(dates, northValues, color='yellow', label='north %')
#plt.scatter(dates, southCampusValues, color='green', label='south campus %')

# Line plot connecting the points
#plt.plot(dates, values, color='red', linestyle='-', marker='', label='Trend')
plt.plot(dates, southValues, color='blue', linestyle='-', marker='', label='south %')
plt.plot(dates, westValues, color='red', linestyle='-', marker='', label='west %')
plt.plot(dates, northValues, color='yellow', linestyle='-', marker='', label='north %')
plt.plot(dates, southCampusValues, color='green', linestyle='-', marker='', label='south campus %')

# Formatting the x-axis to show dates properly
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.gcf().autofmt_xdate()  # Rotation

# Labels and title
plt.xlabel('Date and Time')
plt.ylabel('Value out of 100')
plt.title('Scatter Plot with Connecting Line')
plt.legend()

# Show the plot
plt.show()

# remove weekends


# convert date to numpy
#X = df.select(
#    pl.col("dateTime").dt.year() + pl.col("dateTime").dt.month()/12 + pl.col("dateTime").dt.day()/365 + pl.col("dateTime").dt.hour()/8760 + pl.col("dateTime").dt.minute()/525600
#).to_numpy()
# convert data to numpy
#y = df["south%", "west%", "north%", "southcampus%"].to_numpy()
#print(y)
# daily variation kernel
