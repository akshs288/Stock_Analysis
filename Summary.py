import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from mysql_connect import main_save


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
            df = st.session_state["df"]
            filename = st.session_state["file_name"]
            cursor,tabel_name,sql_connect = main_save(filename,df)

            # Defining session states
            st.session_state["main_cursor"] = cursor
            st.session_state["tabel_name1"] = tabel_name
            st.session_state["connection"] = sql_connect

            if cursor is None:
                st.error("❌ Something happens")
                st.stop()
          
            st.subheader("📋Summary")
            cursor.execute(f"""select 
                           min(date), 
                           max(date), 
                           count(*),
                           (select date from `{tabel_name}` where High = (select max(High) from `{tabel_name}`)),
                           (select High from `{tabel_name}` where High = (select max(High) from `{tabel_name}`)),
                           (select date from `{tabel_name}` where Low = (select min(Low) from `{tabel_name}`)),
                           (select Low from `{tabel_name}` where Low = (select min(Low) from `{tabel_name}`)),
                           (select avg(Close) from `{tabel_name}`) 
                           from `{tabel_name}`""")

            main_data = cursor.fetchone()
            start_date = str(main_data[0])
            end_date = str(main_data[1])
            len_d = str(main_data[2])
            date1 = str(main_data[3])
            price1 = str(main_data[4])
            date2 = str(main_data[5])
            price2  = str(main_data[6])
            price3  = str(main_data[7])
            
            st.markdown(f"""
                        Stock name: {j.name}
                        \nNo. of records: {len_d}
                        \nData Ranges from {start_date} to {end_date}""")
            
            st.write("----------------x------------------x------------------x------------------x------------------x------------------x------------------x")
            st.write(" ")
            cola,colb, colc = st.columns(3)
            with cola:
                st.write("💵Highest Price:")
            cola.metric(date1,price1,border=True)
            
            with colb:
                st.write("📉Lowest Price:")
            colb.metric(date2,price2,border=True)

            with colc:
                st.write("⚖️Average closing price:")
            colc.metric("",price3,"",border=True)
            
            st.write("----------------x------------------x------------------x------------------x------------------x------------------x------------------x")
            st.write(" ")
            # Price Charts
            st.write("📊Price Chart")
            # fig = go.Figure(data = [go.Candlestick(x=df["Date"], open = df["Open"], close=df["Close"],high = df["High"],low=df["Low"])])
            # st.plotly_chart(fig)
            
            
            
