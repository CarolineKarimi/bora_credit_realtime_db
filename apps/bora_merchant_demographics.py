#!/usr/bin/env python
# coding: utf-8

# In[11]:


import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly_express as px
import plotly.graph_objects as go

# Define a custom color mapping dictionary
unique_colors = ['rgb(164,164,213)','rgb(249,167,41)', 'rgb(145,220,234)', 'rgb(249,210,60)','rgb(95,187,104)',
'rgb(187,201,229)','rgb(100,205,204)','rgb(253,111,48)','rgb(235,30,44)','rgb(252,113,158)','rgb(206,105,190)',
'rgb(120,115,192)','rgb(213,187,33)','rgb(87,163,55)','rgb(27,163,198)','rgb(255,190,209)','rgb(128,116,168)',
'rgb(196,100,135)','rgb(158,61,34)']

def app():

    @st.cache_data

    def load_df_1():
        df = pd.read_csv('aggregated_demographic_data.csv')
        return df

    st.header('Sample Description')
    st.subheader('Bora Credit: March 2024')
    
    red_markdown = "#F03E35"

# load data
    df = load_df_1()

    c =df.Aggregation.unique().tolist()
    # Create a counter to keep track of the charts in the current row
    chart_counter = 0
    if len(c) == 0:
         st.markdown(f'<p style="color:{red_markdown}; font-size: 14px; font-style: italic;">Select some categories</p>', unsafe_allow_html=True)

    else:
         chart_columns  = st.columns(2)
         for item in c:
             df1 = df[(df.Aggregation== item)].copy()
             df1 = df1.rename(columns={'Cnt': 'Count'})
             definition=(df[(df.Aggregation == item)].Question.unique().tolist())[0]
             # Concatenate item and definition with a newline
             titles = f"{definition}<br><br>&nbsp;<br>"
             
             x_lab = (df1[df1['Aggregation'] ==item]['Y_axis'].unique().tolist())[0]
             # Calculate the maximum value from the df1 dataframe
             
             fig = px.bar(df1, y='Answer', x="Value", color="Answer", color_discrete_sequence=unique_colors,
                     orientation='h',title=(titles),hover_data={'Answer': True,'Count': ':.0f', 'Value': ':,.3f'},
                     labels={'Value': x_lab})

            
             # Remove gaps for zero values
             fig.update_xaxes(categoryorder='total ascending')
             fig.update_layout(legend=dict(orientation="h", xanchor="auto", x=0, yanchor="bottom", y=-1))
             fig.update_layout(showlegend=False)
            
             
             # Specify the category order
             fig.update_xaxes(tickformat=".0%")
             fig.update_xaxes(range=[0, 1])     
             
             fig.update_layout(xaxis=dict(showline=True,showgrid=False, zeroline=False,visible=True,title=df1['Y_axis'].iloc[0]),yaxis=dict(showgrid=False, zeroline=True,visible=True),)
             
             
             # Update font size for all text elements
             font_size = 16  # Choose your desired font size
             fig.update_layout(font=dict(size=font_size),xaxis=dict(tickfont=dict(size=font_size)),
             yaxis=dict(tickfont=dict(size=font_size)),legend=dict(font=dict(size=font_size)),
             title=dict(font=dict(size=font_size)))
             fig.update_traces(textfont=dict(size=font_size))
             fig.update_traces(textposition='inside',textfont_size=25, texttemplate='%{x:.0%}')
             fig.update_layout(yaxis_title=None)
             
             # Place the chart in the appropriate column of the current row
             with chart_columns[chart_counter]:
                 st.plotly_chart(fig, use_container_width=True)
            
             #row[chart_counter].plotly_chart(fig)
             chart_counter += 1
             if chart_counter == 2:
                 chart_counter = 0

         
 




        
    
        
    