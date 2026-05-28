# Data Directory

## Structure
- `raw/` - Raw sensor data (CSV, binary)
- `processed/` - Processed and cleaned data
- `archival/` - Archived historical data with checksums

## Data Retention
- Raw data: 7 days
- Processed data: 30 days
- Archival data: 365 days

## Security
All archival data includes SHA-256 checksums for tamper evidence.
