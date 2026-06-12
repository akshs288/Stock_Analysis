import mysql.connector as mql
import streamlit as st   
import pandas as pd

def main_save(filename,df):
    try:
        main_c = mql.connect(host= "localhost",user="root", database = "Stock_analysis", password= "Akshs123")
        if main_c.is_connected():
            cursor = main_c.cursor()
            cursor.execute("use Stock_analysis;")
            tabel_name = filename.replace("-", "_").replace(".csv","").replace(" ","_")
            cursor.execute(f"drop table if exists `{tabel_name}`;")
            cursor.execute(f"create table if not exists `{tabel_name}` (Date DATE primary key,Open FLOAT,High FLOAT,Low float,Close float,Adj_Close float, Volume INT)")
        
            df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True).dt.strftime("%Y-%m-%d")                    
            query = f"""
            INSERT INTO `{tabel_name}` (`Date`, `Open`, `High`, `Low`, `Close`, `Adj_Close`, `Volume`)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            data = df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]].values.tolist()
            cursor.executemany(query, data)

            main_c.commit()
            return cursor,tabel_name, main_c

    except Exception as e:
        print("Any error occurred - ",e)
        st.warning("Any error occurred")
        return None, None,None
        
