CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    user_type INTEGER
);
CREATE TABLE channels (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    content TEXT,
    channel_id INTEGER REFERENCES channels,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    visible INTEGER
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts,
    sent_at TIMESTAMP,
    visible INTEGER
);
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    vote INTEGER
    user_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts,
    comment_id INTEGER REFERENCES comments,
    UNIQUE(user_id,post_id),
    UNIQUE(user_id,comment_id)
);
