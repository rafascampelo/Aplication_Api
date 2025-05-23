from src.interface import create_interface
import os
import tempfile

# Configurações para resolver problemas do Windows
os.environ['TEMP'] = tempfile.mkdtemp()  # Cria um diretório temporário exclusivo
os.environ['PROJ_LIB'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proj_data')
if __name__ == "__main__":
    interface = create_interface()
    interface.launch()