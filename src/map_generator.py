import folium
from folium.plugins import MarkerCluster
import pandas as pd

def generate_map(data: pd.DataFrame):
    print("Colunas:", data.columns)
    print("Primeiras linhas:", data.head())
    """Gera mapa Folium a partir dos dados"""
    if data is None or data.empty:
        return create_empty_map("Dados inválidos ou vazios")
    
    # Normaliza nomes de colunas
    data.columns = data.columns.str.lower()
    
    # Tenta encontrar colunas de coordenadas
    lat_col = next((col for col in data.columns if 'lat' in col), None)
    lon_col = next((col for col in data.columns if 'lon' in col or 'lng' in col), None)
    
    if not lat_col or not lon_col:
        return create_empty_map("Colunas de coordenadas não encontradas")
    
    try:
        # Converte para numérico e remove inválidos
        data[lat_col] = pd.to_numeric(data[lat_col], errors='coerce')
        data[lon_col] = pd.to_numeric(data[lon_col], errors='coerce')
        data = data.dropna(subset=[lat_col, lon_col])
        
        if data.empty:
            return create_empty_map("Nenhuma coordenada válida encontrada")
        
        # Cria o mapa
        avg_lat = data[lat_col].mean()
        avg_lon = data[lon_col].mean()
        
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)
        marker_cluster = MarkerCluster().add_to(m)
        
        # Adiciona marcadores
        name_col = next((col for col in data.columns if 'name' in col or 'nome' in col), None)
        
        for _, row in data.iterrows():
            popup = str(row[name_col]) if name_col else "Localização"
            folium.Marker(
                [row[lat_col], row[lon_col]],
                popup=popup,
                icon=folium.Icon(color='blue')
            ).add_to(marker_cluster)
            
        return m
    
    except Exception as e:
        return create_empty_map(f"Erro ao gerar mapa: {str(e)}")

def create_empty_map(message: str):
    """Cria mapa vazio com mensagem de erro"""
    m = folium.Map(location=[0, 0], zoom_start=2)
    folium.Marker(
        [0, 0],
        popup=message,
        icon=folium.Icon(color='red', icon='warning-sign')
    ).add_to(m)
    return m