import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import numpy as np

all_data = pd.DataFrame()
if os.path.isfile('all_data.csv'):
    all_data = pd.read_csv("all_data.csv")
else:    
    files = [file for file in os.listdir('Sales_Data')]
    for file in files:
        my_file = pd.read_csv("./Sales_Data/" + file)
        all_data = pd.concat([all_data, my_file])

# clean data
# nan_rows = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how="all")
all_data = all_data[all_data["Order Date"].str[0:2] != "Or"]
# print (all_data)

# add month column
# all_data["Month"] = all_data["Order Date"].str[0:2].astype(str).str.replace('/', '')
# all_data["Month"] = all_data["Month"].astype('int32')
all_data["Order Date"] = pd.to_datetime(all_data["Order Date"])  
all_data["Month"] = pd.DatetimeIndex(all_data["Order Date"]).month
all_data["Hour"] = pd.DatetimeIndex(all_data["Order Date"]).hour

# print (all_data)

# add sales column
all_data["Quantity Ordered"] = all_data["Quantity Ordered"].astype('int32')
all_data["Price Each"] = all_data["Price Each"].astype(float)
all_data["Sales"] = all_data["Quantity Ordered"] * all_data["Price Each"]
# add city column
def get_city_data(x, text):
    if text == "city":
        return x.split(',')[1]
    else:
        return x.split(',')[2].split(' ')[1]
all_data["City"] = all_data["Purchase Address"].apply(lambda x: get_city_data(x, "city") + " (" + get_city_data(x, "state") + ")")
# print (all_data)

# reorder columns
cols_list = ["Order ID", "Product", "Quantity Ordered", "Price Each", "Sales", "Purchase Address", "City", "Order Date", "Month", "Hour"]
all_data = all_data[cols_list]
# print (all_data)

def group_by(text, method):
    if method == "sum":
        return all_data.groupby([text]).sum()
    if method == "average" or method == "avg" or method == "mean":
        return all_data.groupby([text]).mean()
    if method == "count":
        return all_data.groupby([text]).count()
    

# Question01 --> best month for sales and how much (+ matplotlib graphic)
best_month_sum = group_by("Month", "sum")
months = [month for month, df in all_data.groupby('Month')]
# print (best_month_sum)
# print (months)
fig = plt.figure("Oana", figsize=(6, 8))
fig.suptitle('Best for sales', fontsize=16)
fig.subplots_adjust(top=0.8)
barWidth = 0.50
ax01 = fig.add_axes([0.08,0.6,0.4,0.3]) #[left, bottom, width, height]
ax01.bar(months, best_month_sum['Sales'], color='lightblue',edgecolor='blue',width=barWidth)
ax01.set_xticks(months)
ax01.set_xlabel("Months")
ax01.set_ylabel("Sales")
ax01.set_title('Best month for sales')


# Question02 --> best city for sales and how much (+ matplotlib graphic)
best_city_sum = group_by("City", "sum")
# print(best_city_sum)
# cities = all_data['City'].unique()
cities = [city for city, df in all_data.groupby('City')]
ax02 = fig.add_axes([0.55,0.6,0.4,0.3])
ax02.bar(cities, best_city_sum['Sales'], color='lightblue',edgecolor='blue',width=barWidth)
ax02.set_xticks(cities)
ax02.set_xticklabels(cities, rotation=45, ha="right")
ax02.set_ylabel("Sales")
ax02.set_title('Best city for sales')


# Question03 --> best time to show adds to max sales
hours = [hour for hour, df in all_data.groupby('Hour')]
all_data["Count"] = 1
best_hour_count = group_by("Hour", "count")
# print(best_hour_count)
# print(hours)
ax03 = fig.add_axes([0.1,0.08,0.8,0.3])
ax03.bar(hours, best_hour_count['Sales'], color='lightblue',edgecolor='blue',width=barWidth)
ax03.set_xticks(hours)
ax03.set_xticklabels(hours, rotation=45, ha="right")
ax03.set_xlabel("Hours")
ax03.set_ylabel("Sales")
ax03.grid()
ax03.set_title('Best time to show adds to max sales')


all_data.to_csv("all_data.csv", index=False)
# print (all_data)
plt.show()