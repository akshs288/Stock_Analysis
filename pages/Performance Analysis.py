import streamlit as st


# Check if data is loaded
if "main_cursor" not in st.session_state:
    st.warning("⚠️ Please upload a file on the Summary page first")
    st.stop()
    
    
df = st.session_state["df"]
filename = st.session_state["file_name"]
cursor = st.session_state["main_cursor"]
tabel_name = st.session_state["tabel_name1"]

st.subheader("💹 Performance of stock")
st.write("")
st.write("")
st.write("")
col1,col2,col3 = st.columns(3)

with col1:
    st.write("📈Best Return Day")
    cursor.execute(f"with cte1 as (select *,(LAG(CLOSE) OVER(ORDER BY DATE)-close)/close as daily_Return from `{tabel_name}`) select date,round(daily_return,2) as Highest_return from cte1 where daily_return = (select max(daily_return) from cte1);")    
    lis_tup = cursor.fetchall()
    high_date = "On "+ str(lis_tup[0][0])
    best_return = str(lis_tup[0][1])
col1.metric(high_date,"",best_return,border=True)
        
        
with col2:
    st.write("📉Lowest Return Day")
    cursor.execute(f"with cte2 as (select *,(LAG(CLOSE) OVER(ORDER BY DATE)-close)/close as daily_Return from `{tabel_name}`) select date,round(daily_return,2) as Lowest_return from cte2 where daily_return = (select min(daily_return) from cte2);")
    lis_tup1 = cursor.fetchall()
    low_date = "On "+ str(lis_tup1[0][0])
    lowest_return = str(lis_tup1[0][1])
col2.metric(low_date,"",lowest_return,border=True)
             
             
with col3:
    st.write("⚖️Average Return Day")
    cursor.execute(f"with cte3 as (select *,(LAG(CLOSE) OVER(ORDER BY DATE)-close)/close as daily_Return from `{tabel_name}`) select round(avg(daily_return),4) as average_return from cte3;")
    lis_tup1 = cursor.fetchall()
    average_return = str(lis_tup1[0][0])
col3.metric("","",average_return,border=True)
        
st.subheader("💸 Volatility")
# df1 = pd.DataFrame()

