import argparse
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
from adjustText import adjust_text

PROJECTED_EPSG = 3857  # Web Mercator for contextily basemaps

def load_monitors(csv_path):
    df = pd.read_csv(csv_path)
    geometry = [Point(xy) for xy in zip(df["Site Longitude"], df["Site Latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf.to_crs(epsg=PROJECTED_EPSG)

def load_zips(shapefile_path, monitors_gdf, buffer_distance=0):
    zips = gpd.read_file(shapefile_path).to_crs(epsg=PROJECTED_EPSG)
    zip_hits = gpd.sjoin(zips, monitors_gdf, how="inner", predicate="contains")
    relevant_zip_codes = zip_hits["ZCTA5CE10"].unique()
    relevant_zips = zips[zips["ZCTA5CE10"].isin(relevant_zip_codes)]
    if buffer_distance > 0:
        buffer_geom = relevant_zips.geometry.unary_union.buffer(buffer_distance)
        zips = zips[zips.intersects(buffer_geom)]
    else:
        zips = relevant_zips
    print("\nIncluded ZIP codes:")
    print(sorted(zips["ZCTA5CE10"].unique()))
    return zips

def plot_static_map(monitors_gdf, zips_gdf, output_image):
    fig, ax = plt.subplots(figsize=(14, 12))

    # Plot ZIPs with fill
    zips_gdf.plot(ax=ax, edgecolor='gray', facecolor='lightblue', alpha=0.5)

    # Plot monitors with custom colors and black outlines
    site_names = monitors_gdf["Local Site Name"].unique()
    color_map = {
        "Lawrenceville": "#404040",
        "Liberty": "#ff7f0e",
        "North Braddock": "#2ca02c",
        "Harrison": "#d62728",
        "Parkway East Near-Road": "#9467bd",
        "Avalon": "#8c564b",
        "South Fayette": "#e377c2",
        "North Park": "#7f7f7f",
        "Clairton": "#bcbd22",
        "Flag Plaza": "#A9A9A9",
        "Manchester": "#1f78b4",
        "Glassport": "#17becf",
        "Lincoln": "#ffbb78",
        "Bridgeville": "#f7b6d2"
    }

    for name in site_names:
        site_data = monitors_gdf[monitors_gdf["Local Site Name"] == name]
        site_data.plot(
            ax=ax,
            color=[color_map.get(name, "black")],
            markersize=50,
            label=name,
            edgecolor="black",
            linewidth=0.5
        )

    # Add ZIP labels
    zips_gdf['centroid'] = zips_gdf.geometry.centroid
    for _, row in zips_gdf.iterrows():
        ax.text(row['centroid'].x, row['centroid'].y, row['ZCTA5CE10'],
                fontsize=8, ha='center', va='center', color='navy')

    # Basemap
    ctx.add_basemap(ax, crs=monitors_gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron)

    # Styling
    ax.set_title("Air Quality Monitors and ZIP Code Boundaries", fontsize=16)
    ax.set_xlabel("Easting (meters)")
    ax.set_ylabel("Northing (meters)")
    ax.grid(True)
    ax.legend(title='Local Site Name', fontsize=8, title_fontsize=9, loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()

    if output_image:
        plt.savefig(output_image, dpi=300)
    else:
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Static map of air quality monitors and ZIP codes.")
    parser.add_argument("--monitors", required=True, help="Path to monitor CSV file")
    parser.add_argument("--zips", required=True, help="Path to ZIP shapefile (.shp)")
    parser.add_argument("--output", help="Path to output PNG file")
    parser.add_argument("--buffer", type=int, default=2000, help="Buffer (in meters) around ZIPs with monitors")

    args = parser.parse_args()
    monitors = load_monitors(args.monitors)
    zips = load_zips(args.zips, monitors, buffer_distance=args.buffer)
    plot_static_map(monitors, zips, args.output)
