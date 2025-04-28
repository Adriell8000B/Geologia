import folium
import geopandas
import random
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Região de estudo e suas respectivas coordenadas
regiao = {
    "nome": "pernambuco",
    "coordenadas": [-8.301538967444309, -38.151501330306274]
}

# Caminho dos dados
dados = geopandas.read_file("./dados/unidades_solo_pe.geojson")

# Filtra os campos, removendo 'geometry'
campos = [coluna for coluna in dados.columns if coluna != "geometry"]

def gerar_cor_aleatoria():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

cores = {str(idx): gerar_cor_aleatoria() for idx in dados.index}

# Corrige a função de estilo
def estilo(feature):
    indice = str(feature["properties"].get("index"))  # Pega o índice como string
    return {
        "fillColor": cores.get(indice, "#FFFFFF"),  # branco se não encontrar
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7,
    }

dados = dados.reset_index()

# Criando o mapa
mapa = folium.Map(
    location=regiao["coordenadas"],
    zoom_start=7,
    control_scale=True,
    tiles=f"https://tile.jawg.io/jawg-dark/{{z}}/{{x}}/{{y}}.png?access-token={getenv('API_KEY')}",
    attr="&copy; <a href='https://www.jawg.io'>Jawg</a> contributors",
    name="Jawg.Dark",
)

folium.GeoJson(
    dados,
    tooltip=folium.features.GeoJsonTooltip(fields=campos, style="background-color: black; color: white; font-weight: bold; sticky: true; border: none; font-size: 16px;"),
    name="Solos",
    show=True,
    style_function=estilo,
).add_to(mapa)

# Gerando arquivo html para executar no navegador
mapa.save("./html/solos.html")