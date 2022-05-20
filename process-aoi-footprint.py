#A script to take the first tif file in each Raster subfolder of 'ref-data/labels'

import rasterio
from shapely.geometry.polygon import Polygon
import geopandas as gpd
import glob
import matplotlib.pyplot as plt


def raster_to_feature(raster_file):
    with rasterio.open(raster_file) as src:
        

        extent = src.bounds

        polygon = Polygon([(extent[0], extent[1]), (extent[2], extent[1]), (extent[2], extent[3]), (extent[0], extent[3])])

 
        gdf = gpd.GeoDataFrame(geometry=[polygon])
        gdf.crs = src.crs
            
        gdf = gdf.to_crs({'init': 'epsg:4269'})
        gdf.columns = ['geometry']

    return gdf


def main():

    gdf = gpd.GeoDataFrame()

    raster_paths = [f for f in glob.glob(r'ref-data/labels/*/Labels/Raster/')] 

    #iterate through all items in raster_paths, converting the first file to a feature and add to gdf
    for raster_path in raster_paths:
        raster_files = [f for f in glob.glob(raster_path + '*/*.tif')]

        raster_file = raster_files[0]

        raster_feature = raster_to_feature(raster_file)

        gdf = gdf.append(raster_feature)

    #plot gdf
    #gdf.plot()
    #plt.show()
    
    gdf = gdf.to_crs({'init': 'epsg:4269'})

    gdf.to_file('ref-data/aoi-footprint.gpkg', driver='GPKG')


if __name__ == '__main__':
    main()
