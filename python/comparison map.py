# comparison_map.py - Final fix with correct Phase 1 field name 'access_lvl'
# Run in OSGeo4W Shell after cd to python_webmap folder

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import os

os.chdir(r"E:\QGIS Tutorial for Beginners & Intermediates\GIS\Healthcare_Accessibility_Mampong\python_webmap")

# Load common layers
boundary = gpd.read_file('mampong_boundary.geojson')
roads = gpd.read_file('roads.geojson') if os.path.exists('roads.geojson') else gpd.GeoDataFrame()

# Load Phase 1 layers
communities1 = gpd.read_file('communities distance phase1.geojson')
facilities1 = gpd.read_file('health facilities Centeroids.geojson')

# Load Phase 2 layers
communities2 = gpd.read_file('communities_distance_phase2.geojson')
facilities2 = gpd.read_file('Complete_Healthcare_Facilities_Phase2.geojson')

# Reproject
crs = boundary.crs
for layer in [communities1, facilities1, communities2, facilities2, roads]:
    if not layer.empty:
        layer = layer.to_crs(crs)

# Access level field names - CORRECTED for Phase 1
access_field1 = 'Acces_lvl1'   # Phase 1 field (confirmed by you)
access_field2 = 'Acces_lvl2'   # Phase 2 field

# Standard colors
access_colors = {
    'Good Access': 'green',
    'Moderate Access': 'yellow',
    'Poor Access': 'red'
}

# Selected communities for labels
selected_names = ['Mampong', 'Daaho', 'Kofiase', 'Anyinasu', 'Asaam', 'Kyeremfaso', 'Ninting', 'Jamasi', 'Agona', 'Banko', 'Nsuta', 'Sekyere Kwamang', 'Abaasua', 'Wiamoase', 'Nyame Bekyere', 'Krobo']

# Centroids for labeling
def get_labeled(df):
    labeled = df[df['name'].isin(selected_names)].copy()
    labeled['geometry'] = labeled.centroid
    return labeled

labeled1 = get_labeled(communities1)
labeled2 = get_labeled(communities2)

# Create side-by-side figure
fig = plt.figure(figsize=(20, 10))
gs = fig.add_gridspec(1, 2, wspace=0.1, hspace=0)

# Phase 1 (left) - Access levels now visible
ax1 = fig.add_subplot(gs[0, 0])
boundary.plot(ax=ax1, facecolor='none', edgecolor='black', linewidth=2)
if not roads.empty:
    roads.plot(ax=ax1, color='gray', linewidth=0.8, alpha=0.7)
facilities1.plot(ax=ax1, color='red', marker='+', markersize=140, linewidth=3)
for level, color in access_colors.items():
    subset = communities1[communities1[access_field1] == level]
    if not subset.empty:
        subset.plot(ax=ax1, color=color, markersize=45, alpha=0.9, edgecolor='black', linewidth=0.5)
for _, row in labeled1.iterrows():
    ax1.annotate(row['name'], xy=(row.geometry.x, row.geometry.y), xytext=(5, 5),
                 textcoords="offset points", fontsize=10, fontweight='bold', color='black',
                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=2))
ax1.set_title('Phase 1: \n(4 Captured Facilities)', fontsize=16, fontweight='bold', pad=20)
ax1.set_axis_off()

# Phase 2 (right)
ax2 = fig.add_subplot(gs[0, 1])
boundary.plot(ax=ax2, facecolor='none', edgecolor='black', linewidth=2)
if not roads.empty:
    roads.plot(ax=ax2, color='gray', linewidth=0.8, alpha=0.7)
facilities2.plot(ax=ax2, color='red', marker='+', markersize=140, linewidth=3)
for level, color in access_colors.items():
    subset = communities2[communities2[access_field2] == level]
    if not subset.empty:
        subset.plot(ax=ax2, color=color, markersize=45, alpha=0.9, edgecolor='black', linewidth=0.5)
for _, row in labeled2.iterrows():
    ax2.annotate(row['name'], xy=(row.geometry.x, row.geometry.y), xytext=(5, 5),
                 textcoords="offset points", fontsize=10, fontweight='bold', color='black',
                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=2))
ax2.set_title('Phase 2: With Additional Private & CHPS Facilities', fontsize=16, fontweight='bold', pad=20)
ax2.set_axis_off()

# Main title
fig.suptitle('Healthcare Accessibility in Mampong Municipality: Phase 1 vs Phase 2 Comparison\n'
             '(Phase 1: 4 Captured Facilities)                     (Phase 2: With Additional Private & CHPS Facilities)',
             fontsize=18, fontweight='bold', y=1.02)

# Shared legend
legend_elements = [
    Line2D([0], [0], color='gray', lw=1, label='Roads'),
    mpatches.Patch(color='green', label='Good Access'),
    mpatches.Patch(color='yellow', label='Moderate Access'),
    mpatches.Patch(color='red', label='Poor Access'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Communities'),
    Line2D([0], [0], marker='+', color='red', lw=3, markersize=14, label='Healthcare Facilities'),
    mpatches.Patch(facecolor='none', edgecolor='black', label='Mampong Boundary')
]
fig.legend(handles=legend_elements, loc='lower center', ncol=7, fontsize=11, frameon=True, fancybox=True, shadow=True, bbox_to_anchor=(0.5, 0.02))

# Author, date, sources
info_text = "Author: Lawrence Kofi Amoako | Date: December 2025 | Data Sources: QuickOSM, GADM"
fig.text(0.01, 0.01, info_text, fontsize=10, ha='left', va='bottom',
         bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))

# Caption
caption_left = "Left: Phase 1 shows widespread poor access with only 4 captured facilities."
caption_right = "Right: Phase 2 includes additional private clinics and CHPS compounds, resulting in modest improvements. However, rural and peri-urban towns/communities still face significant accessibility challenges."
caption = caption_left + " " + caption_right
fig.text(0.5, 0.08, caption, ha='center', va='center', fontsize=11, wrap=True,
         bbox=dict(facecolor='white', alpha=0.95, edgecolor='gray', boxstyle='round,pad=1'))

# Layout
plt.tight_layout(rect=[0, 0.12, 1, 0.95])

# Save
plt.savefig('Comparison_Map.png', dpi=300, bbox_inches='tight')
plt.savefig('Comparison_Map.pdf', dpi=300, bbox_inches='tight')

print("Final comparison map generated — Phase 1 access levels now fully visible!")