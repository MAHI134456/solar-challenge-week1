import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_and_process_data, create_boxplot, create_ghi_ranking

# Set page configuration
st.set_page_config(page_title="Solar Potential Dashboard", layout="wide")

# Title and description
st.title("Solar Potential Comparison Dashboard")
st.write("Explore solar potential (GHI, DNI, DHI) across Benin, Sierra Leone, and Togo with interactive visualizations.")

# Sidebar for interactive controls
st.sidebar.header("Filters")
metric = st.sidebar.selectbox("Select Metric", ["GHI", "DNI", "DHI"])
min_value = st.sidebar.slider("Minimum Value (W/m²)", 0, 1000, 0)
max_value = st.sidebar.slider("Maximum Value (W/m²)", 0, 1000, 1000)

# Load and process data (placeholder function call)
data = load_and_process_data("data/benin_clean.csv", "data/togo_clean.csv", "data/sierraleone_clean.csv")

# Filter data based on slider values
filtered_data = data[(data[metric] >= min_value) & (data[metric] <= max_value)]

# Display data summary
st.subheader("Data Summary")
st.write(filtered_data.describe())

# Create and display boxplot
st.subheader(f"{metric} Distribution by Country")
fig1 = create_boxplot(filtered_data, metric)
st.pyplot(fig1)

# Create and display GHI ranking bar chart
st.subheader("Average GHI Ranking by Country")
fig2 = create_ghi_ranking(filtered_data)
st.pyplot(fig2)

# Add interactivity note
st.sidebar.write("Adjust the sliders to filter data and explore different ranges.")