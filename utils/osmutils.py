import geopandas as gpd
import osmnx as ox
import folium
from typing import Dict, List, Tuple, Union

from static.tags import TAGS
from .gpdutils import get_area


def get_zoom(radius: int) -> int:
    """
    Calculates start zoom for the folium map.

    :param radius: Radius (in meters).
    :return: Start zoom.
    """
    if radius <= 250:
        return 16
    if radius <= 500:
        return 15
    if radius <= 1000:
        return 14
    if radius <= 2000:
        return 13
    return 10
    
    
def get_tagname(tag: str) -> str:
    """
    
    """
    for name, tags in TAGS.items():
        if tag == tags[1]:
            return name


def create_map(location: Tuple[float, float], 
               address: str, radius: int) -> folium.Map:
    """
    Creates an interactive map.

    :param location: The latitude and longitude.
    :param address: The address of location.
    :param radius: Need to calculate start zoom of the map. 
    :return: An interactive map with center in location.
    """
    zoom = get_zoom(radius)
    map_obj = folium.Map(location=location, zoom_start=zoom)
    folium.Marker(location=location, 
                  icon=folium.Icon(color='red'),
                  popup=address, 
                  tooltip=address).add_to(map_obj)
    return map_obj
    
    
def add_object(map_obj: folium.Map, 
               obj: gpd.GeoSeries | gpd.GeoDataFrame) -> None:
    """
    Adds and visualizes a GeoSeries or GeoDataFrame on the interactive map.

    :param map_obj: An interactive map.
    :param obj: The spatial data to be visualized.
    :return: None.
    """
    folium.GeoJson(obj.__geo_interface__, name="geojson").add_to(map_obj)
    
    
    
def update_tags(tags: Dict[str, List[str]], 
                tag: str, selected: bool) -> None:
    """
    Updates a list of tags within groups based on user selection by appending
    or removing a tag from the appropriate group in the `tags` dictionary.

    :param tags: A dictionary containing tag groups as keys 
                 and list of tags as values.
    :param tag: The identifier of the tag to be added or removed.
                It must exist in the global `TAGS` dictionary, 
                which maps tags to their corresponding groups.
    :param selected: If True, the tag will be added to the appropriate group.
                     If False, the tag will be removed from the group.
    :return: None
    """
    taggroup, tagname = TAGS.get(tag)
    if selected and tagname not in tags[taggroup]:
        tags[taggroup].append(tagname)
    if not selected and tagname in tags[taggroup]:
        tags[taggroup].remove(tagname)
        
        
def get_greenery(territory: Union[gpd.GeoSeries, gpd.GeoDataFrame], 
                 tags: Dict[str, List[str]]) -> gpd.GeoDataFrame:
    """
    Retrieve greenery features within a specified territory using OSM data.

    :param territory: A GeoSeries or GeoDataFrame representing the territory
                      polygon(s). Must have a valid CRS and contain a single
                      or multiple polygons.
    :param tags: Dictionary of OSM tags to filter greenery features.
    :return: A GeoDataFrame of greenery features in the input territory.
    """
    greenery_gdf = ox.features_from_polygon(territory.item(), tags)
    intersection_gdf = greenery_gdf.unary_union.intersection(territory)
    return intersection_gdf
    
    
def get_details(territory: Union[gpd.GeoSeries, gpd.GeoDataFrame], 
                 tags: Dict[str, List[str]]) -> gpd.GeoDataFrame:
    """
    Retrieve greenery features within a specified territory using OSM data.

    :param territory: A GeoSeries or GeoDataFrame representing the territory
                      polygon(s). Must have a valid CRS and contain a single
                      or multiple polygons.
    :param tags: Dictionary of OSM tags to filter greenery features.
    :return: A GeoDataFrame of greenery features in the input territory.
    """
    details = {}
    for group, taglist in tags.items():
        for tag in taglist:
            temp_tags = {group: tag}
            try:
                objects = ox.features_from_polygon(territory.item(), temp_tags)
                intersection = objects.unary_union.intersection(territory)
                details[tag] = get_area(intersection)
            except:
                pass
    return details
    



