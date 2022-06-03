CREATE DATABASE IF NOT EXISTS {{ project_name }} ENGINE=Atomic;

CREATE TABLE IF NOT EXISTS {{ project_name }}.Reports(
    id String,
    error_name String,
    version String,
    license String,
    techInfo String,
    traceback String,
    path_to_dump String,
    date Date
) ENGINE=ReplacingMergeTree ORDER BY (id);

CREATE TABLE IF NOT EXISTS {{ project_name }}.Errors(
    error_name String,
    language String,
    weight UInt32,
    reason String,
    solve String
) ENGINE=ReplacingMergeTree ORDER BY (errorName);

CREATE TABLE IF NOT EXISTS {{ project_name }}.Analyze(
    analyze_id String,
    analyzed_reports String,
    analyze_time Date
) ENGINE=ReplacingMergeTree ORDER BY (analyze_id, analyzed_reports);