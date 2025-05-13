import gradio as gr
from src.viz import criar_mapa
from src.utils import carregar_dados


def gerar_html_mapa():
    mapa = criar_mapa()  # assume que retorna um folium.Map
    mapa.save("mapa.html")
    with open("mapa.html", "r", encoding="utf-8") as f:
        return f.read()


def inicializar_interface():
    demo = gr.Interface(
        fn=gerar_html_mapa,
        inputs=[],
        outputs=gr.HTML()
    )
    demo.launch()
