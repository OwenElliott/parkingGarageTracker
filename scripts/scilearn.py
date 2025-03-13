import scipy, datetime
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ExpSineSquared, RationalQuadratic, WhiteKernel

#download dataset and store in co2
co2 = fetch_openml(data_id=41187, as_frame=True)
co2.frame.head()

# process dataframe to create date column and select it with CO2 collumn
co2_data = pl.DataFrame(co2.frame[["year","month","day","co2"]]).select(
    pl.date("year","month","day"), "co2")
co2_data.head()

#plot data on graph
# x-axis: time    y-axis: co2 Concentration
#preprocess data set by
# (1) taking monthly average
# (2) drop months for which no measurements are collected
co2_data = ( #set co2_data to
    co2_data.sort(by="date")# sort data by date
    .group_by_dynamic("date", every="1mo") # then group by month
    .agg(pl.col("co2").mean()) # cluster by taking mean of co2 levels
    .drop_nulls() # drop clusters with 0 co2 readings
)
#plt.plot(co2_data["date"], co2_data["co2"])
#plt.xlabel("date")
#plt.ylabel("Monthly average of C0$_2$ concentration (ppm)")
#_ = plt.title("Monthly average of air samples measurements\nfrom the Mauna Loa Observatory")
#plt.show()
#convert date to numeric value
X = co2_data.select(
    #select column date, get the year add it to the month devided by 12
    # 1975.000, 1975.083, 1975.167, ...
    pl.col("date").dt.year() + pl.col("date").dt.month() / 12
).to_numpy()
y = co2_data["co2"].to_numpy()

#long term rising trend
long_term_trend_kernel = 50.0**2 * RBF(length_scale=50.0)

# seasonal variation
seasonal_kernel = (
    2.0**2
    * RBF(length_scale=100.0)
    * ExpSineSquared(length_scale=1.0, periodicity=1.0, periodicity_bounds="fixed")
)

#small irregularities
irregularities_kernel = 0.5**2 * RationalQuadratic(length_scale=1.0, alpha=1.0)

#noise
noise_kernel = 0.1**2 * RBF(length_scale=0.1) + WhiteKernel(
    noise_level=0.1**2, noise_level_bounds=(1e-5, 1e5)
)

#final combined kernel
co2_kernel = (
    long_term_trend_kernel + seasonal_kernel + irregularities_kernel + noise_kernel
)
#print(co2_kernel)

#model fitting and extrapolation stage

#subtract the mean from the target
y_mean = y.mean()
gaussian_process = GaussianProcessRegressor(kernel=co2_kernel, normalize_y=False)
gaussian_process.fit(X, y - y_mean)

#use gaussian process to predict on:
# training data to inspect the goodness of fit;
# future data to see the extrapolation done by the model
# create syntehic data from 1958 to curernt month.
# add the subtracted mean computed during training
today = datetime.datetime.now()
current_month = today.year + today.month/12
X_test = np.linspace(start=1958, stop=current_month, num=1_000).reshape(-1, 1)
mean_y_pred, std_y_pred = gaussian_process.predict(X_test, return_std=True)
mean_y_pred += y_mean

#plotting plot + prediction
plt.plot(X, y, color="black", linestyle="dashed", label="Measurements")
plt.plot(X_test, mean_y_pred, color="tab:blue", alpha=0.4, label="Gaussian process")
plt.fill_between(
    X_test.ravel(),
    mean_y_pred - std_y_pred,
    mean_y_pred + std_y_pred,
    color="tab:blue",
    alpha=0.2,
)
plt.legend()
plt.xlabel("Year")
plt.ylabel("Month averag of CO$_2$ concentration (ppm)")
_ = plt.title(
    "Montly average of air samples measurements\nfrom the Mauna Loa Observatory"
)
plt.show()