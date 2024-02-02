DROP SCHEMA IF EXISTS test1 CASCADE;
CREATE SCHEMA test1;
SET search_path to test1;
-- DROP SCHEMA IF EXISTS test2 CASCADE;
-- CREATE SCHEMA test2;
-- SET search_path to test2;
-- DROP SCHEMA IF EXISTS test3 CASCADE;
-- CREATE SCHEMA test3;
-- SET search_path to test3;

DROP TABLE IF EXISTS name_basics;
CREATE TABLE "name_basics"
(
  "nconst" text,
  "primaryName" text,
  "birthYear" text,
  "deathYear" text,
  "primaryProfession" text,
  "knownForTitles" text
);

DROP TABLE IF EXISTS title_basics;
CREATE TABLE title_basics
(
  "tconst" text NOT NULL,
  "titleType" text,
  "primaryTitle" text,
  "originalTitle" text,
  "isAdult" text,
  "startYear" text,
  "endYear" text,
  "runtimeMinutes" text,
  "genres" text
);

DROP TABLE IF EXISTS title_principals;
CREATE TABLE title_principals
(
  "tconst" text NOT NULL,
  "ordering" int2 NOT NULL,
  "nconst" text,
  "category" text,
  "job" text,
  "characters" text
);

DROP TABLE IF EXISTS title_crew;
CREATE TABLE title_crew
(
  "tconst" text,
  "directors" text,
  "writers" text
);

DROP TABLE IF EXISTS title_akas;
CREATE TABLE title_akas
(
  "titleId" text,
  "ordering" int,
  "title" text,
  "region" text,
  "language" text,
  "types" text,
  "attributes" text,
  "isOriginalTitle" text
);

DROP TABLE IF EXISTS title_episode;
CREATE TABLE title_episode
(
  "tconst" text,
  "parentTconst" text,
  "seasonNumber" text,
  "episodeNumber" text
);

DROP TABLE IF EXISTS title_ratings;
CREATE TABLE title_ratings
(
  "tconst" text,
  "averageRating" text,
  "numVotes" text
);

\COPY name_basics FROM PROGRAM 'curl -s https://datasets.imdbws.com/name.basics.tsv.gz | zcat | head -50000' with (format csv, delimiter E'\t', header TRUE, quote E'\b');
\COPY title_basics FROM PROGRAM 'curl -s https://datasets.imdbws.com/title.basics.tsv.gz | zcat | head -50000' with (format csv, delimiter E'\t', header TRUE, quote E'\b');
\COPY title_principals FROM PROGRAM 'curl -s https://datasets.imdbws.com/title.principals.tsv.gz | zcat | head -50000' with (format csv, delimiter E'\t', header TRUE, quote E'\b');
\COPY title_crew FROM PROGRAM 'curl -s https://datasets.imdbws.com/title.crew.tsv.gz | zcat | head -50000' with (format csv, delimiter E'\t', header TRUE, quote E'\b');
\COPY title_akas FROM PROGRAM 'curl -s https://datasets.imdbws.com/title.akas.tsv.gz | zcat | head -50000' with (format csv, delimiter E'\t', header TRUE, quote E'\b');
\COPY title_episode FROM PROGRAM 'curl -s https://datasets.imdbws.com/title.episode.tsv.gz | zcat | head -50000' with (format csv, delimiter E'\t', header TRUE, quote E'\b');
\COPY title_ratings FROM PROGRAM 'curl -s https://datasets.imdbws.com/title.ratings.tsv.gz | zcat | head -50000' with (format csv, delimiter E'\t', header TRUE, quote E'\b');
