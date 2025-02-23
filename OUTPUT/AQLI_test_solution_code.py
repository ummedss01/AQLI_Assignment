import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable



###import csv
test=pd.read_csv('gadm2_aqli_1998_2021.csv')
 ###check columns 
test.columns

###question 1.1 How many GADM2 regions are present in India?
ind_gadm2=test[test.iso_alpha3 == 'IND']
ind_gadm2.columns
ind_gadm_q1=ind_gadm2[['iso_alpha3', 'country', 'name_1', 'name_2']]
# Get unique regions from 'name_1' and 'name_2'
unique_name_1 = ind_gadm_q1["name_1"].unique()
unique_name_2 = ind_gadm_q1["name_2"].unique()
# Count the number of unique regions
num_regions_name_1 = len(unique_name_1)
num_regions_name_2 = len(unique_name_2)





#####1.2 Calculate population weighted pollution average of all years at country (GADM0) level
Pop_weig_pm=test[['iso_alpha3', 'country', 'name_1', 'name_2','pm1998', 'pm1999',
                  'pm2000', 'pm2001', 'pm2002', 'pm2003', 'pm2004', 'pm2005', 'pm2006',
                  'pm2007', 'pm2008', 'pm2009', 'pm2010', 'pm2011', 'pm2012', 'pm2013',
                  'pm2014', 'pm2015', 'pm2016', 'pm2017', 'pm2018', 'pm2019', 'pm2020',
                  'pm2021']]
# List all PM columns
pm_columns = [col for col in Pop_weig_pm.columns if col.startswith("pm")]
# Calculate row-wise average of PM columns and add as a new column
Pop_weig_pm["ALL_Year_Pop_Weig_PM"] = Pop_weig_pm[pm_columns].mean(axis=1, skipna=True)
# Group by country to get the average at the country level
Pop_weig_country = Pop_weig_pm.groupby([ "country"])["ALL_Year_Pop_Weig_PM"].mean().reset_index()
##### Save the country level file as a CSV.
Pop_weig_country.to_csv('Pop_weig_avg_Poll_country.csv')




#####What are the 10 most polluted countries in 2021?
Most_poll_count_21=Pop_weig_pm[['country','pm2021']]
# Group by country and calculate the mean pm2021 value
Most_poll_count_21 = Pop_weig_pm.groupby("country")["pm2021"].mean().reset_index()
# Sort in descending order and select the top 10
Most_poll_count_21 = Most_poll_count_21.sort_values(by="pm2021", ascending=False).head(10)
####save as csv
Most_poll_count_21.to_csv('most_10_polluted_country_21.csv')



####1.3 What was the most polluted GADM2 region in the world in 1998, 2005 and 2021?
top_1998 = Pop_weig_pm[['country', 'name_1','name_2', 'pm1998']].sort_values(by="pm1998", ascending=False).head(1)
print(top_1998)
top_2005 = Pop_weig_pm[['country', 'name_1','name_2', 'pm2005']].sort_values(by="pm2005", ascending=False).head(1)
print(top_2005)
top_2021 = Pop_weig_pm[['country', 'name_1','name_2', 'pm2021']].sort_values(by="pm2021", ascending=False).head(1)
print(top_2021)
# Combine the data into one table
combined_all = pd.concat([top_1998, top_2005, top_2021], ignore_index=True)
   ###save as csv
combined_all.to_csv('top_GADM2_region.csv')




#######Plot a population weighted pollution average trendline plot for Uttar Pradesh from 1998 to 2021. Save this plot as a high quality PNG file.
UP = Pop_weig_pm.drop(columns=['iso_alpha3', 'country', 'name_2'])
UP_annual_tend = UP[UP['name_1'] == 'Uttar Pradesh'].groupby('name_1').mean()



plt.figure(figsize=(10, 6))
sns.regplot(x=years, y=pm_values, scatter=True, order=2, ci=None, 
            line_kws={"color": "red"}, 
            scatter_kws={"color": "blue", "s": 50})  
# Customize the plot
plt.xlabel("Year", fontsize=12, fontweight='bold', color="purple")  
plt.ylabel("Population-Weighted PM$_{2.5}$ (µg m$^{-3}$)", fontsize=14, fontweight='bold', color="purple")  
plt.title("PM$_{2.5}$ Trend in Uttar Pradesh (1998-2021)", fontsize=16, fontweight='bold', color="olive") 
# Make axis text (tick labels) bold and black
plt.xticks(fontsize=12, fontweight='bold', color="green", rotation=45)
plt.yticks(fontsize=12, fontweight='bold', color="green")
# Add a grid lines
plt.grid(True, linestyle='--', alpha=0.6)
# Save 
plt.savefig("UP_PM25_Trend.png", dpi=300, bbox_inches="tight")
# Show the plot
plt.show()




                 #####Q 2 ###0.098
####2.1 Plot a bar graph for the life years lost relative to the WHO guideline in the 10 most polluted countries 
#in the world and also plot them on a global country level map. For the map, the 10 most polluted country boundaries
# should be filled in with “dark red” and the rest of the map should be grayed out.
# Save both the bar graph and the map as high quality PNG files.
###I am ploting for most recent year 2021 becase not meantioned in question 
top_YLL_ctry_WHO=test[['country','pm2021','llpp_who_2021']].groupby('country').mean()
top_YLL_ctry_WHO_10=top_YLL_ctry_WHO.sort_values(by="pm2021", ascending=False).head(10).reset_index()



# Replace specific country names for better ploting 
top_YLL_ctry_WHO_10["country"] = top_YLL_ctry_WHO_10["country"].replace({
    "Democratic Republic of the Congo": "DRC",
    "Republic of the Congo": "RC"
})
# Sort countries by pm2021 for better color scaling
top_YLL_ctry_WHO_10 = top_YLL_ctry_WHO_10.sort_values(by="pm2021", ascending=False)
# Create a color gradient from dark to light red (reverse order for correct mapping)
colors = sns.color_palette("Reds", len(top_YLL_ctry_WHO_10))[::-1] 

# Create the bar plot
plt.figure(figsize=(8, 6))
bars = plt.bar(top_YLL_ctry_WHO_10["country"], top_YLL_ctry_WHO_10["llpp_who_2021"], 
               color=colors, edgecolor="black")
#plt.xlabel("Country", fontsize=12, fontweight='bold', color="purple")  
plt.ylabel("Life Years Lost (LYL) due to PM$_{2.5}$ exposure in 2021", fontsize=11, fontweight='bold', color="blue") 
plt.title("LYL in World Top 10 Polluted Countries relative to the WHO guideline ", fontsize=14, fontweight='bold', color="teal")  
# Rotate x-axis labels for better readability
plt.xticks(rotation=90, fontsize=12, fontweight='bold', color="purple")  
plt.yticks(fontsize=14, fontweight='bold', color="black")  
# Add grid lines
plt.grid(axis="y", linestyle="--", alpha=0.6)
# Show the plot
plt.tight_layout()
# Save 
plt.savefig("top_LYL_countries_2021.png", dpi=300, bbox_inches="tight")
plt.show()







      ####2.1 part 2
###top 10 polluted country in 2021
top_YLL_ctry_WHO_10=top_YLL_ctry_WHO.sort_values(by="pm2021", ascending=False).head(10).reset_index()
top_YLL_ctry_WHO_10=top_YLL_ctry_WHO_10[['country', 'pm2021']]

####ploting 
###import shapefile
world=gpd.read_file('aqli_gadm2_final_june302023.shp')
world.columns
# # Rename to match top_YLL_ctry_WHO_10
world['country']=world['name0']
 #####selected required columns
world_ctry=world[['country', 'geometry']]
# Merge polygons at the country level (dissolve by 'country')
world_merged = world_ctry.dissolve(by="country")
world_merged=world_merged.reset_index()
# Merge the world dataset with pollution data to identify the top 10 polluted countries
world_merged["highlight"] = world_merged["country"].isin(top_YLL_ctry_WHO_10["country"])

              ####updated Indian boundary in global shapefile 
###import India shapefile 
ind=gpd.read_file('India_Boundary.shp')
###check CRS in shapefile ..is it in EPSG:4326
ind.crs
# Ensure both shapefiles have the same CRS
ind = ind.to_crs(world_merged.crs)
# Update India's geometry in world_merged
world_merged.at[world_merged[world_merged["country"] == "India"].index[0], "geometry"] = ind.geometry.iloc[0]



# Sort countries by PM2.5 concentration (pm2021) in descending order
top_YLL_ctry_WHO_10 = top_YLL_ctry_WHO_10.sort_values(by="pm2021", ascending=False)

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))
# Plot the world map with gray color for all countries
world_merged.plot(ax=ax, color="lightgray", edgecolor="black", linewidth=0.5)
# Highlight the top 10 polluted countries in dark red
highlighted_countries = world_merged[world_merged["country"].isin(top_YLL_ctry_WHO_10["country"])]
highlighted_countries.plot(ax=ax, color="darkred", edgecolor="black", linewidth=0.8)

# Add serial numbers (1-10) at the center of each highlighted country
for idx, row in highlighted_countries.iterrows():
    country_rank = top_YLL_ctry_WHO_10[top_YLL_ctry_WHO_10["country"] == row["country"]].index[0] + 1  
    centroid = row["geometry"].centroid  # Get country centroid
    ax.text(centroid.x, centroid.y, str(country_rank), ha="center", fontsize=8, color="blue", fontweight="bold")
# Create custom legend text with country names and ranks
legend_labels = [f"{i+1}. {top_YLL_ctry_WHO_10.iloc[i]['country']}" for i in range(len(top_YLL_ctry_WHO_10))]
# Position the legend at the bottom-right within the map
legend_x, legend_y =  -0.01, 0.5  # Adjust position within the map
# Add legend title (No rectangle box)
ax.text(legend_x, legend_y + 0.1, "Top Polluted Countries", transform=ax.transAxes, 
        fontsize=12, fontweight="bold", color="olive") 
# Add legend text (Country names)
for i, text in enumerate(legend_labels):
    ax.text(legend_x, legend_y - (i * 0.05), text, transform=ax.transAxes, fontsize=10, fontweight="bold", color="blue")

# Remove axis borders and ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)
# Add title
plt.title("Top 10 Most Polluted Countries in World (2021)", fontsize=14, fontweight='bold', color="red")
# Save 
plt.savefig("top_polluted_countries_2021.png", dpi=300, bbox_inches="tight")
# Show the plot
plt.show()









             #####2.2 section 

###### Esteren vs western europ 
###import Western and ESTERN Europ countries as per Assembly of States Parties to the Rome Statute/international criminal court
# https://asp.icc-cpi.int/states-parties/western-european-and-other-states 
europ=pd.read_excel('EUROP_COUNTRY.xlsx')

   ###extract europian region from world map based on eurp countries name  
###import shapefile
world=gpd.read_file('aqli_gadm2_final_june302023.shp')
world.columns
# Merge `world` and `europ` on the 'country' column (ensuring matching names)
EST_WST_EU= world.merge(europ, left_on="name0", right_on="Country Name", how="inner")
   ###selected required columns
EST_WST_EURO_contry=EST_WST_EU[['country', 'name1', 'name2', 'Europe Part', 'geometry']]
###for 2021 life expectency data
EWE=test[['iso_alpha3', 'country','name_1', 'name_2','pm2021', 'llpp_who_2021']] 
####merge with europian countries file 
EUP_EW_country=EWE.merge(europ, left_on='country', right_on='Country Name', how='inner')
####selected data for descriptive analysis
EUP_LEG=EUP_EW_country[['country','name_1', 'name_2','pm2021', 'llpp_who_2021','Europe Part']]

#####merge with shapefile 
EST_WST_EURO_contry.columns
EUP_LEG.columns
###rename columns for merge 
EST_WST_EURO_contry = EST_WST_EURO_contry.rename(columns={'name2': 'name_2'})
EST_WST_EURO_contry = EST_WST_EURO_contry.rename(columns={'name1': 'name_1'})
####merge the both file 
EUP_LEG_pm = EUP_LEG.merge(EST_WST_EURO_contry, on=['country', 'name_1','name_2'], how='inner')
####rename Europe part
EUP_LEG_pm=EUP_LEG_pm.rename(columns={'Europe Part_x': 'EURO_part'})
EUP_LEG_pm=EUP_LEG_pm.drop(columns='Europe Part_y')
####select desired columns
EUP_LEG_pm.columns



####country level bourndary 
world_merged=gpd.read_file('Ind_updated_world.shp')
EU_map=world_merged[['country', 'geometry']]
 ####select country for europian region
EU_map1=EU_map.merge(europ, left_on='country', right_on='Country Name', how='inner')
###Estern and western europ 
EWEshp=EUP_LEG_pm[['EURO_part','geometry']]
# Merge polygons at the country level (dissolve by 'country')
EWEshp_2 = EWEshp.dissolve(by="EURO_part")
EWEshp_2=EWEshp_2.reset_index()

   #EWEshp_2.plot()
acount_pm_le=EUP_LEG_pm[['pm2021', 'llpp_who_2021', 'EURO_part']]
   ####mean PM2.5 and year of life loss 
acount_pm_le_1=acount_pm_le.groupby('EURO_part').mean().reset_index()

# Ensure data is a GeoDataFrame
if not isinstance(EUP_LEG_pm, gpd.GeoDataFrame):
    EUP_LEG_pm = gpd.GeoDataFrame(EUP_LEG_pm, geometry="geometry")
# Define bin edges for color mapping
bins = [0, 0.1, 0.5, 1, 2, 3]
# Create a colormap from floralwhite to darkorange
cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", ["floralwhite", "darkorange"])
norm = mcolors.BoundaryNorm(bins, cmap.N)


# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))
# Plot the life expectancy regions with color
EUP_LEG_pm.plot(
    column="llpp_who_2021",
    cmap=cmap,
    linewidth=0.3,
    edgecolor="none",
    alpha=0.8,
    legend=False,
    ax=ax
)
# Plot country boundaries from EU_map1 (Black edges with alpha)
EU_map1.plot(ax=ax, color="none", edgecolor="black", linewidth=0.2, alpha=0.4)
# Plot Eastern boundary (Purple)
EWEshp_2[EWEshp_2['EURO_part'] == 'Eastern'].plot(ax=ax, color="none", edgecolor="purple", linewidth=0.6, alpha=0.5)
# Create a colorbar inside the map (horizontally aligned at the bottom)
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, ticks=bins, orientation="horizontal", shrink=0.6, pad=0.02)
cbar.set_label("Potential Gain in Life Expectancy (In Years)", fontsize=10, fontweight="bold",)
# Adjust legend position (x, y, width, height)
cbar.ax.set_position([0.2, 0.32, 0.6, 0.02])  

# Define Text for Western & Eastern Europe (Two-Row Format)
western_text = "Western Europe:7.5 µg m$^{-3}$,\n2.7 months potential gain"
eastern_text = "Eastern Europe:14.6 µg m$^{-3}$,\n9.4 months potential gain"
# Display text on the left side (Above Left Bottom)
ax.text(0.02, 0.42, western_text, fontsize=8, fontweight="bold", color="black", transform=ax.transAxes, ha="left")
# Display text on the right side (Below Top Right)
ax.text(0.99, 0.55, eastern_text, fontsize=8, fontweight="bold", color="purple", transform=ax.transAxes, ha="right")

# Map title and layout
ax.set_title("", fontsize=14)
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)
# Save as high-quality PDF
plt.savefig("EST_WST_EUROP_map.pdf", 
            dpi=600, format="pdf", bbox_inches="tight")

# Show the plot
plt.show()





                  ####2.3 global pollution map
####global shapefile for district level
GADM_shp=world
GADM_shp=GADM_shp[['name0','country', 'name1', 'name2', 'geometry',]]
####global air pollution data at district level 
world21ap=test[['country', 'name_1', 'name_2','pm2021']]
####rename columns in shapefile to mrege air pollution and shapfile 
GADM_shp=GADM_shp.rename(columns={'name1': 'name_1'})
GADM_shp=GADM_shp.rename(columns={'name2': 'name_2'})
###merge both dataset
world_pm = GADM_shp.merge(world21ap, on=['country', 'name_1','name_2'], how='inner')
####country level shapefile 
world_merged=gpd.read_file('Ind_updated_world.shp')
EU_map=world_merged[['country', 'geometry']]



       ###map ploting
if not isinstance(world_pm, gpd.GeoDataFrame):
    world_pm = gpd.GeoDataFrame(world_pm, geometry="geometry")

# Define bin edges for PM2.5 concentration # Last bin for values >70
bins = [0, 5, 10, 20, 30, 40, 50, 60, 70, 500]  
 # Use a blue gradient colormap
cmap = plt.get_cmap("PuBu") 
# Normalize the color scale based on bins
## Ensures highest values (>70) are properly colored
norm = mcolors.BoundaryNorm(bins, cmap.N, extend="max")  

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))
# Plot world map colored by PM2.5 levels
world_pm.plot(
    column="pm2021",
    cmap=cmap,
    norm=norm,
    linewidth=0.3,
    edgecolor="none",  
    alpha=0.8,
    legend=False,
    ax=ax
)
# Plot country boundaries from EU_map1 (Black edges with transparency)
EU_map.plot(ax=ax, color="none", edgecolor="black", linewidth=0.2, alpha=0.4)
# Create a colorbar with defined bins
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, ticks=bins[:-1], orientation="horizontal", shrink=0.6, pad=0.02)  
# Update tick labels (must match `bins[:-1]`)   # Use a blue gradient colormap
cbar.ax.set_xticklabels(["0", "5", "10", "20", "30", "40", "50", "60", ">70"])  
# Set legend title
cbar.set_label("PM$_{2.5}$ (µg m$^{-3}$)", fontsize=12, fontweight="bold")
# Map title and layout
ax.set_title("The global pollution map (2021)", fontsize=14, fontweight="bold")
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)
# Save as high-quality SVG
plt.savefig("global_pm2021_map.svg", dpi=320, format="svg")
# Show the plot
plt.show()
