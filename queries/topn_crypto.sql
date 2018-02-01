select cryptocurrency, count(*) c
from cryptocurrency_market_data
group by cryptocurrency
order by c desc
limit 10;
