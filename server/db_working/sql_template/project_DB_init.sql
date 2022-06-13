CREATE DATABASE IF NOT EXISTS {{ project_name }} ENGINE=Atomic;

CREATE TABLE IF NOT EXISTS {{ project_name }}.Reports(
    id String,
    error_name String,
    version String,
    license String,
    techInfo String,
    traceback String,
    path_to_dump String,
    date DateTime,
    analyze_id String,
    analyze_time DateTime
) ENGINE=ReplacingMergeTree ORDER BY (id);

CREATE TABLE IF NOT EXISTS {{ project_name }}.Errors(
    error_name String,
    language String,
    weight UInt32,
    reason String,
    solve String,
    description String
) ENGINE=ReplacingMergeTree ORDER BY (error_name)