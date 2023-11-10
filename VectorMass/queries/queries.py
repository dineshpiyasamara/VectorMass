
CHECK_COLLECTION_EXIST = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"

CREATE_COLLECTION = "CREATE TABLE {} (id TEXT PRIMARY KEY, document TEXT, embedding BLOB)"

INSERT_RECORD = "INSERT INTO {} (id, document, embedding) VALUES ({}, {}, {})"

GET_RECORD = "SELECT * FROM {} WHERE id={}"

CHECK_ID_EXIST = "SELECT COUNT(*) FROM {} WHERE id = {}"