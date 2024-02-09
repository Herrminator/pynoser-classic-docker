.mode column

-- https://www.sqlite.org/dbstat.html
with sizes as (
  select sum(length(text)) txs, sum(length(summary)) ds, sum(length(title)) ttx, count(*) na, feed_id
  from reader_article
  group by feed_id
  order by  txs desc
),
tot_sizes as (
  select txs + ds + ttx as tot, * from sizes
  order by tot desc
)
select * from tot_sizes s join reader_feed f on f.id = s.feed_id
