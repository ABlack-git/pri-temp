from datetime import datetime as dt, timedelta
import random
import pandas as pd

start_date = "2022-05-01 00:00:00"
end_date = "2022-11-27 23:59:59"
time_format = "%Y-%m-%d %H:%M:%S"
current_time = dt.strptime(start_date, time_format)
end_time = dt.strptime(end_date, time_format)

print(current_time, end_date)

delta = timedelta(minutes=30)

data = {
    "date": [],
    "temperature": [],
    "humidity": []
}


while current_time < end_time:
    data["date"].append(current_time.strftime(time_format))
    data["temperature"].append(random.uniform(17, 25.0))
    data["humidity"].append(random.randint(20, 80))
    current_time = delta + current_time


df = pd.DataFrame(data)
df.to_csv("data.csv", sep=",", index=False)