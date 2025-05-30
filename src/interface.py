import gradio as gr
import folium
from io import StringIO
import tempfile
import os
import uuid
from src.map_generator import generate_map
from src.data_loader import load_data

def process_file(file):
    if not file:
        return "<div style='color:red;padding:20px'>Nenhum arquivo enviado</div>"

    try:
        file_path = file.name if hasattr(file, 'name') else file
        print("Arquivo recebido:", file_path)

        df = load_data(file_path)
        print("Preview dos dados:", df.head())

        m = generate_map(df)
        html_content = generate_html_content(m)

        return html_content

    except Exception as e:
        return f"<div style='color:red;padding:20px'>ERRO: {str(e)}</div>"

def generate_html_content(folium_map):
    """Gera conteúdo HTML sem usar arquivos temporários físicos"""
    # Cria um arquivo em memória
    with StringIO() as buffer:
        folium_map.save(buffer, close_file=False)
        html_content = buffer.getvalue()
    
    return html_content

def create_interface():
    with gr.Blocks(title="Visualizador de Mapas") as demo:
        gr.Markdown("# 🗺️ Visualizador de Dados Geoespaciais")
        
        with gr.Row():
            file_input = gr.File(
                label="Selecione seu arquivo (CSV, JSON ou XML)",
                file_types=[".csv", ".json", ".xml"],
                type="filepath"
            )
            
            btn = gr.Button("Gerar Mapa", variant="primary")
        
        html_output = gr.HTML(label="Mapa Gerado")
        
        btn.click(
            fn=process_file,
            inputs=file_input,
            outputs=html_output
        )
    
    return demo
