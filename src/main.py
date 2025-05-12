import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import geopandas as gpd
import folium
import webbrowser
import sys


class GeoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Geoespacial v2.0")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Configuração da interface
        self.setup_ui()
        self.data = None

    def setup_ui(self):
        """Configura os elementos da interface"""
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Button(
            self.frame,
            text="Carregar Arquivo",
            command=self.safe_open_file,  # Método modificado
            width=25,
            height=2
        ).pack(pady=10)

        self.map_btn = tk.Button(
            self.frame,
            text="Gerar Mapa",
            command=self.create_map,
            width=25,
            height=2,
            state=tk.DISABLED
        )
        self.map_btn.pack(pady=10)

        self.status = tk.Label(
            self.frame, text="Pronto para carregar arquivo", fg="gray")
        self.status.pack(pady=10)

    def safe_open_file(self):
        """Método seguro para abrir arquivos"""
        try:
            # Cria uma janela Tkinter temporária
            temp_root = tk.Tk()
            temp_root.withdraw()  # Esconde a janela
            # Garante que ficará visível
            temp_root.attributes('-topmost', True)

            file_path = filedialog.askopenfilename(
                parent=temp_root,
                title="Selecione um arquivo",
                filetypes=[
                    ("CSV", "*.csv"),
                    ("JSON", "*.json;*.geojson"),
                    ("XML", "*.xml")
                ]
            )
            temp_root.destroy()  # Fecha a janela temporária

            if file_path:
                self.process_file(file_path)

        except Exception as e:
            messagebox.showerror(
                "Erro Fatal", f"O programa encontrou um erro:\n{str(e)}")
            self.on_close()

    def process_file(self, file_path):
        """Processa o arquivo selecionado"""
        try:
            if file_path.endswith(".csv"):
                self.data = pd.read_csv(file_path)
                # Converte para GeoDataFrame se tiver coordenadas
                if all(col in self.data.columns for col in ["latitude", "longitude"]):
                    self.data = gpd.GeoDataFrame(
                        self.data,
                        geometry=gpd.points_from_xy(
                            self.data.longitude, self.data.latitude)
                    )

            elif file_path.endswith((".json", ".geojson")):
                self.data = gpd.read_file(file_path)

            elif file_path.endswith(".xml"):
                self.data = pd.read_xml(file_path)

            self.map_btn.config(state=tk.NORMAL)
            self.status.config(
                text=f"Arquivo carregado: {file_path.split('/')[-1]}", fg="green")

        except Exception as e:
            messagebox.showerror(
                "Erro", f"Falha ao processar arquivo:\n{str(e)}")

    def create_map(self):
        """Gera o mapa com Folium"""
        if self.data is None:
            messagebox.showwarning("Aviso", "Nenhum dado carregado!")
            return

        try:
            # Determina o centro do mapa
            if isinstance(self.data, gpd.GeoDataFrame):
                centroid = self.data.geometry.centroid
                center = [centroid.y.mean(), centroid.x.mean()]
            else:
                center = [self.data["latitude"].mean(
                ), self.data["longitude"].mean()]

            # Cria o mapa
            m = folium.Map(location=center, zoom_start=6)

            # Adiciona marcadores
            if isinstance(self.data, gpd.GeoDataFrame):
                for idx, row in self.data.iterrows():
                    if row.geometry.geom_type == "Point":
                        folium.Marker(
                            [row.geometry.y, row.geometry.x],
                            popup=f"ID: {idx}"
                        ).add_to(m)
            else:
                for idx, row in self.data.iterrows():
                    folium.Marker(
                        [row["latitude"], row["longitude"]],
                        popup=f"ID: {idx}"
                    ).add_to(m)

            # Salva e abre o mapa
            map_path = "mapa.html"
            m.save(map_path)
            webbrowser.open(map_path)

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar mapa:\n{str(e)}")

    def on_close(self):
        """Método para encerrar o programa corretamente"""
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    app = GeoApp(root)

    # Configuração adicional para Windows
    if sys.platform == "win32":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)

    root.mainloop()
