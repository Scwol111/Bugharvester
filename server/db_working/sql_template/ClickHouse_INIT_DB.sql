CREATE DATABASE IF NOT EXISTS BugHarvester ENGINE=Atomic;

CREATE TABLE IF NOT EXISTS BugHarvester.Projects(
    project_name String,
    project_description String,
    current_version String,
    maximal Int32
) ENGINE=ReplacingMergeTree ORDER BY (project_name)