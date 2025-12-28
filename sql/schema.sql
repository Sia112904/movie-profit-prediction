-- =========================
-- Movie Profitability Database Schema
-- Normalized to 3NF
-- =========================

-- Drop tables if they exist (for reruns)
DROP TABLE IF EXISTS movie_genres;
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

