CREATE TABLE IF NOT EXISTS title_ratings (
    tconst VARCHAR(255) PRIMARY KEY,
    averageRating DOUBLE,
    numVotes INT
);


LOAD DATA LOCAL INFILE './tmp/title.ratings.tsv' INTO
TABLE title_ratings FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 LINES (
    tconst,
    averageRating,
    numVotes
);