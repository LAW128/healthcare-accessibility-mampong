# Thematic_Map1.py - Updated Phase 1 map with your requests
# Run in OSGeo4W Shell after cd to python_webmap folder

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import os

os.chdir(r"E:\QGIS Tutorial for Beginners & Intermediates\GIS\Healthcare_Accessibility_Mampong\python_webmap")

# Load Phase 1 layers (adjust filenames if different)
boundary = gpd.read_file('mampong_boundary.geojson')
communities = gpd.read_file('communities distance phase1.geojson')  # Phase 1 communities
facilities = gpd.read_file('health facilities Centeroids.geojson')  # Only 4 captured public facilities
roads = gpd.read_file('roads.geojson') if os.path.exists('roads.geojson') else gpd.GeoDataFrame()

# Reproject
crs = boundary.crs
communities = communities.to_crs(crs)
facilities = facilities.to_crs(crs)
if not roads.empty:
    roads = roads.to_crs(crs)

# Access level field (change if your Phase 1 field is different)
access_field = 'Acces_lvl1'  # Update if needed (e.g., 'access_level')

unique_access = communities[access_field].unique()
print("Phase 1 Detected access levels:", unique_access)

access_colors = {}
for val in unique_access:
    if 'good' in str(val).lower():
        access_colors[val] = 'green'
    elif 'moderate' in str(val).lower():
        access_colors[val] = 'yellow'
    elif 'poor' in str(val).lower():
        access_colors[val] = 'red'
    else:
        access_colors[val] = 'gray'

# Selected communities for labels (same as Phase 2)
selected_names = ['Mampong', 'Daaho', 'Kofiase', 'Anyinasu', 'Asaam', 'Kyeremfaso', 'Ninting', 'Jamasi', 'Agona', 'Banko', 'Nsuta', 'Sekyere Kwamang', 'Abaasua', 'Wiamoase', 'Nyame Bekyere', 'Krobo']
labeled_communities = communities[communities['name'].isin(selected_names)].copy()
labeled_communities['geometry'] = labeled_communities.centroid

# Create figure
fig, ax = plt.subplots(figsize=(12, 12))

# Plot boundary
boundary.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=2)

# Plot roads
if not roads.empty:
    roads.plot(ax=ax, color='gray', linewidth=0.8, alpha=0.7)

# Plot healthcare facilities - larger, thicker red plus (+) for high visibility
facilities.plot(ax=ax, color='red', marker='+', markersize=180, linewidth=4)

# Plot communities by access level
for level in unique_access:
    if level in access_colors:
        subset = communities[communities[access_field] == level]
        if not subset.empty:
            subset.plot(ax=ax, color=access_colors[level], markersize=40, alpha=0.8)

# Labels for selected communities
for _, row in labeled_communities.iterrows():
    ax.annotate(
        row['name'],
        xy=(row.geometry.x, row.geometry.y),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=10,
        fontweight='bold',
        color='black',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=2)
    )

# Updated Title
plt.title('Phase 1 Health Accessibility Mampong (4 Captured Facilities Only)', fontsize=16, pad=30)

# North arrow
ax.annotate('N', xy=(0.95, 0.95), xycoords='axes fraction', fontsize=14, ha='center', va='center')
ax.arrow(0.95, 0.92, 0, 0.03, head_width=0.015, head_length=0.03, fc='black', ec='black', transform=ax.transAxes)

# Scale bar
ax.add_artist(ScaleBar(1, location='lower center', box_alpha=0.8, length_fraction=0.2))

# Legend (same as Phase 2)
legend_elements = [
    Line2D([0], [0], color='gray', lw=1, label='Roads'),
    mpatches.Patch(color='green', label='Good Access'),
    mpatches.Patch(color='yellow', label='Moderate Access'),
    mpatches.Patch(color='red', label='Poor Access'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Communities'),
    Line2D([0], [0], marker='+', color='red', lw=4, markersize=16, label='Healthcare Facilities'),
    mpatches.Patch(facecolor='none', edgecolor='black', label='Mampong Boundary')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, title='Legend', framealpha=0.9)

# Author, date, sources
info_text = "Author: Lawrence Kofi Amoako\nDate: December 2025\nData Sources: QuickOSM, GADM"
ax.text(0.02, 0.02, info_text, transform=ax.transAxes, fontsize=9, va='bottom',
        bbox=dict(facecolor='white', alpha=0.9, edgecolor='black', boxstyle='round,pad=0.5'))

# Updated interpretation note
interpretation = (
    "Phase 1 analysis based on 4 captured facilities only. "
    "Large areas show poor access especially in rural and peri-urban communities, "
    "highlighting significant gaps in coverage."
)
fig.text(0.5, 0.04, interpretation, ha='center', va='center', fontsize=10, wrap=True,
         bbox=dict(facecolor='white', alpha=0.95, edgecolor='gray', boxstyle='round,pad=1'))

# Clean layout
ax.set_axis_off()
plt.tight_layout(rect=[0, 0.07, 1, 0.95])

# Save
plt.savefig('Thematic_Map1.png', dpi=300, bbox_inches='tight')
plt.savefig('Thematic_Map1.pdf', dpi=300, bbox_inches='tight')

print("Phase 1 Thematic Map generated successfully with updates!")