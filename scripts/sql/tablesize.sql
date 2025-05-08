.mode column

select name, sum(pgsize) as size from dbstat
group by name
order by size desc, name asc
;
