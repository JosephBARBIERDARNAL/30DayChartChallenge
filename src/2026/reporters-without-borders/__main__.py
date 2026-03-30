import geopandas as gpd
import matplotlib.pyplot as plt
import polars as pl
from pypalettes import load_cmap
from pyfonts import load_google_font, set_default_font


EUROPEAN_COUNTRIES = [
    "Albania",
    "Andorra",
    "Armenia",
    "Austria",
    "Azerbaijan",
    "Belarus",
    "Belgium",
    "Bosnia and Herzegovina",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Georgia",
    "Germany",
    "Greece",
    "Hungary",
    "Iceland",
    "Ireland",
    "Italy",
    "Kazakhstan",
    "Kosovo",
    "Latvia",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Moldova",
    "Monaco",
    "Montenegro",
    "Netherlands",
    "North Macedonia",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "Russian Federation",
    "San Marino",
    "Serbia",
    "Slovak Republic",
    "Slovenia",
    "Spain",
    "Sweden",
    "Switzerland",
    "Turkiye",
    "Ukraine",
    "United Kingdom",
    "Vatican City",
]
GEOJSON_COUNTRY_ALIASES = {
    "Bosnia and Herz.": "Bosnia and Herzegovina",
    "Russia": "Russian Federation",
    "Slovakia": "Slovak Republic",
    "Turkey": "Turkiye",
}
target_countries = set(EUROPEAN_COUNTRIES)
gdf = gpd.read_file(
    "https://raw.githubusercontent.com/JosephBARBIERDARNAL/30DayMapChallenge/main/data/countries.geojson"
)
gdf["country"] = gdf["name"].replace(GEOJSON_COUNTRY_ALIASES)

df = (
    pl.read_csv("src/2026/reporters-without-borders/RWB_PFI_SCORE.csv")
    .filter(pl.col("UNIT_MEASURE") == "SCORE")
    .filter(pl.col("UNIT_TYPE") == "NUMBER")
    .filter(pl.col("INDICATOR_LABEL") == "Press Freedom Index Score")
    .filter(pl.col("TIME_PERIOD") == 2025)
    .select("OBS_VALUE", "REF_AREA_LABEL")
    .to_pandas()
)
df["country"] = df["REF_AREA_LABEL"]
df = df[df["country"].isin(target_countries)]
df = gdf[gdf["country"].isin(target_countries)].merge(
    df[["country", "OBS_VALUE"]], on="country", how="left"
)
df_projected = df.to_crs(epsg=3035)
df_projected["centroid"] = df_projected.geometry.centroid
df["centroid"] = df_projected["centroid"].to_crs(df.crs)


adjustments = {
    "France": (10, 3),
    "Italy": (-2.4, 2.5),
    "Finland": (0, -2),
    "Belarus": (0, -0.4),
    "Ireland": (0, -1),
    "Germany": (-0.2, 0),
    "Poland": (0, 0.2),
    "Sweden": (-1.2, -2.8),
    "United Kingdom": (1, -1),
    "Norway": (-4, -5.5),
    "Russian Federation": (-30, -5.5),
}
countries_to_annotate = [
    "France",
    "Poland",
    "Russian Federation",
    "Finland",
    "Spain",
    "Germany",
    "Kazakhstan",
    "Sweden",
    "Ukraine",
    "United Kingdom",
    "Belarus",
    "Turkiye",
]

cmap = load_cmap("Taurus1", cmap_type="continuous", reverse=True)
set_default_font(load_google_font("Arvo"))

fig, ax = plt.subplots(figsize=(10, 7))
fig.set_facecolor("#f8f9fa")
ax.set_facecolor("#f8f9fa")
df.plot(
    ax=ax,
    column="OBS_VALUE",
    cmap=cmap,
    vmin=0,
    vmax=100,
    edgecolor="black",
    linewidth=0.5,
)
ax.set_xlim(-30, 90)
ax.set_ylim(30, 83)
# ax.axis("off")

for country in countries_to_annotate:
    print(country)
    centroid = df.loc[df["country"] == country, "centroid"].values[0]
    x, y = centroid.coords[0]
    try:
        x += adjustments[country][0]
        y += adjustments[country][1]
    except KeyError:
        pass
    value = df.loc[df["country"] == country, "OBS_VALUE"].values[0]
    if country == "United Kingdom":
        country = "UK"
    if value >= 70:
        color = "black"
    else:
        color = "white"
    params = dict(fontsize=7, color=color, ha="center", va="center")
    ax.text(x=x, y=y, s=f"{country.upper()}", **params)  # ty: ignore
    ax.text(x=x, y=y - 1.2, s=f"{value:.1f}", weight="bold", **params)  # ty: ignore

plt.savefig("src/2026/reporters-without-borders/chart.png", dpi=200)
