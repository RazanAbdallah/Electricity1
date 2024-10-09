import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
path = "https://linked.aub.edu.lb/pkgcube/data/8008173bd298d3924db1f875942e8bd7_20240909_165536.csv"
data = pd.read_csv(path)

# Preprocess the data to remove 'https://dbpedia.org/page/' from 'refArea'
data['refArea'] = data['refArea'].str.replace('https://dbpedia.org/page/', '', regex=False)
data['refArea'] = data['refArea'].str.replace('http://dbpedia.org/resource/', '', regex=False)

# Create DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.title("Lebanon Electricity Data Visualization")

# Introduction to Lebanon's Electricity Infrastructure
st.subheader("Introduction to Lebanon's Electricity Infrastructure")
st.write("""
Lebanon's electricity infrastructure has faced significant challenges over the years. 
The country has experienced chronic power shortages, with daily electricity cuts that often last up to 12 hours or more. 
Lebanon relies heavily on expensive and inefficient fuel imports to power its plants, leading to financial and environmental burdens. 
The power sector accounts for a substantial portion of Lebanon’s public debt due to mismanagement, outdated infrastructure, and corruption. 
In recent years, alternative energy sources, such as solar power, have gained attention as potential solutions to these issues, though their implementation has been slow.
""")

# Adding an image related to electricity infrastructure in Lebanon
image_url = "https://images.app.goo.gl/cJUCY2Bgi82Xfdoe9"
st.image(image_url, caption="Lebanon's Electricity Infrastructure", use_column_width=True)

image_path = r"C:\Users\user\Downloads\edl.jpg"  # Raw string
st.image(image_path, caption="Lebanon's Electricity Infrastructure", use_column_width=True)


# Multi-select for refArea to compare multiple areas
ref_area = st.multiselect("Select RefArea(s):", df['refArea'].unique(), default=[df['refArea'].iloc[0]])

# Filter the data based on selected refAreas
filtered_data = df[df['refArea'].isin(ref_area)]

# Group data by 'refArea' and 'Existence of alternative energy - exists'
grouped_data = filtered_data.groupby(['refArea', 'Existence of alternative energy - exists']).size().reset_index(name='Count')

# Pivot the data to get counts for both "Exists" (1) and "Does not exist" (0)
pivot_data = grouped_data.pivot(index='refArea', columns='Existence of alternative energy - exists', values='Count').fillna(0)
pivot_data.columns = ['Does not exist', 'Exists']

# Reset index to make 'refArea' a column again for plotting
pivot_data = pivot_data.reset_index()

# Bar chart comparing existence (1) vs non-existence (0) of alternative energy by refArea
fig1 = px.bar(pivot_data, 
              x='refArea', 
              y=['Exists', 'Does not exist'], 
              title="Comparison of Alternative Energy Existence by RefArea",
              labels={'value': 'Count', 'variable': 'Energy Status'},
              barmode='group',  # Grouped bars for easy comparison
              height=500)

# Display the bar chart
st.plotly_chart(fig1)  # Bar chart first

# Filter the data based on selected RefArea for the pie chart
filtered_data_pie = df[df['refArea'].isin(ref_area)]

# Group data by 'Existence of alternative energy - exists' for the pie chart
grouped_data_pie = filtered_data_pie.groupby('Existence of alternative energy - exists').size().reset_index(name='Count')

# Map the existence values to their labels
grouped_data_pie['Existence Status'] = grouped_data_pie['Existence of alternative energy - exists'].map({1: '1 Exists', 0: '0 Does Not Exist'})

# Pie chart to show proportion of alternative energy existence
fig3 = px.pie(grouped_data_pie, 
              names='Existence Status',  # Use mapped labels for the names
              values='Count', 
              title=f"Proportion of Alternative Energy Existence in Selected Areas: {', '.join(ref_area)}",
              hover_data=['Existence Status'],  # Show existence status on hover
              color_discrete_sequence=['lightblue', 'blue'])  # Custom colors for the pie chart

# Adding text on the pie slices for clarity
fig3.update_traces(textinfo='percent+label', pull=[0.1 if i == 0 else 0 for i in range(len(grouped_data_pie))])

# Display the pie chart second
st.plotly_chart(fig3)  # Pie chart second
