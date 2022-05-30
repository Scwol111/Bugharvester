CREATE DATABASE IF NOT EXISTS BugHarvester ENGINE=Atomic;

CREATE TABLE IF NOT EXISTS BugHarvester.Reports(
    projectName String,
    id String,
    error String,
    version String,
    license String,
    techInfo String,
    traceback String,
    dump String,
    date Date
) ENGINE=ReplacingMergeTree ORDER BY (projectName, id);

CREATE TABLE IF NOT EXISTS BugHarvester.Errors(
    errorName String,
    language String,
    weight UInt32,
    reason String,
    solve String
) ENGINE=ReplacingMergeTree ORDER BY (errorName);

CREATE TABLE IF NOT EXISTS BugHarvester.Projects(
    projectName String,
    version String,
    info String
) ENGINE=ReplacingMergeTree ORDER BY (projectName);
