import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import Point

def perform_spatial_risk_analysis():
    print("Loading datasets...")
    # 1. Load Data
    conflict_path = 'data.md/mudug_conflict_data_som - Foglio2.csv'
    school_path = 'data.md/mudug-education-facilities.xlsx - School Master List,.csv'
    
    conflict_df = pd.read_csv(conflict_path)
    school_df = pd.read_csv(school_path)

    # 2. Convert to GeoDataFrames
    # Convert conflict WKT to geometry
    conflict_df['geometry'] = conflict_df['geom_wkt'].apply(wkt.loads)
    gdf_conflicts = gpd.GeoDataFrame(conflict_df, geometry='geometry', crs="EPSG:4326")

    # Convert school Lat/Lon to geometry
    school_df = school_df.dropna(subset=['Latitude', 'Longitude'])
    school_df['geometry'] = school_df.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
    gdf_schools = gpd.GeoDataFrame(school_df, geometry='geometry', crs="EPSG:4326")

    # 3. Project to a Metric CRS for accurate buffering (Somalia UTM Zone 38N)
    print("Projecting to UTM Zone 38N for metric distance calculations...")
    gdf_conflicts_metric = gdf_conflicts.to_crs(epsg=32638)
    gdf_schools_metric = gdf_schools.to_crs(epsg=32638)

    # 4. Create 10km Buffer (10,000 meters) around conflict events
    print("Creating 10km buffers around conflict events...")
    gdf_conflicts_metric['buffer_10km'] = gdf_conflicts_metric.geometry.buffer(10000)
    
    # Create a new GeoDataFrame where the geometry is the buffer
    gdf_buffers = gdf_conflicts_metric.set_geometry('buffer_10km')

    # 5. Perform Spatial Join
    # 'inner' join keeps only schools that fall inside a buffer
    print("Performing Spatial Join...")
    schools_at_risk = gpd.sjoin(gdf_schools_metric, gdf_buffers[['id', 'conflict_name', 'year', 'buffer_10km']], 
                                how='inner', predicate='intersects')

    # 6. Save and Summary
    output_cols = ['Name of school / Learning Center', 'District (Select the appropriate District in the dropdown list)', 
                   'conflict_name', 'year', 'id']
    
    # Deduplicate in case a school is in multiple conflict buffers
    schools_at_risk_unique = schools_at_risk.drop_duplicates(subset=['Name of school / Learning Center'])
    
    schools_at_risk_unique.to_csv('geospatial_risk_analysis.csv', index=False)
    
    print("\n--- Spatial Risk Analysis Complete ---")
    print(f"Total schools analyzed: {len(gdf_schools)}")
    print(f"Schools identified within 10km of conflict: {len(schools_at_risk_unique)}")
    print("Results saved to 'geospatial_risk_analysis.csv'")

if __name__ == "__main__":
    perform_spatial_risk_analysis()
