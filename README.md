# Static Monitor Map Generator

## Overview

This Python program generates a static PNG map that displays air quality monitors overlaid on ZIP Code Tabulation Areas (ZCTAs). Each monitor is color-coded by its Local Site Name and labeled via a legend. ZIP code polygons are filled for geographic context, and a basemap is included beneath the plotted data. This tool helps users visually assess monitor distribution in relation to ZIP codes.

## Features

* Loads ZIP boundaries from a U.S. Census TIGER/Line ZCTA shapefile
* Reads air quality monitor data from a CSV file with latitude/longitude
* Assigns each monitor site a unique color, with a matching legend
* Plots ZIP code boundaries with fill and label options
* Adds a background basemap using `contextily`
* Optionally filters ZIPs to include only those within a specified buffer of monitor locations
* Prints the included ZIP codes to the console
* Saves output as a static PNG map

## Input Files

### 1. Monitor CSV

The CSV file must include at least the following columns:

* `Local Site Name`
* `Site Latitude`
* `Site Longitude`

### 2. ZIP Code Shapefile (ZCTA)

Downloadable from the U.S. Census Bureau:
[https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)

The shapefile must include these components:

* `.shp`, `.shx`, `.dbf`, `.prj`, etc.

ZIP code areas are identified via the `ZCTA5CE10` field.

## ZIP Code Filtering

By default, the script includes only ZIP code polygons that:

* Contain at least one air monitor, or
* Are within a user-defined buffer (in meters) from ZIPs with a monitor

This helps keep the map clean and focused. For broader inclusion, increase the buffer size. To include all ZIPs regardless of monitor proximity, the filtering logic would need to be removed or modified.

When the map is generated, the script also prints the list of included ZIP codes to the terminal.

## Setup Instructions

### 1. Install Conda (if not installed)

Use Miniconda: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

### 2. Create and Activate a Conda Environment

```bash
conda create -n monitor-map python=3.9
conda activate monitor-map
```

### 3. Install Required Packages

```bash
conda install -c conda-forge geopandas matplotlib contextily adjusttext
```

## Running the Script

Run the script using the following command:

```bash
python map_monitors_static_outlined_dots_zipprint.py \
  --monitors monitor_capabilities_with_metadata.csv \
  --zips tl_2020_us_zcta510/tl_2020_us_zcta510.shp \
  --output static_monitor_map.png \
  --buffer 10000
```

### Parameters

* `--monitors`: Path to the monitor CSV file
* `--zips`: Path to the main `.shp` file in your ZCTA folder
* `--output`: Desired output filename for the PNG map
* `--buffer`: Buffer distance in meters (e.g. 10000 = 10km)

## Output

The script produces:

* A PNG image (`static_monitor_map.png`) showing:

  * ZIP boundaries (light blue fill)
  * Colored monitor dots with black outlines
  * A legend matching dot color to Local Site Name
  * A geographic basemap
* A printed list of all ZIP codes included in the map (in the terminal)

## Support

For questions, adjustments to the plotting behavior, or to extend the tool (e.g., interactive maps, filtering by site type), contact the script author or development team.

