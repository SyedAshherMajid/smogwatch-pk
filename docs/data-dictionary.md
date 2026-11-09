# Data Dictionary

> Planned schema. Finalised as the transform and validation stages are built.

## `silver/observations` (one row per point per hour)

| Column | Type | Description |
|--------|------|-------------|
| `point_id` | string | Stable point ID, e.g. `lahore_031_744` |
| `city` | string | City name |
| `lat`, `lon` | float64 | Point coordinates (WGS84) |
| `geohash5` | string | Geohash, precision 5 (~4.9 km cell) |
| `geohash4` | string | Geohash, precision 4 (~39 × 20 km cell) |
| `ts_utc` | timestamp (UTC) | Start of the hour |
| `ts_pkt` | timestamp | Same hour in Pakistan Standard Time (UTC+5), display only |
| `pm2_5`, `pm10` | float64 | Particulate matter, µg/m³ |
| `no2`, `o3`, `co`, `dust` | float64 | µg/m³ |
| `us_aqi_source` | int | US AQI as provided by Open-Meteo |
| `aqi_pm25_calc` | int | AQI calculated by this pipeline from PM2.5 (EPA breakpoints) |
| `aqi_category` | string | Good / Moderate / Unhealthy for Sensitive Groups / Unhealthy / Very Unhealthy / Hazardous |
| `temperature_c` | float64 | Air temperature at 2 m, °C |
| `humidity_pct` | float64 | Relative humidity at 2 m, % |
| `wind_speed_kmh` | float64 | Wind speed at 10 m, km/h |
| `wind_dir_deg` | float64 | Wind direction at 10 m, degrees |
| `precip_mm` | float64 | Precipitation, mm |
| `run_id` | string | Pipeline run that wrote the row |
| `ingested_at` | timestamp (UTC) | Write time |

## `gold/catalog_p5` (one row per geohash cell per hour)

| Column | Description |
|--------|-------------|
| `geohash5`, `city`, `centroid_lat`, `centroid_lon` | The cell |
| `ts_utc`, `ts_pkt` | The hour |
| `pm2_5_mean`, `pm2_5_max`, `pm10_mean` | Pollution statistics |
| `aqi_max`, `aqi_category` | Worst AQI in the cell |
| `temperature_c_mean`, `humidity_pct_mean`, `wind_speed_kmh_mean` | Weather statistics |
| `n_points` | Number of points aggregated (completeness signal) |
| `pipeline_version`, `run_id` | Lineage |

`gold/catalog_p4` has the same columns aggregated to precision 4.

## Data quality rules

### Row level (failing rows → quarantine)

| Rule | Check |
|------|-------|
| Required fields | `point_id`, `ts_utc`, `geohash5`, `pm2_5` not null |
| PM2.5 | 0 ≤ value ≤ 1000 |
| PM10 | 0 ≤ value ≤ 2000 |
| Temperature | −30 ≤ value ≤ 60 °C |
| Humidity | 0 ≤ value ≤ 100 |
| Wind speed | 0 ≤ value ≤ 200 km/h |
| AQI | 0 ≤ value ≤ 500 |
| Geohash | matches `^[0-9b-hjkmnp-z]{5}$` |
| Coordinates | inside Pakistan bounding box (23.5–37.5 N, 60.5–78 E) |

### Run level (failing → run fails)

| Check | Threshold |
|-------|-----------|
| Uniqueness | no duplicate (`point_id`, `ts_utc`) |
| Completeness | ≥ 95% of expected points per hour |
| Quarantine rate | ≤ 20% |
| Freshness | newest `ts_utc` ≤ 2 h old |
| Schema drift | expected fields present in API response |

### Warnings (logged only)

- `pm2_5 > pm10`
- Calculated AQI differs from source AQI by more than 50
- Identical value repeated for 6+ consecutive hours
