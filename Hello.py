import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper
import numpy as np 
def fun(value):
    if(type(value)!=str):
        return value
    else:
        test=arabic_reshaper.reshape(value)
        test=get_display(test)
        return test
    

def arabic_list(value):
    data=[]
    for i in value:
        test=arabic_reshaper.reshape(i)
        test=get_display(test)
        data.append(test)
    return data

df=pd.read_csv("Kenzy Mamdouh.csv")
st.title("Dashboard")

col1, col2, col3,col4 = st.columns(4)

col1.metric(label="Number of clients", value=len(df.index))

col2.metric(label="Number of courses", value=9)

col4.metric(label="Number of academic year", value=len(df["السنة الدراسية"].unique()))
col3.metric(label="Number of months", value=3)

#col1, col2, col3 = st.columns(3)
df["طابع زمني"]= pd.to_datetime(df["طابع زمني"])
months=df["طابع زمني"].dt.month.unique()
monthsdata=[]
for month in months: 
    test=df[df["طابع زمني"].dt.month==month]
    final=test.iloc[:,8:16].groupby(test["السنة الدراسية"]).agg(sum).max().sort_values(ascending=[False])[0:5]
    final.index=arabic_list(final.index)  
    monthsdata.append(final)

def monthShow(final):
    plt.figure(figsize=(9,4))
    plt.bar(final.index,final.values)
    col1.pyplot(plt)
    
col1, col2,col3 = st.columns(3)

col1.subheader("Top 5 courses per month")
selected_month = col1.selectbox("Select a month:", options=list(months))

# Display the corresponding image
print(selected_month)


if selected_month:
    itemindex = np.where( months== selected_month)
    monthShow(monthsdata[itemindex[0][0]])
else:
    st.write("No image found for selected month")


col2.subheader("Most advertising places")
plt.figure(figsize=(8,5))
plt.pie(df["من أين علمت عن جينيس؟"].value_counts(),labels= df["من أين علمت عن جينيس؟"].value_counts().index,autopct='%0.0f%%')
col2.pyplot(plt)


col3.subheader("Academic year by course")
all=df.iloc[:,8:16].groupby(df["السنة الدراسية"]).agg(sum).idxmax(axis=1)

col3.table(all)

col1.subheader("Locations of most customer cities")
cities=df["city"].value_counts() 
cities.index=arabic_list(cities.index)  
plt.figure(figsize=(9,6))
plt.bar(cities[:10].index,cities[:10].values)
col1.pyplot(plt)

col1.subheader("Locations of most customer towns")
town=df["town"].value_counts() 
town.index=arabic_list(town.index)  
plt.figure(figsize=(11,6))
plt.bar(town[:10].index,town[:10].values)
col1.pyplot(plt)


col2.subheader("Do you find distance education useful and important?")
artext=df["هل ترى التعليم عن بعد مفيد ومهم؟"].apply(fun)
plt.figure(figsize=(9,6))
plt.pie(artext.value_counts().values,labels= artext.value_counts().index,autopct='%0.1f%%')
col2.pyplot(plt)