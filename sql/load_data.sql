-- =========================
-- Movie Profitability Database Tables + Indexes
-- =========================

-- Drop tables if they exist
DROP TABLE IF EXISTS movie_genres;
DROP TABLE IF EXISTS movie_companies;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS production_companies;

-- =========================
-- Production Companies
-- =========================
CREATE TABLE production_companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL UNIQUE
);

-- =========================
-- Movies
-- =========================
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    budget BIGINT,
    revenue BIGINT,
    runtime INT,
    popularity FLOAT,
    vote_average FLOAT,
    vote_count INT,
    company_id INT,
    CONSTRAINT fk_company
        FOREIGN KEY (company_id)
        REFERENCES production_companies(company_id)
        ON DELETE SET NULL
);

-- =========================
-- Genres
-- =========================
CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL UNIQUE
);

-- =========================
-- Movie ↔ Genre (Junction Table)
-- =========================
CREATE TABLE movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    CONSTRAINT fk_movie
        FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_genre
        FOREIGN KEY (genre_id)
        REFERENCES genres(genre_id)
        ON DELETE CASCADE
);

-- =========================
-- Movie ↔ Production Company (Junction Table)
-- =========================
CREATE TABLE movie_companies (
    movie_id INT NOT NULL,
    company_id INT NOT NULL,
    PRIMARY KEY (movie_id, company_id),
    CONSTRAINT fk_mc_movie
        FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_mc_company
        FOREIGN KEY (company_id)
        REFERENCES production_companies(company_id)
        ON DELETE CASCADE
);

-- =========================
-- Indexes for faster joins
-- =========================
CREATE INDEX idx_movie_genre_movie ON movie_genres(movie_id);
CREATE INDEX idx_movie_genre_genre ON movie_genres(genre_id);

CREATE INDEX idx_movie_company_movie ON movie_companies(movie_id);
CREATE INDEX idx_movie_company_company ON movie_companies(company_id);


-- Movies
INSERT INTO movies (title, release_year, budget, revenue, runtime, popularity, vote_average, vote_count, 
company_id)
VALUES
('Movie A', 2010, 1000000, 5000000, 120, 8.5, 7.2, 200, 1),
('Movie B', 2012, 2000000, 7000000, 130, 9.0, 6.8, 150, 2);

-- Genres
INSERT INTO genres (genre_name) VALUES
('Action'),
('Comedy'),
('Drama');

-- Movie Genres
INSERT INTO movie_genres (movie_id, genre_id) VALUES
(1, 1),
(1, 3),
(2, 2);

-- Production Companies
INSERT INTO production_companies (company_name) VALUES
('Company A'),
('Company B');

-- Movie Companies
INSERT INTO movie_companies (movie_id, company_id) VALUES
(1, 1),
(2, 2);

