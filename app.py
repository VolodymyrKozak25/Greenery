import streamlit as st
import folium
import warnings
from streamlit_folium import folium_static

from utils import osmutils
from utils.geoutils import get_location
from utils.gpdutils import circle_area, get_area
from static.tags import TAGS, TAG_GROUPS
from static.addresses import DISTRICTS


st.session_state.setdefault("map_obj", None)
st.session_state.setdefault("tags", {tag: False for tag in TAGS})

# SIDEBAR
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        min-width: 30%;
        max-width: 30%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

tab = st.sidebar.radio("Оберіть вид досліджуваної території:", 
                      ["Кругова область", "Адміністративний район м. Львів"])

if tab == "Кругова область":
    address = st.sidebar.text_input("Адреса")
    radius = st.sidebar.number_input("Радіус охоплення (у метрах)", 
        	                     min_value=0, 
        	                     value=500, 
        	                     step=100, 
        	                     format="%d")
else:
    address = st.sidebar.selectbox("Оберіть район:", DISTRICTS, index=0)
    radius = None
                                 
for tag in st.session_state.tags:
    st.session_state.tags[tag] = st.sidebar.checkbox(
                                        tag, value=st.session_state.tags[tag])

# CALCULATION
if st.sidebar.button("Обчислити рівень озеленення території"):
    st.session_state.update({"map_obj": None})
    tags = {group: [] for group in TAG_GROUPS}
    success, location = True, None
    if radius is not None:
        try:
            location = get_location(address)
        except:
            success = False
            st.write('Геокодер недоступний. Перевірте підключення '
                     'до мережі або спробуйте пізніше')
    if success:
        if location is not None:
            territory = circle_area(location, radius)
        else:
            territory = osmutils.district_area(f"{address} район")
            location = territory.geometry.union_all().centroid.coords[0][::-1]																																																																																																																									
        territory_area = get_area(territory)
        map_obj = osmutils.create_map(location, address, radius)
        osmutils.add_object(map_obj, territory) 
        for tag, selected in st.session_state.tags.items():
            osmutils.update_tags(tags, tag, selected)
        try:
            greenery = osmutils.get_greenery(territory, tags)
            osmutils.add_object(map_obj, greenery)
            greenery_area = get_area(greenery)
            details = osmutils.get_details(territory, tags)
        except:
            greenery_area = 0
        greenery_level = round(greenery_area / territory_area * 100, 1)
        st.write(f"Площа зелених насаджень: {round(greenery_area)} кв. м.   " 
                 f"Рівень озеленення: {greenery_level}%")
        st.session_state.update({"map_obj": map_obj})
    else:
        st.write('Геокодер не може розпізнати введену Вами адресу. '
                 'Перевірте її коректність.')
if (osm := st.session_state.get("map_obj")) is not None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        folium_static(osm)
    try:
        for tag, area in details.items():
            if area:
                st.write(f"{osmutils.get_tagname(tag)}: {area} кв. м.")
    except:
        pass
