-- customers
DROP TABLE IF EXISTS users;

CREATE TABLE users; 
(
    email TEXT NOT NULL PRIMARY KEY,
    username TEXT ,
    password TEXT NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    verified BOOLEAN NOT NULL DEFAULT 0,
    admin BOOLEAN NOT NULL DEFAULT 0,
);


INSERT INTO customers (username, password, first_name, last_name, email)
VALUES
    ("sampleuser", "pbkdf2:sha256:260000$PWBqysgRgwZu29FI$c55cb445d03264b0977807abba784523ce7e26963174750ef61649512008b363", "sample", "user", "0831234567", '2003-02-26', "m", "14 Sunway drive", "Main Street Avenue", "Dublin", "Ireland", 50)
;

CREATE TABLE meetings (
    meeting_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    meeting_name TEXT NOT NULL,
    meeting_description TEXT DEFAULT "No description has been set",
    meeting_manager TEXT NOT NULL,
    meeting_location TEXT,
    meeting_setDate date DEFAULT "No date has been set",
    meeting_startTime time DEFAULT "No time has been set",
    meeting_dateSelectionRangeStart date,
    meeting_dateSelectionRangeEnd date,
    meeting_attendees TEXT,
    meeting_password TEXT,
    meeting_status TEXT DEFAULT "Upcoming",
    meeting_idealdates TEXT DEFAULT "No ideal dates have been identified yet",
    meeting_type TEXT NOT NULL,
    meeting_category TEXT,
    meeting_public BOOLEAN NOT NULL DEFAULT 0,
    meeting_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    meeting_updated_at TEXT
);
