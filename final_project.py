import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="COVID-19 Analysis",
    page_icon="🦠",
    layout="wide"
)

st.title("COVID-19 Data Analysis")
st.write("Analysis of COVID-19 spread, cases, recoveries and deaths")

# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.header("COVID-19 Dashboard")

# -------------------------------
# Sample Data
# -------------------------------

data = {
    "Country": [
        "India", "India", "India",
        "USA", "USA", "USA",
        "UK", "UK", "UK"
    ],

    "Date": [
        "2020-01-01", "2020-02-01", "2020-03-01",
        "2020-01-01", "2020-02-01", "2020-03-01",
        "2020-01-01", "2020-02-01", "2020-03-01"
    ],

    "Confirmed": [
        100, 500, 5000,
        200, 1000, 10000,
        150, 700, 7000
    ],

    "Recovered": [
        20, 100, 1000,
        30, 200, 2000,
        25, 150, 1500
    ],

    "Deaths": [
        2, 10, 100,
        5, 20, 300,
        3, 15, 150
    ]
}

df = pd.DataFrame(data)

df.to_csv("covid.csv", index=False)

df = pd.read_csv("covid.csv")

df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------
# Country Selection
# -------------------------------

countries = sorted(df["Country"].unique())

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

country_data = df[
    df["Country"] == selected_country
]

# -------------------------------
# COVID Data
# -------------------------------

st.subheader("COVID-19 Data")

st.dataframe(
    df,
    use_container_width=True
)

# -------------------------------
# Data Information
# -------------------------------

st.subheader("Data Information")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Countries", df["Country"].nunique())
col4.metric(
    "Total Confirmed",
    df["Confirmed"].sum()
)

# -------------------------------
# Summary
# -------------------------------

st.subheader("COVID-19 Summary")

total_confirmed = df["Confirmed"].sum()
total_recovered = df["Recovered"].sum()
total_deaths = df["Deaths"].sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Confirmed Cases",
    total_confirmed
)

col2.metric(
    "Recovered Cases",
    total_recovered
)

col3.metric(
    "Deaths",
    total_deaths
)

# -------------------------------
# Country-wise Analysis
# -------------------------------

st.subheader("Country-wise COVID-19 Analysis")

country_summary = df.groupby(
    "Country"
)[
    ["Confirmed", "Recovered", "Deaths"]
].max()

st.dataframe(
    country_summary,
    use_container_width=True
)

highest_country = country_summary[
    "Confirmed"
].idxmax()

highest_cases = country_summary[
    "Confirmed"
].max()

st.write(
    "Country with Highest Confirmed Cases:",
    highest_country
)

st.write(
    "Highest Confirmed Cases:",
    highest_cases
)

average_confirmed = np.mean(
    country_summary["Confirmed"]
)

st.write(
    "Average Confirmed Cases:",
    round(average_confirmed, 2)
)

# -------------------------------
# COVID Spread Over Time
# -------------------------------

st.subheader("COVID-19 Spread Over Time")

trend = df.groupby(
    "Date"
)[
    ["Confirmed", "Recovered", "Deaths"]
].sum()

fig, ax = plt.subplots(figsize=(8, 4))

trend.plot(ax=ax)

ax.set_title("COVID-19 Spread Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Cases")

st.pyplot(fig)

plt.close(fig)

# -------------------------------
# Selected Country Trend
# -------------------------------

st.subheader(
    "COVID-19 Trend - " + selected_country
)

fig, ax = plt.subplots(figsize=(8, 4))

country_data.plot(
    x="Date",
    y=[
        "Confirmed",
        "Recovered",
        "Deaths"
    ],
    ax=ax,
    marker="o"
)

ax.set_title(
    "COVID-19 Trend in " + selected_country
)

ax.set_xlabel("Date")
ax.set_ylabel("Cases")

st.pyplot(fig)

plt.close(fig)

# -------------------------------
# Country Comparison
# -------------------------------

st.subheader("Country Comparison")

country_total = df.groupby(
    "Country"
)[
    ["Confirmed", "Recovered", "Deaths"]
].max()

fig, ax = plt.subplots(figsize=(8, 4))

country_total.plot(
    kind="bar",
    ax=ax
)

ax.set_title("COVID-19 Country Comparison")
ax.set_xlabel("Country")
ax.set_ylabel("Cases")

ax.tick_params(
    axis="x",
    rotation=45
)

st.pyplot(fig)

plt.close(fig)

# -------------------------------
# Death Analysis
# -------------------------------

st.subheader("Death Analysis")

fig, ax = plt.subplots(figsize=(8, 4))

country_total["Deaths"].plot(
    kind="bar",
    ax=ax
)

ax.set_title("Deaths by Country")
ax.set_xlabel("Country")
ax.set_ylabel("Deaths")

ax.tick_params(
    axis="x",
    rotation=45
)

st.pyplot(fig)

plt.close(fig)

# -------------------------------
# Seaborn Chart
# -------------------------------

st.subheader("Confirmed COVID-19 Cases")

fig, ax = plt.subplots(figsize=(8, 4))

sns.lineplot(
    data=country_data,
    x="Date",
    y="Confirmed",
    marker="o",
    ax=ax
)

ax.set_title(
    "Confirmed COVID-19 Cases - " +
    selected_country
)

ax.set_xlabel("Date")
ax.set_ylabel("Confirmed Cases")

ax.tick_params(
    axis="x",
    rotation=45
)

st.pyplot(fig)

plt.close(fig)

# -------------------------------
# Intervention Analysis
# -------------------------------

st.subheader(
    "Effect of Intervention on COVID-19 Spread"
)

intervention_date = st.date_input(
    "Select Intervention Date",
    value=country_data["Date"].min().date()
)

intervention_date = pd.to_datetime(
    intervention_date
)

before = country_data[
    country_data["Date"] < intervention_date
]

after = country_data[
    country_data["Date"] >= intervention_date
]

before_cases = before["Confirmed"].sum()
after_cases = after["Confirmed"].sum()

col1, col2 = st.columns(2)

col1.metric(
    "Cases Before Intervention",
    before_cases
)

col2.metric(
    "Cases After Intervention",
    after_cases
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(
    country_data["Date"],
    country_data["Confirmed"],
    marker="o"
)

ax.axvline(
    intervention_date,
    linestyle="--"
)

ax.set_title(
    "Intervention Effect - " +
    selected_country
)

ax.set_xlabel("Date")
ax.set_ylabel("Confirmed Cases")

plt.xticks(rotation=45)

st.pyplot(fig)

plt.close(fig)

# -------------------------------
# Conclusion
# -------------------------------

st.subheader("Analysis Conclusion")

st.write(
    "COVID-19 spread, confirmed cases, recoveries "
    "and deaths were analyzed over time. "
    "Different countries were compared using "
    "data visualization. The intervention date "
    "was also used to compare cases before and "
    "after the intervention."
)