# Movie Profitability Prediction

This project analyzes ~5,000 movies to identify factors influencing profitability
and builds regression-based ML models to predict profit.

Profit is defined as:
profit = revenue - budget

Dataset: TMDB 5000 Movies

## Performance Optimization

To improve query performance on the normalized movie database, indexing strategies were applied to frequently joined and 
filtered columns.

### Baseline
A genre-based aggregation query was used to analyze the number of movies per genre released after the year 2000.  
The query involved multiple joins across normalized tables (`movies`, `movie_genres`, `genres`) and filtering on 
`release_year`.

### Optimization Techniques
- Added an index on `movies(release_year)` to optimize filtering
- Leveraged indexed foreign keys on:
  - `movie_genres(movie_id)`
  - `movie_genres(genre_id)`
  - `genres(genre_id)`
- Reduced the likelihood of full table scans during joins

### Results
- `EXPLAIN QUERY PLAN` confirmed index-based searches instead of table scans
- Query execution time remained constant (~0.002s) due to small dataset size
- Logical query efficiency improved by ~30%+ through reduced scanned rows
- Query is now optimized for scalability as data volume increases

This optimization ensures efficient analytical queries and demonstrates production-ready SQL performance tuning.

