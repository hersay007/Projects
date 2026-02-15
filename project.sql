-- Create Table
CREATE TABLE movies (
    id INT,
    title VARCHAR(255),
    budget BIGINT,
    revenue BIGINT,
    popularity FLOAT,
    runtime INT,
    release_year INT,
    genres VARCHAR(255),
    vote_count INT
);

-- 1️⃣ Budget vs Popularity Correlation
SELECT 
    CORR(budget, popularity) AS budget_popularity_correlation
FROM movies
WHERE budget IS NOT NULL;

-- 2️⃣ Average Popularity by Budget Category
SELECT 
    CASE 
        WHEN budget >= (SELECT AVG(budget) FROM movies) THEN 'High Budget'
        ELSE 'Low Budget'
    END AS budget_category,
    AVG(popularity) AS avg_popularity
FROM movies
GROUP BY budget_category;

-- 3️⃣ Runtime Impact on Popularity
SELECT 
    CASE 
        WHEN runtime < 100 THEN 'Short'
        WHEN runtime BETWEEN 100 AND 200 THEN 'Medium'
        ELSE 'Long'
    END AS runtime_category,
    AVG(popularity) AS avg_popularity
FROM movies
GROUP BY runtime_category;

-- 4️⃣ Profit Calculation
SELECT 
    title,
    (revenue - budget) AS profit
FROM movies
ORDER BY profit DESC
LIMIT 10;

-- 5️⃣ Top 10 Revenue Movies
SELECT 
    title,
    revenue,
    budget,
    popularity,
    runtime
FROM movies
ORDER BY revenue DESC
LIMIT 10;

-- 6️⃣ Most Frequent Genres
SELECT 
    genres,
    COUNT(*) AS genre_count
FROM movies
GROUP BY genres
ORDER BY genre_count DESC;
