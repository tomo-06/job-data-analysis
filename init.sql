CREATE TABLE IF NOT EXISTS job_listings (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    location TEXT,
    salary TEXT,
    job_url TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
