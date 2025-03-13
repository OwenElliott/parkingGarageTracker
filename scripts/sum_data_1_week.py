import polars as pl
import datetime
import numpy as np

df = pl.read_csv("data/transformed/transformed_parking_status.csv", try_parse_dates=True)

start_time = datetime.datetime.strptime("00:00", "%H:%M")
end_time = datetime.datetime.strptime("23:59", "%H:%M")

time_range = []
current_time = start_time
while current_time <= end_time:
    time_range.append(current_time.strftime("%H:%M"))
    current_time += datetime.timedelta(minutes=5)

# extract day of week and round time to 5-minute intervals

df = df.with_columns(
    pl.col("datetime").dt.weekday().alias("day_of_week")
)

# round into 5 minute intervals

df = df.with_columns(
    (
        (pl.col("datetime").dt.timestamp("us") // 300000000 * 300000000) # round to nearest 5 minutes
        .cast(pl.Datetime)                                  # convert back to datetime
        .alias("datetime")
    )
)

#print(df)



# segregate data into DF's by day of week
result = df
mondays_df = result.filter(pl.col("day_of_week")==1).drop("day_of_week")
tuesdays_df = result.filter(pl.col("day_of_week")==2).drop("day_of_week")
wednesdays_df = result.filter(pl.col("day_of_week")==3).drop("day_of_week")
thursdays_df = result.filter(pl.col("day_of_week")==4).drop("day_of_week")
fridays_df = result.filter(pl.col("day_of_week")==5).drop("day_of_week")
saturdays_df = result.filter(pl.col("day_of_week")==6).drop("day_of_week")
sundays_df = result.filter(pl.col("day_of_week")==7).drop("day_of_week")

# print all monday times
# print(mondays_df)

# save monday as csv for testing purposes


# aggregate the data based on same times across different weeks

# create week_dataframes with data frame for each day
days_of_week = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
week_dataframes = {}
for day in days_of_week:
    week_dataframes[day] = pl.DataFrame({})
#print(week_dataframes)

#  for testing for testing for testing for testing
# save {day}_df as csv
for day in days_of_week:
    day_df = globals()[day + "s_df"]
    print("data/transformed/weekly/"+day+"s_df.csv")
    day_df.write_csv("data/transformed/weekly/"+day+"s_df.csv")
    

#while day <= len(days):
#    time_range = []
#    current_time = start_time
#    while current_time <= end_time:
#        print(type(current_time))
#        mondays_final = mondays_df.filter(
#            (pl.col("datetime").dt.hour() == current_time) &
#            pl.col("datetime").dt.minute() == current_time)
#        current_time += datetime.timedelta(minutes=5)
#    print(day)
#    day += 1