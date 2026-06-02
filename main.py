import streamlit as st
import mysql.connector as mql
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


st.title("Stock Analyzer")

# Uploading files
main_data = st.file_uploader(label= "Upload your file here",type = ["csv"], accept_multiple_files=True) # It returns the name of the files
l = []
for i in main_data:
    l.append(i.name)

file_select = st.sidebar.selectbox("Choose the file",l)

if st.button("Done"):
    for j in main_data:
        if j.name == file_select:
            df = pd.read_csv(j)
            st.subheader("Summary")
            st.markdown(f"""
                        Stock name: {j.name}
                        \nNo. of records: {len(df)}
                        \nData Ranges from {df.iloc[1,0]} to {df.iloc[-1,0]}""")            
            st.write(" ")
            st.write(" ")
            cola,colb, colc, cold,cole, colf = st.columns(3+3)
            with cola:
                st.write("Highest Price:")
                st.write(f"₹{round(df.iloc[:,2].max(),2)} rupees on {df.loc[df['High'].idxmax(),'Date']}")
            with colb:
                st.write("Lowest Price:")
                st.write(f"₹{round(df.iloc[:,3].min(),2)} rupees on {df.loc[df['Low'].idxmin(),'Date']}")
            with colc:
                st.write("Average closing price:")
                st.write(f"₹{round(df['Close'].mean(),2)} rupees")

            # Price Charts
            st.write("Price Chart")
            fig = go.Figure(data = [go.Candlestick(x=df["Date"], open = df["Open"], close=df["Close"],high = df["High"],low=df["Low"])])
            st.plotly_chart(fig)
            
            st.subheader("Gains and losses:")
            
            