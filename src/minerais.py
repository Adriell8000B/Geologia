from dotenv import load_dotenv
from os import getenv
import geopandas
import folium
import pandas

load_dotenv()

dados = geopandas.read_file("./dados/minerais_industriais.geojson")
campos = [coluna for coluna in dados.columns if coluna != "geometry"]

regiao = {
	"nome": "pernambuco",
	"coordenadas": [-8.301538967444309, -38.151501330306274],
}

mapa = folium.Map(
	location=regiao["coordenadas"],
	zoom_start=8,
	control_scale=True,
	tiles=f"https://tile.jawg.io/jawg-dark/{{z}}/{{x}}/{{y}}.png?access-token={getenv('API_KEY')}",
	attr="&copy; <a href='https://www.jawg.io'>Jawg</a> contributors",
	name="Jawg.Dark",
)

features_com_tooltip = []

for index, row in dados.iterrows():
	properties = {}
	tooltip_content = "<div style='background-color: transparent; color: white; font-weight: bold; padding: 5px; border-radius: 3px;'>"
	has_data = False
	for col in campos:
		value = row[col]
		if pandas.notna(value) and value != "":
			properties[col] = value
			tooltip_content += f"<p style='margin: 2px;'>{col}: {value}</p>"
			has_data = True
		properties[''] = tooltip_content + "</div>" if has_data else ""
	feature = {
		"type": "Feature",
		"geometry": {
			"type": "Point",
			"coordinates": [row["LONGITUDE"], row["LATITUDE"]],
		},
		"properties": properties,
	}
	features_com_tooltip.append(feature)

geojson_data_com_tooltip = {
	"type": "FeatureCollection",
	"features": features_com_tooltip,
}

folium.GeoJson(
	geojson_data_com_tooltip,
	tooltip=folium.GeoJsonTooltip(fields=[''], localize=False, sticky=True, permanent=False, style="background: black;font-size: 16px;"),
	name="Minerais Industriais",
	marker=folium.CircleMarker(
		radius=20,
		color="white",
		stroke=True,
		weight=0.8,
		fill=True,
		fill_opacity=0.2,
		opacity=1,
	),
).add_to(mapa)

mapa.save("./html/minerais.html")
