SET search_path to principal;
SELECT *
FROM "filmview"
WHERE "runtimeMinutes" Is NOT null and "averageRating" 
is NOT NULL and "genres" is NOT NULL and "startYear" 
is NOT NULL and "isAdult" is NOT NULL and "titleType" is NOT NULL and "titleType" = 'movie' and "isAdult" = 0 ORDER BY "numVotes" DESC NULLS LAST, "averageRating" DESC NULLS LAST
LIMIT 20000;