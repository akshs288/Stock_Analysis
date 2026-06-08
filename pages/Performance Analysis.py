import streamlit as st
import mysql.connector as mql
import pandas as pd

df = st.session_state["selected_file"]
file_select = st.session_state["selected_file"]


try:
    main_c = mql.connect(host= "localhost",user="root", database = "Stock_analysis", password= "Akshs123")
    if main_c.is_connected():
        cursor = main_c.cursor()
        cursor.execute("use Stock_analysis;")
        tabel_name = file_select.replace("-", "_").replace(".csv","").replace(" ","_")
        cursor.execute(f"DROP TABLE IF EXISTS `{tabel_name}`;")
        cursor.execute(f"create table `{tabel_name}` (Date DATETIME,Open FLOAT,High FLOAT,Low float,Close float,Adj_Close float, VoluINT)")
                
        df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True).dt.strftime("%Y-%m-%d")                    
        query = f"""
        INSERT INTO `{tabel_name}` (`Date`, `Open`, `High`, `Low`, `Close`, `Adj_Close`, `Volume`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]].values.tolist()
        cursor.executemany(query, data)
                    
        # cursor.execute("create view daily_return as select year(date) as _year,daily_return from (select *,(LAG(CLOSE) OVER(ORDER DATE)-close)/close as daily_Return from a) t;")
        # cursor.execute("select _year, round((stddev(daily_return)* sqrt(252))*100,2) as volatility from daily_return  group by _year;")
        # volatility = cursor.fetchall()   # It will return list of tuples
        main_c.commit()
                        
except Exception as e:
        print("Any error occured -",e)

st.subheader("💹 Performance of stock")

st.write("")
st.write("")
st.write("")
cola,colb,colc = st.columns(3)



with cola:
    st.write("📈Best Return Day")
    
with colb:
    st.write("📉Lowest Return Day")
        
with colc:
    st.write("⚖️Average Return Day")
        

