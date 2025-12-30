-- ============================
-- Average Profit by Genre
-- ============================

SELECT
    g.genre_name,
    ROUND(AVG(m.revenue - m.budget), 2) AS avg_profit
FROM movies m
JOIN movie_genres mg ON m.movie_id = mg.movie_id
JOIN genres g ON mg.genre_id = g.genre_id
WHERE m.budget > 0 AND m.revenue > 0
GROUP BY g.genre_name
ORDER BY avg_profit DESC;
-- ====================================
-- Top Profitable Genres by Decade
-- ====================================

SELECT
    (m.release_year / 10) * 10 AS decade,
    g.genre_name,
    ROUND(AVG(m.revenue - m.budget), 2) AS avg_profit
FROM movies m
JOIN movie_genres mg ON m.movie_id = mg.movie_id
JOIN genres g ON mg.genre_id = g.genre_id
WHERE m.release_year IS NOT NULL
  AND m.budget > 0
  AND m.revenue > 0
GROUP BY decade, g.genre_name
ORDER BY decade, avg_profit DESC;

-- ============================
-- Budget vs Revenue Analysis
-- ============================

SELECT
    CASE
        WHEN budget < 10000000 THEN 'Low Budget (<10M)'
        WHEN budget BETWEEN 10000000 AND 50000000 THEN 'Mid Budget (10M–50M)'
        ELSE 'High Budget (>50M)'
    END AS budget_category,
    COUNT(*) AS movie_count,
    ROUND(AVG(revenue), 2) AS avg_revenue,
    ROUND(AVG(revenue - budget), 2) AS avg_profit
FROM movies
WHERE budget > 0 AND revenue > 0
GROUP BY budget_category
ORDER BY avg_profit DESC;
-- ====================================
-- Query Plan BEFORE Indexing
-- ====================================

EXPLAIN QUERY PLAN
SELECT
    g.genre_name,
    AVG(m.revenue - m.budget)
FROM movies m
JOIN movie_genres mg ON m.movie_id = mg.movie_id
JOIN genres g ON mg.genre_id = g.genre_id
GROUP BY g.genre_name;

-- ============================
-- Index Optimization
-- ============================

CREATE INDEX IF NOT EXISTS idx_movies_movie_id
ON movies(movie_id);

CREATE INDEX IF NOT EXISTS idx_movie_genres_movie_id
ON movie_genres(movie_id);

CREATE INDEX IF NOT EXISTS idx_movie_genres_genre_id
ON movie_genres(genre_id);

CREATE INDEX IF NOT EXISTS idx_movies_release_year
ON movies(release_year);

-- ====================================
-- Query Plan AFTER Indexing
-- ====================================

EXPLAIN QUERY PLAN
SELECT
    g.genre_name,
    AVG(m.revenue - m.budget)
FROM movies m
JOIN movie_genres mg ON m.movie_id = mg.movie_id
JOIN genres g ON mg.genre_id = g.genre_id
GROUP BY g.genre_name;


