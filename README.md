# Movie Profit Prediction Project

A data project that predicts movie profitability using budget, genre, and other movie data.

## What This Project Does

Takes messy movie data and turns it into predictions about how much money a movie might make.

## The Challenge

Movie data is often:
- Messy and incomplete
- Hard to analyze directly
- From different sources with different formats

**Goal:** Predict movie profit before release.

## How It Works

### 1. Data Preparation
- Load movie data (budget, revenue, genres, dates)
- Clean up missing or bad data
- Calculate: `profit = revenue - budget`

### 2. Feature Creation
- Extract year and month from release dates
- Turn genres into numbers computers can understand
- Save this format for future predictions

### 3. Database Setup
- Organize data into separate tables:
  - Movies
  - Genres
  - Which movies have which genres
- Make queries run faster with indexes

### 4. Machine Learning
**Target:** Predict profit amount

**Models Tested:**
1. Random Forest
2. Gradient Boosting

**Results:**
- Gradient Boosting worked better
- Still makes mistakes (about $91 million on average)
- Budget is the most important factor

## Model Performance

**Comparison:**
- **Random Forest:** 30% accuracy
- **Gradient Boosting:** 40% accuracy ✓ (chosen)

**Key Findings:**
- Budget matters most
- Action/Adventure movies tend to be more profitable
- Model works best for mid-budget movies

## Project Structure
project/
├── data/ # Saved models & results
├── src/ # Python scripts
├── notebooks/ # Data exploration
└── README.md

## How to Use

1. Train model: `python src/train.py`
2. Make predictions: `python src/predict.py`

Predictions are saved to `data/results/predicted_profits.csv`

## Tools Used

- **Python** (pandas, scikit-learn)
- **SQL** (for organizing data)
- **Git** (for version control)

## Key Takeaways

1. Bigger budgets → usually bigger profits (and bigger risks)
2. Genre affects profitability
3. Clean, organized data makes better predictions
4. Simple models can still provide useful insights
