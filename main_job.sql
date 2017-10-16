CREATE TABLE IF NOT EXISTS job
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20),
    chat_id VARCHAR(20),
    type VARCHAR(20),
    track_id VARCHAR(20),
    content TEXT,
    status VARCHAR(10),
    date DATETIME,
    done BOOLEAN
)