SET search_path to principal;
SELECT "primaryTitle", "averageRating", "titleType", "startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers" , array_agg(name_basics."primaryName") AS director_names
FROM title_basics 
JOIN title_ratings ON title_basics."tconst" = title_ratings."tconst"
JOIN title_crew ON title_basics."tconst" = title_crew."tconst"
JOIN name_basics ON name_basics.nconst = ANY(string_to_array(title_crew."directors", ','))
GROUP BY "primaryTitle", "averageRating", "titleType", "startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers"
LIMIT 2;