import tkinter as Tk
from tkinter import filedialog, ttk
import pandas as pd
import folium
from folium import IFrame, plugins
import geopandas as gpd
from io import BytesIO
import base64
from PIL import ImageTk, Image
import requests
import webbrowser

frame_table = None  # Variável global inicializada

# Função para abrir o arquivo de dados (CSV, JSON, XML)


def open_file():
    file_path = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[
            ("Arquivos CSV", "*.csv"),
            ("Arquivos JSON", "*.json"),
            ("Arquivos XML", "*.xml")
        ]
    )

    if file_path:
        print(f"Arquivo selecionado: {file_path}")

        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            data = pd.read_json(file_path)
        elif file_path.endswith(".xml"):
            data = pd.read_xml(file_path)

        print(data.head())  # printa os dados no terminal

        display_table(data)
        create_map(data)


def display_table(data):
    # Limpa qualquer coisa antiga
    for widget in frame_table.winfo_children():
        widget.destroy()

    # Cria a tabela
    tree = ttk.Treeview(frame_table, columns=data.columns, show="headings")

    # Configura as colunas
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # Preenche com os dados
    for _, row in data.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill="both")


# Função para criar o mapa com folium

def create_map(data):
    # Garante que tem colunas de latitude e longitude
    if "latitude" not in data.columns or "longitude" not in data.columns:
        print("Dados não contêm colunas 'latitude' e 'longitude'")
        return

    # Centraliza o mapa pela média das coordenadas
    center = [data["latitude"].mean(), data["longitude"].mean()]
    m = folium.Map(location=center, zoom_start=6)

    # Adiciona marcadores
    for _, row in data.iterrows():
        lat = row["latitude"]
        lon = row["longitude"]
        popup = str(row.get("cidade", f"{lat}, {lon}"))
        folium.Marker(location=[lat, lon], popup=popup).add_to(m)

    # Salva o mapa
    map_file = "map.html"
    m.save(map_file)

    # Abre no navegador
    open_map(map_file)

# Função para abrir o mapa no navegador


def open_map(map_file):
    webbrowser.open(map_file)

# Função para criar a interface gráfica com Tkinter


def create_interface():
    global frame_table

    root = tk.Tk()  # Aqui usamos 'root' para a janela principal
    root.title("Análise Geoespacial")
    root.geometry("800x600")  # Define o tamanho da janela

    # Frame para os botões
    frame_buttons = ttk.Frame(root)
    frame_buttons.pack(pady=10)

    # Botão para abrir o arquivo
    open_button = tk.Button(
        frame_buttons, text="Abrir Arquivo", command=open_file)
    open_button.pack()

    # Botão para gerar o mapa
    map_button = tk.Button(
        frame_buttons, text="Gerar Mapa", command=create_map)
    map_button.pack()

    # Frame para a tabela
    frame_table = ttk.Frame(root)  # Usamos ttk.Frame para o frame da tabela
    frame_table.pack(pady=20)

    root.mainloop()  # Mantém a janela aberta


# Chama a função para criar a interface
create_interface()
# Executa a interface gráfica
if __name__ == "__main__":
    create_interface()  # Cria e exibe a interface
