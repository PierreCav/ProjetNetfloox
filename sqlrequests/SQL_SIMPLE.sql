SET search_path to principal;
SELECT "primaryTitle", 
        "averageRating", 
        "titleType", 
        "startYear", 
        "runtimeMinutes", 
        "genres", 
        "isAdult", 
        "directors", 
        "writers"
FROM title_basics 
JOIN title_ratings ON title_basics."tconst" = title_ratings."tconst"
JOIN title_crew ON title_basics."tconst" = title_crew."tconst"
LIMIT 10;