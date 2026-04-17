import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="COVID Analyzer", layout="wide")

# Title 
st.title("COVID-19 Data Analyzer 🌍")

# datasets
cases = pd.read_csv('covid19_dataset.csv')
vacc = pd.read_csv('covid_vaccinated people.csv')

cases['Country'] = cases['Country'].str.strip()
vacc['Country'] = vacc['Country'].str.strip()

# Data Cleaning 
cases['Total Cases'] = cases['Total Cases'].astype(str).str.replace(',', '').astype(float)
cases['Total Deaths'] = cases['Total Deaths'].astype(str).str.replace(',', '').astype(float)
cases['Population'] = cases['Population'].astype(str).str.replace(',', '').astype(float)

cases = cases[['Country', 'Total Cases', 'Population']]
vacc = vacc[['Country', '% of population fully vaccinated']]

# Merge datasets 
data = pd.merge(cases, vacc, on='Country')

data = data.dropna()

data['Cases per 1M'] = (data['Total Cases'] / data['Population']) * 1000000

st.sidebar.header("Filter Data")
top_n = st.sidebar.slider("Select Top Countries", 5, 30, 10)

data = data.sort_values(by='Cases per 1M', ascending=False)
top_data = data.head(top_n)

st.subheader(f"Top {top_n} Countries")
st.dataframe(top_data, use_container_width=True, hide_index=True)   

# Bar chart
st.subheader("Cases per Million (Bar Chart)")
fig1, ax1 = plt.subplots()
ax1.bar(top_data['Country'], top_data['Cases per 1M'])
plt.xticks(rotation=45)
st.pyplot(fig1)

# Scatter plot
st.subheader("Vaccination vs Cases")

fig2, ax2 = plt.subplots()
ax2.scatter(data['% of population fully vaccinated'], data['Cases per 1M'])
ax2.set_xlabel("Vaccination Rate (%)")
ax2.set_ylabel("Cases per Million")
st.pyplot(fig2)

# Country search
st.subheader("Search Country")

country = st.text_input("Enter country name")

if country:
    result = data[data['Country'].str.lower() == country.lower()]
    
    if not result.empty:
        st.dataframe(result, use_container_width=True, hide_index=True)
    else:
        st.warning("Country not found")