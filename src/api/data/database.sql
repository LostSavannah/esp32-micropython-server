DROP TABLE IF EXISTS Versions;
CREATE TABLE Versions(
    version_hash TEXT,
    version_epoch FLOAT,
    version_logic_path TEXT
);

DROP TABLE IF EXISTS Requests;
CREATE TABLE Requests(
    request_id TEXT,
    request_path TEXT,
    request_headers TEXT,
    request_body TEXT
);