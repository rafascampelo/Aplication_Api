
from src.viz import criar_mapa
from src.utils import carregar_dados
import tempfile
import gradio as gr


def gerar_html_mapa(arquivo):
    try:
        df = carregar_dados(arquivo.name)
        mapa = criar_mapa(df)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            mapa.save(tmp.name)
            tmp.seek(0)
            return tmp.read().decode("utf-8")
    except Exception as e:
        return f"<p style='color:red;'>Erro: {str(e)}</p>"


def inicializar_interface():
    demo = gr.Interface(
        fn=gerar_html_mapa,
        inputs=gr.File(label="Envie um arquivo CSV, JSON ou XML"),
        outputs=gr.HTML(label="Mapa gerado")
    )
    demo.launch()
