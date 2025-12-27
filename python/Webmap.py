# Webmap.py - Super safe version with debug counts

import folium
import json
import os

os.chdir(r"E:\QGIS Tutorial for Beginners & Intermediates\GIS\Healthcare_Accessibility_Mampong\python_webmap")

# Load files
with open('mampong_boundary.geojson') as f:
    boundary_geo = json.load(f)

with open('communities distance phase1.geojson') as f:
    communities1_geo = json.load(f)

with open('health facilities Centeroids.geojson') as f:
    facilities1_geo = json.load(f)

with open('communities_distance_phase2.geojson') as f:
    communities2_geo = json.load(f)

with open('Complete_Healthcare_Facilities_Phase2.geojson') as f:
    facilities2_geo = json.load(f)

roads_geo = None
if os.path.exists('roads.geojson'):
    with open('roads.geojson') as f:
        roads_geo = json.load(f)

# Center
exterior_coords = boundary_geo['features'][0]['geometry']['coordinates'][0]
center_lon = sum(point[0] for point in exterior_coords) / len(exterior_coords)
center_lat = sum(point[1] for point in exterior_coords) / len(exterior_coords)

m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="OpenStreetMap")

color_map = {'Good Access': 'green', 'Moderate Access': 'yellow', 'Poor Access': 'red'}

# Phase 1
phase1 = folium.FeatureGroup(name="Phase 1: Health Facilities Only (4 Captured)", show=True)
folium.GeoJson(boundary_geo, style_function=lambda x: {'fillOpacity': 0, 'color': 'black', 'weight': 2}).add_to(phase1)
if roads_geo:
    folium.GeoJson(roads_geo, style_function=lambda x: {'color': 'gray', 'weight': 1}).add_to(phase1)

count_fac1 = 0
for feature in facilities1_geo['features']:
    geom = feature['geometry']
    if geom and geom['coordinates'] and len(geom['coordinates']) >= 2:
        coords = geom['coordinates']
        name = feature['properties'].get('name', 'Facility')
        folium.Marker([coords[1], coords[0]], icon=folium.Icon(color='red', icon='plus', prefix='fa'), popup=name).add_to(phase1)
        count_fac1 += 1

count_com1 = 0
for feature in communities1_geo['features']:
    geom = feature['geometry']
    if geom and geom['coordinates'] and len(geom['coordinates']) >= 2:
        coords = geom['coordinates']
        props = feature['properties']
        level = props.get('Acces_lvl1', 'Unknown')
        color = color_map.get(level, 'gray')
        name = props.get('name', 'Community')
        folium.CircleMarker([coords[1], coords[0]], radius=7, color='black', fill_color=color, fill_opacity=0.8, popup=f"{name}<br>{level}").add_to(phase1)
        count_com1 += 1

print(f"Phase 1 added: {count_fac1} facilities, {count_com1} communities")

phase1.add_to(m)

# Phase 2 (same safe logic)
phase2 = folium.FeatureGroup(name="Phase 2: With Private & CHPS Facilities", show=False)
folium.GeoJson(boundary_geo, style_function=lambda x: {'fillOpacity': 0, 'color': 'black', 'weight': 2}).add_to(phase2)
if roads_geo:
    folium.GeoJson(roads_geo, style_function=lambda x: {'color': 'gray', 'weight': 1}).add_to(phase2)

count_fac2 = 0
for feature in facilities2_geo['features']:
    geom = feature['geometry']
    if geom and geom['coordinates'] and len(geom['coordinates']) >= 2:
        coords = geom['coordinates']
        name = feature['properties'].get('name', 'Facility')
        folium.Marker([coords[1], coords[0]], icon=folium.Icon(color='red', icon='plus', prefix='fa'), popup=name).add_to(phase2)
        count_fac2 += 1

count_com2 = 0
for feature in communities2_geo['features']:
    geom = feature['geometry']
    if geom and geom['coordinates'] and len(geom['coordinates']) >= 2:
        coords = geom['coordinates']
        props = feature['properties']
        level = props.get('Acces_lvl2', 'Unknown')
        color = color_map.get(level, 'gray')
        name = props.get('name', 'Community')
        folium.CircleMarker([coords[1], coords[0]], radius=7, color='black', fill_color=color, fill_opacity=0.8, popup=f"{name}<br>{level}").add_to(phase2)
        count_com2 += 1

print(f"Phase 2 added: {count_fac2} facilities, {count_com2} communities")

phase2.add_to(m)

folium.LayerControl().add_to(m)

# Title and author (same as before)
title_html = '''
<h3 align="center" style="font-size:22px; font-weight:bold"><b>Healthcare Accessibility in Mampong Municipality</b></h3>
<h4 align="center" style="font-size:16px">Interactive Comparison: Phase 1 vs Phase 2</h4>
<p align="center">Toggle layers to compare public-only (Phase 1) vs enriched (Phase 2 with private & CHPS)</p>
'''
m.get_root().html.add_child(folium.Element(title_html))

author_html = '''
<div style="position: fixed; bottom: 10px; left: 10px; width: 300px; height: 80px; background-color: white; border:2px solid grey; z-index:9999; font-size:12px; padding: 10px;">
<b>Author:</b> Lawrence Kofi Amoako<br>
<b>Date:</b> December 2025<br>
<b>Data Sources:</b> QuickOSM, GADM
</div>
'''
m.get_root().html.add_child(folium.Element(author_html))

m.save('Interactive_Comparison_Map.html')

print("Interactive map saved! Open Interactive_Comparison_Map.html")