import streamlit as st
import mysql.connector as mql
import pandas as pd

df = st.session_state["df"]
filename = st.session_state["file_name"]

st.subheader("💹 Performance of stock")

st.write("")
st.write("")
st.write("")
cola,colb,colc = st.columns(3)
    

try:
    main_c = mql.connect(host= "localhost",user="root", database = "Stock_analysis", password= "Akshs123")
    if main_c.is_connected():
        cursor = main_c.cursor()
        cursor.execute("use Stock_analysis;")
        tabel_name = filename.replace("-", "_").replace(".csv","").replace(" ","_")
        cursor.execute(f"create table if not exists `{tabel_name}` (Date DATE,Open FLOAT,High FLOAT,Low float,Close float,Adj_Close float, Volume INT)")
    
        df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True).dt.strftime("%Y-%m-%d")                    
        query = f"""
        INSERT INTO `{tabel_name}` (`Date`, `Open`, `High`, `Low`, `Close`, `Adj_Close`, `Volume`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]].values.tolist()
        cursor.executemany(query, data)

        main_c.commit()
        with cola:
            st.write("📈Best Return Day")
            cursor.execute(f"with cte1 as (select *,(LAG(CLOSE) OVER(ORDER BY DATE)-close)/close as daily_Return from `{tabel_name}`) select date,round(daily_return,2) as Highest_return from cte1 where daily_return = (select max(daily_return) from cte1);")    
            lis_tup = cursor.fetchall()
            high_date = "On "+ str(lis_tup[0][0])
            best_return = str(lis_tup[0][1])
        cola.metric(high_date,"",best_return,border=True)
        
        with colb:
            st.write("📉Lowest Return Day")
            cursor.execute(f"with cte2 as (select *,(LAG(CLOSE) OVER(ORDER BY DATE)-close)/close as daily_Return from `{tabel_name}`) select date,round(daily_return,2) as Lowest_return from cte2 where daily_return = (select min(daily_return) from cte2);")
            lis_tup1 = cursor.fetchall()
            low_date = "On "+ str(lis_tup1[0][0])
            lowest_return = str(lis_tup1[0][1])
        colb.metric(low_date,"",lowest_return,border=True)
             
        with colc:
            st.write("⚖️Average Return Day")
            cursor.execute(f"with cte3 as (select *,(LAG(CLOSE) OVER(ORDER BY DATE)-close)/close as daily_Return from aa ) select round(avg(daily_return),4) as average_return from cte3; ")
            lis_tup1 = cursor.fetchall()
            average_return = str(lis_tup1[0][0])
        colc.metric("","",average_return,border=True)
        
                
except Exception as e:
        print("Any error occured -",e)



