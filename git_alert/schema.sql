CREATE TABLE paths (
  id INTEGER PRIMARY KEY,
  path BLOB NOT NULL -- Compressed directory path
);

CREATE TABLE status (id INTEGER PRIMARY KEY, desc TEXT NOT NULL);

CREATE TABLE projects (
  id INTEGER PRIMARY KEY,
  path_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  status_id INTEGER,
  FOREIGN KEY (path_id) REFERENCES paths (id)
);

-- make status_id nullable as it is added later
-- fill status with values to be referenced
