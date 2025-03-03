\c clickstream_db;  -- Connect to the database

-- Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clickstream Events Table
CREATE TABLE clickstream_events (
    event_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    event_type VARCHAR(50) NOT NULL, -- e.g., page_view, add_to_cart, purchase
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_id INT,
    session_id VARCHAR(255)
);

-- Product Recommendations Table
CREATE TABLE product_recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    recommended_product_id INT,
    confidence_score FLOAT
);
