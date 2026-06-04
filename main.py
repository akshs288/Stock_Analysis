import streamlit as st
import mysql.connector as mql
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

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
            cola,colb, colc, cold, cole, colf = st.columns(3+3)
            with cola:
                st.write("Highest Price:")
                st.write(f"₹{round(df.iloc[:,2].max(),2)} rupees on {df.loc[df['High'].idxmax(),'Date']}")
            with colb:
                st.write("Lowest Price:")
                st.write(f"₹{round(df.iloc[:,3].min(),2)} rupees on {df.loc[df['Low'].idxmin(),'Date']}")
            with colc:
                st.write("Average closing price:")
                st.write(f"₹{round(df['Close'].mean(),2)} rupees")
            
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            # Showing volatility for a share
            st.write("Volatility")
            try:
                main_c = mql.connect(host= "localhost",user="root", database = "Stock_analysis", password= "Akshs123")
                if main_c.is_connected():
                    cursor = main_c.cursor()
                    cursor.execute("use Stock_analysis;")
                    tabel_name = file_select.replace("-", "_").replace(".csv","").replace(" ","_")
                    cursor.execute(f"DROP TABLE IF EXISTS `{tabel_name}`;")
                    cursor.execute(f"create table `{tabel_name}` (Date DATETIME,Open FLOAT,High FLOAT,Low float,Close float,Adj_Close float, Volume INT)")
                
                    df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True).dt.strftime("%Y-%m-%d")                    
                    query = f"""
                    INSERT INTO `{tabel_name}` (`Date`, `Open`, `High`, `Low`, `Close`, `Adj_Close`, `Volume`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    data = df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]].values.tolist()
                    cursor.executemany(query, data)
                    
                    
                    main_c.commit()
                        
            except Exception as e:
                    print("Any error occured -",e)
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            # Price Charts
            st.write("Price Chart")
            fig = go.Figure(data = [go.Candlestick(x=df["Date"], open = df["Open"], close=df["Close"],high = df["High"],low=df["Low"])])
            st.plotly_chart(fig)
                    