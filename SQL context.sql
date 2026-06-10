use stock_analysis;
create table if not exists user_ (Date DATETIME,Open FLOAT,High FLOAT,Low float,Close float,Adj_Close float, Volume INT);

-- I want to check volatility for particular year...


-- Final query for volatility
create view daily_return as
select year(date) as _year,daily_return from(
select *,(LAG(CLOSE) OVER(ORDER BY DATE)-close)/close as daily_Return
from aame) t;

select * from (
select year(date) as _year, round((stddev(daily_return)* sqrt(252))*100,2) as volatility
from (select *,(LAG(CLOSE) OVER(ORDER BY DATE)-close)/close as daily_Return
from aame) t
group by _year) x 
where (x.volatility = (select max(volatility) from x)) or (x.volatility = (select min(volatility) from x));


select * from aa;

select date, daily_return from(
select *,(LAG(CLOSE) OVER(ORDER BY DATE)-close)/close as daily_Return, row_number() over(order by date) as rank_number
from aa) t
where t.rank_number > 1 and (daily_return = (select max(t.daily_return) from aa));



select *,row_number() over(order by volatility) as asc_,row_number() over(order by volatility desc) as desc_ from(
select _year, round((stddev(daily_return)* sqrt(252))*100,2) as volatility
from daily_return
group by _year) t;

with vol as (
select _year, round((stddev(daily_return)* sqrt(252))*100,2) as volatility
from daily_return
group by _year
)
select max(volatility),min(volatility) from vol;



