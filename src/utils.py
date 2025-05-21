# src/utils.py
import json
import xml.etree.ElementTree as ET
import pandas as pd


def carregar_dados(filepath):
    if filepath.endswith('.csv'):
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, encoding='latin1')

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
    df.columns = df.columns.str.lower()

    # Garante que as colunas essenciais estão presentes
    colunas_necessarias = {'latitude', 'longitude', 'nome'}
    if not colunas_necessarias.issubset(df.columns):
        raise ValueError(
            f"O arquivo deve conter as colunas: {colunas_necessarias}")

    return df
