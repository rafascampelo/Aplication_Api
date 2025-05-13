# src/utils.py

import pandas as pd
import json
import xml.etree.ElementTree as ET


def carregar_dados(filepath):
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)

    elif filepath.endswith('.json'):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            df = pd.json_normalize(data)

    elif filepath.endswith('.xml'):
        tree = ET.parse(filepath)
        root = tree.getroot()

        dados = []
        for item in root:
            registro = {}
            for elem in item:
                registro[elem.tag] = elem.text
            dados.append(registro)

        df = pd.DataFrame(dados)

    else:
        raise ValueError(
            'Formato de arquivo não suportado. Use CSV, JSON ou XML.')

    return df
