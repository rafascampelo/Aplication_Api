import pandas as pd
import json
import xml.etree.ElementTree as ET
from typing import Union

def load_data(file_path: str) -> Union[pd.DataFrame, None]:
    """Carrega dados de arquivos CSV, JSON ou XML"""
    if not file_path:
        return None
    
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return pd.json_normalize(data)
        elif file_path.endswith('.xml'):
            tree = ET.parse(file_path)
            root = tree.getroot()
            data = []
            for item in root.findall('item'):
                data.append({elem.tag: elem.text for elem in item})
            return pd.DataFrame(data)
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

def validate_data(df: pd.DataFrame) -> bool:
    """Verifica se o DataFrame contém colunas necessárias"""
    if df is None:
        return False
    
    # Verifica colunas de coordenadas com nomes variantes
    has_lat = any(col.lower() in ['lat', 'latitude'] for col in df.columns)
    has_lon = any(col.lower() in ['lon', 'longitude', 'lng'] for col in df.columns)
    
    return has_lat and has_lon