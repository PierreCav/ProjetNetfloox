SET search_path to principal;
select title_basics."tconst","titleType","isAdult","startYear","endYear","runtimeMinutes","genres",
"category","seasonNumber","episodeNumber"
from title_basics
join title_principals on title_basics."tconst" = title_principals."tconst"
join title_episode on title_basics."tconst" = title_episode."parentTconst";
