-- 初期スキーマ作成
CREATE SCHEMA IF NOT EXISTS job_data_analysis AUTHORIZATION "user";
CREATE SCHEMA IF NOT EXISTS metabase_internal AUTHORIZATION "user";


-- クレンジング前テーブル（生データ）
CREATE TABLE IF NOT EXISTS job_data_analysis.job_listings (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    location TEXT,
    salary TEXT,
    job_url TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- クレンジング後テーブル
-- tb_job_postings
CREATE TABLE IF NOT EXISTS job_data_analysis.tb_job_postings (
	id SERIAL PRIMARY KEY,
	company_name VARCHAR(100),
	location VARCHAR(100),
	salary INTEGER,
	prefecture varchar(10)
);


-- tb_skills
CREATE TABLE IF NOT EXISTS job_data_analysis.tb_skills(
	id SERIAL PRIMARY KEY,
	keyword VARCHAR(200) UNIQUE NOT NULL
);


-- tb_job_posting_skills
CREATE TABLE IF NOT EXISTS job_data_analysis.tb_job_postings_skills (
        job_id INTEGER REFERENCES job_data_analysis.tb_job_postings(id) ON DELETE CASCADE,
	skill_id INTEGER REFERENCES job_data_analysis.tb_skills(id) ON DELETE CASCADE,
	PRIMARY KEY (job_id, skill_id)
);


-- データのインポート
--/copy job_data_analysis.tb_job_postings(id,company_name, location, salary)
--FROM '/docker-entrypoint-initdb.d/data/job_tbl_posting_mask.csv'
--DELIMITER ',' CSV HEADER;

--/copy job_data_analysis.tb_skills(id, keyword)
--FROM '/docker-entrypoint-initdb.d/data/skills.csv'
--DELIMITER ',' CSV HEADER;

--/copy job_data_analysis.tb_job_posting_skills(job_id, skill_id)
--FROM '/docker-entrypoint-initdb.d/data/job_posting_skills.csv'
--DELIMITER ',' CSV HEADER;
