import streamlit as st
import mysql.connector as mql
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.title("📊 🖥️ Stock Analyzer")

# Uploading files
main_data = st.file_uploader(label= "Upload your file here",type = ["csv"], accept_multiple_files=True) # It returns the name of the files
l = []
for i in main_data:
    l.append(i.name)

file_select = st.sidebar.selectbox("Choose the file",l)

if st.button("Done"):
    for j in main_data:
        if j.name == file_select:
            st.session_state["selected_file"] = j        # File is stored in session state
            st.session_state["file_name"] = j.name
            df = pd.read_csv(j)
            st.session_state["df"] = df                  # Data is stored in this df
            
            st.subheader("📋Summary")
            st.markdown(f"""
                        Stock name: {j.name}
                        \nNo. of records: {len(df)}
                        \nData Ranges from {df.iloc[1,0]} to {df.iloc[-1,0]}""")
            st.write("----------------x------------------x------------------x------------------x------------------x------------------x------------------x")
            st.write(" ")
            cola,colb, colc = st.columns(3)
            with cola:
                st.write("💵Highest Price:")
                price1 = str("₹")+str(round(df.iloc[:,2].max(),2))
                date1 = str(df.loc[df['High'].idxmax(),'Date'])

            cola.metric(date1,price1,border=True)
            
            with colb:
                st.write("📉Lowest Price:")
                price2 = str("₹")+str(round(df.iloc[:,3].min(),2))
                date2 = str(df.loc[df['Low'].idxmin(),'Date'])

            colb.metric(date2,price2,border=True)

            with colc:
                st.write("⚖️Average closing price:")
                price3 = str("₹")+str(round(df['Close'].mean(),2))
            colc.metric(price3,"","",border=True)
            
            st.write("----------------x------------------x------------------x------------------x------------------x------------------x------------------x")
            st.write(" ")
            # Price Charts
            st.write("📊Price Chart")
            fig = go.Figure(data = [go.Candlestick(x=df["Date"], open = df["Open"], close=df["Close"],high = df["High"],low=df["Low"])])
            st.plotly_chart(fig)
            
            
            
