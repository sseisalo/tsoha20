CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    user_type INTEGER,
    CONSTRAINT CHK_user CHECK (user_type<=1 AND user_type>=0)
);
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts,
    sent_at TIMESTAMP
);
