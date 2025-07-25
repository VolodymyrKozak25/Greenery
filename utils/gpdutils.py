from typing import Tuple
from shapely.geometry import Point
import geopandas as gpd

from static.tags import LINESTRING_WIDTH, POINT_AREA


def circle_area(center: Tuple[float, float], radius: int) -> gpd.GeoSeries:
    """
    Creates a circular area around a given center point with a specified radius.
    
    The function:
    1. Creates a GeoSeries containing the center point 
       using the EPSG:4326 CRS (WGS 84).
    2. Converts the GeoSeries to a projected CRS (EPSG:3043)
       to compute an accurate buffer in meters.
    3. Reprojects the resulting circular area back to the geographic CRS.
    
    :param center: The center point as a tuple (latitude, longitude).
    :param radius: The radius of the circle in meters.
    :return: A GeoSeries representing the circular area in the EPSG:4326 CRS.
    """
    center_point = Point(*center[::-1])
    obj = gpd.GeoSeries([center_point]).set_crs("EPSG:4326")
    area = obj.to_crs(3043).buffer(radius)
    return area.to_crs(4326)
    
    
def get_area(obj: gpd.GeoSeries) -> int:
    """
    Calculates the area of a GeoSeries object in square meters.

    :patam obj: A GeoSeries object containing geometric features 
                for which the area is to be calculated.
    :return: The total area of the geometries in the GeoSeries.
    """
    obj = obj.set_crs("EPSG:4326").to_crs(3043)
    if obj[0].geom_type == 'GeometryCollection':
        area = 0
        for item in obj[0].geoms:
            if item.area:
                area += item.area
            elif "LineString" in item.geom_type:
                area += item.length * LINESTRING_WIDTH
            elif item.geom_type == "Point":
                area += POINT_AREA 
            elif item.geom_type == "MultiPoint":
                area += len(item.geoms) * POINT_AREA
        return round(area)
    if "LineString" in obj[0].geom_type:
        return round(obj[0].length * LINESTRING_WIDTH)
    if "Point" in obj[0].geom_type:
        return round(len(obj[0].geoms) * POINT_AREA)
    area = obj.area
    try:
        return round(area.values[0])
    except ValueError:
        return round(obj.area.values[0])
    
