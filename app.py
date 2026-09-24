import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="COVID-19 Analysis",
    page_icon="🦠",
    layout="wide"
)

st.title("COVID-19 Analysis")
st.write("COVID-19 data analysis using Python and Streamlit")

df = pd.read_csv("covid.csv")

st.subheader("COVID-19 Dataset")
st.dataframe(df, use_container_width=True)

st.subheader("Top 10 Countries by Confirmed Cases")

top_10 = (
    df.groupby("Country")["Confirmed"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots()
top_10.plot(kind="bar", ax=ax)
ax.set_xlabel("Country")
ax.set_ylabel("Confirmed Cases")
ax.set_title("Top 10 Countries by Confirmed Cases")
plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader("COVID-19 Trend")

country = st.selectbox(
    "Select Country",
    df["Country"].unique()
)

country_data = df[df["Country"] == country]

fig2, ax2 = plt.subplots()
ax2.plot(
    country_data["Date"],
    country_data["Confirmed"],
    marker="o",
    label="Confirmed"
)
ax2.plot(
    country_data["Date"],
    country_data["Recovered"],
    marker="o",
    label="Recovered"
)
ax2.plot(
    country_data["Date"],
    country_data["Deaths"],
    marker="o",
    label="Deaths"
)

ax2.set_xlabel("Date")
ax2.set_ylabel("Cases")
ax2.set_title(f"COVID-19 Trend - {country}")
ax2.legend()
plt.xticks(rotation=45)

st.pyplot(fig2)
