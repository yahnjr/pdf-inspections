import pandas as pd
import geopandas as gpd
import fiona

input_fc = r"P:\21713-North Plains\GIS\mxd\21713 North Plains.gdb\ADA_RampInspections"
output_shapefile = (
    r"P:\21713-North Plains\GIS\Infrastructure\Utilities\ADA_Ramp_Inspections.shp"
)
prefix_to_remove = "combined_output_csv_"

gdb_path = "P:/21713-North Plains/GIS/mxd/21713 North Plains.gdb"
input_feature = "ADA_RampInspections"
layers = fiona.listlayers(gdb_path)

gdf = gpd.read_file(gdb_path, layer=input_feature)

for field in gdf.columns:
    print(field)

gdf.columns = [
    col[len(prefix_to_remove) :] if col.startswith(prefix_to_remove) else col
    for col in gdf.columns
]

datetime_fields = gdf.select_dtypes(include=["datetime"]).columns
gdf = gdf.drop(columns=datetime_fields)

for field in gdf.columns:
    print(field)

gdf.to_file(output_shapefile)
