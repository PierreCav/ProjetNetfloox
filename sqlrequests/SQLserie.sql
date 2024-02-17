SET search_path to principal;
SELECT *
FROM "filmview"
WHERE "runtimeMinutes" Is NOT null and "averageRating" 
is NOT NULL and "genres" is NOT NULL and "startYear" 
is NOT NULL and "isAdult" is NOT NULL and "titleType" is NOT NULL and "titleType" = 'tvSeries'
LIMIT 20000;