# Changelog

## 1.0.0 (2025-06-17)

### Feat

- apply country filtering during import
- add ability to skip downloading file if path is provided
- replace subprocess/awk with csv
- Added country table, renamed geo column
- voronoi generator

### Fix

- reverted country_code column name change
- added index on geocoding.country_code

### Refactor

- fix ruff lint issues for voronoi generator

## 0.2.1 (2025-02-17)

### Fix

- replace deprecated importlib .path method with .files() API

## 0.2.0 (2025-02-11)

### Fix

- add context managers via __enter__ methods, update usage
- do not default use test db conn, error on missing vars

### Refactor

- use encode/httpcore unasync impl, restructure
- fallback to env vars for NearestCity.connect(), esp in tests
- export main classes in __init__.__all__ for pg_nearest_city pkg
- lint all, add extra pre-commit hooks, allow env var db initialisation

## 0.1.0 (2025-02-08)

### Feat

- re-added usage with context manager
- added sync code generation with unasync
- init status and logger
- async wrapper
- auto init when used with context manager
- initialization checks
- added support for external db connections and for closing internal ones
- delete voronoi file after init to lower disk usage
- gzipped files to lower disk usage
- first commit, add stub project, license

### Fix

- added pre-generated sync files
- return on invalid table structure
- changed test dbconfig to match compose file
- moved check for init files existance when they're actually needed

### Refactor

- moved shared logic into base class
