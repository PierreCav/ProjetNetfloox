SET search_path to testmohammed;
select *
from name_basics
where "primaryName"='Fred Astaire'
;

ALTER TABLE name_basics 
ALTER COLUMN nconst TYPE varchar(10) USING nconst::varchar(10)
;

select "primaryName", LENGTH("primaryName") AS longueur
from name_basics

select max(LENGTH("primaryName")) AS longueur
from name_basics

select *
from name_basics
where "birthYear"  = '\N'

update name_basics 
set "birthYear"  = null  
where "birthYear"  = '\N'

update name_basics 
set "deathYear"  = null  
where "deathYear"  = '\N'
;

ALTER TABLE testmohammed.name_basics ALTER COLUMN "primaryName" TYPE varchar(50) USING "primaryName"::varchar(50);
ALTER TABLE testmohammed.name_basics ALTER COLUMN "birthYear" TYPE int2 USING "birthYear"::int2;
ALTER TABLE testmohammed.name_basics ALTER COLUMN "deathYear" TYPE int2 USING "deathYear"::int2;

update name_basics 
set "age" = "deathYear" -"birthYear" 
;

create view "AGE"as 
select "primaryName" ,"birthYear" ,"deathYear" ,  ("deathYear"-"birthYear")as age
from name_basics
where "deathYear" is not null and "birthYear" is not null
order by "age" desc
; 

select *
from title_principals
left join name_basics on title_principals.tconst = name_basics.nconst
where name_basics.nconst isnull 
;

select count(*)
from title_principals
where nconst in 
(select nconst from name_basics);


update title_principals
set nconst =NULL
where nconst not in
(select nconst from name_basics);

delete
from title_ratings 
where title_ratings.tconst not in
(select tconst from title_basics);
