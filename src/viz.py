# src/viz.py

import folium


def criar_mapa(df):
    # Aqui vamos usar um exemplo básico de latitude e longitude
    # Então, os dados devem ter essas colunas: 'latitude' e 'longitude'
    mapa = folium.Map(
        location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=10)

    for _, row in df.iterrows():
        folium.Marker([row['latitude'], row['longitude']],
                      popup=row['nome']).add_to(mapa)

    return mapa
