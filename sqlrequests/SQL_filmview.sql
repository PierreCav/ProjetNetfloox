SELECT tb.tconst,
    tb."primaryTitle",
    tb."titleType",
    tb."isAdult",
    tb."startYear",
    tb."endYear",
    tb."runtimeMinutes",
    tb.genres,
    rt."averageRating",
    rt."numVotes",
    array_agg((tp.category || '_'::text) || replace(nb."primaryName", ' '::text, '_'::text)) AS "Cate&names"
FROM principal.title_basics tb
JOIN principal.title_ratings rt ON tb.tconst::text = rt.tconst::text
JOIN principal.title_principals tp ON tb.tconst::text = tp.tconst::text
JOIN principal.name_basics nb ON tp.nconst::text = nb.nconst::text
GROUP BY tb.tconst, rt."averageRating", rt."numVotes";