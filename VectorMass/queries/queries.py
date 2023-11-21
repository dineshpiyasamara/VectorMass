
CHECK_COLLECTION_EXIST = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"

CREATE_COLLECTION = "CREATE TABLE %(collection_name)s (id TEXT PRIMARY KEY, document TEXT, embedding BLOB)"

INSERT_RECORD = "INSERT INTO %(collection_name)s (id, document, embedding) VALUES (%(id)s, %(document)s, %(embedding)s)"

GET_RECORD = "SELECT * FROM %(collection_name)s WHERE id=%(id)s"

GET_ALL_RECORDS = "SELECT * FROM %(collection_name)s"

CHECK_ID_EXIST = "SELECT COUNT(*) FROM %(collection_name)s WHERE id = %(id)s"

UPDATE_RECORD = "UPDATE %(collection_name)s SET document = %(document)s, embedding = %(embedding)s WHERE id = %(id)s"

DELETE_RECORD = "DELETE FROM %(collection_name)s WHERE id = %(id)s"