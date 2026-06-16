import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as datatime

df=pd.read_excel("C:\\Users\\Mega Store\\Desktop\\python\\ecommerce_orders\\ecommerce_orders-1.xlsx")
pd.set_option("display.max_rows",None)
pd.set_option("display.max_columns",None)
pd.set_option("display.width",None)
#print(df)
#print(df.shape)
#print(df.info())
# print(df.describe(include="all").T)
# print(df.nunique())

df.columns=df.columns.str.strip()
df.columns=df.columns.str.replace("_"," ").str.lower()
#print(df.columns)

text_columns=["customer name","product","category"
,"payment method","status","order id"]

for i in text_columns:
    df[i]=df[i].astype(str)
    df[i]=df[i].str.strip().str.lower()
    df[i]=df[i].replace({"nan":np.nan})

#print(df.info())





df["order date"]=pd.to_datetime(df["order date"],errors="coerce")
#print(df["order date"])
#print(df["order date"].info())


df["quantity"]=pd.to_numeric(df["quantity"],errors="coerce").astype("Int64")
#print(df["quantity"])

df["price"]=pd.to_numeric(df["price"],errors="coerce")
#print(df["price"])



df["price"]=df.groupby("product")["price"].transform(lambda x:x.fillna(x.median()))
#print(df["price"])

df["price"]=df["price"].fillna(df["price"].median())


df=df.dropna(subset=["order date","quantity"])
#print(df.info())

dup_order_id=df[df.duplicated(subset=["order id"],keep=False)]
#print(dup_order_id)

df=df.drop_duplicates(subset="id")

df["total"]=df["quantity"]*df["price"].round(2)
#print(df)

df["order_year"]=df["order date"].dt.year
#print(df["order_year"])
#print(df["order_year"].info())
df["order_month"]=df["order date"].dt.to_period("M")
#print(df["order_month"])
df["order_day"]=df["order date"].dt.day
#print(df["order_day"])

df["uorder date"]=df["order date"].dt.date
#print(df["uorder date"])

df["torder date"]=df["order date"].dt.time
#print(df["torder date"])

#g=df.groupby("order_year")["price"].sum()
#print(g)

#cat_rev=df.groupby("category")["total"].sum()
cat_rev=df.groupby("category").agg(revenue=("total","sum"),items=("quantity","sum")).sort_values("revenue",ascending=False).reset_index()
#print(cat_rev)
prod_rev=df.groupby("product").agg(revenue=("total","sum"),items=("quantity","sum")).sort_values("revenue",ascending=False).head(3)
#print(prod_rev)

monthly_rev=df.groupby("order_month").agg(month=("total","sum")).sort_values("month",ascending=False)
#print(monthly_rev)

year_rev=df.groupby("order_year").agg(year=("total","sum"))
#print(year_rev)
daily_rev=df.groupby("uorder date").agg(day=("total","sum")).reset_index()
#print(daily_rev)
count_payment_method=df["payment method"].value_counts().reset_index()
#print(count_payment_method)
count_status=df["status"].value_counts().reset_index()
count_status=df["status"].value_counts(normalize=True).reset_index()
print(count_status)

plt.figure(figsize=(8,5))
plt.bar(cat_rev["category"],cat_rev["revenue"])
plt.title("Revenue by Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))
plt.plot(daily_rev["uorder date"],daily_rev["day"])
plt.xticks(rotation=45)
plt.title("Daily Revenue")
plt.xlabel("Date")
plt.ylabel("revenue")
plt.tight_layout()
plt.show()

df.to_excel("ecommerce_order_cleaned.xlsx",index=False)
cat_rev.to_csv("report_of_category_revenue.csv")





