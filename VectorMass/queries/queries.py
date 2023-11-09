
check_collection_exist = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"

create_collection = "CREATE TABLE {} (id TEXT PRIMARY KEY, document TEXT, embedding BLOB)"