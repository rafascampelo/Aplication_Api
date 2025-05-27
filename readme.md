INSTRUÇÕES PARA ABRIR O PROJETO ( Windows )

# 1. Vá até a pasta do projeto

cd caminho\da\sua\pasta

# 2. Crie o ambiente virtual

python -m venv venv

# 3. Ative o ambiente

.\venv\Scripts\Activate

# 4. Instale as dependências

pip install -r requirements.txt

# 5. Execute o projeto

python main.py

data_loader.py
Função load_data(file_path: str) -> Union[pd.DataFrame, None]

Lê o arquivo que o usuário manda.

Aceita CSV, JSON e XML (só pelo sufixo do arquivo).

Para CSV, usa pandas.read_csv.

Para JSON, abre o arquivo, carrega com json.load e transforma em DataFrame usando pd.json_normalize.

Para XML, faz o parsing com xml.etree.ElementTree, encontra cada <item>, e monta uma lista de dicionários que vira DataFrame.

Se der erro, printa o erro e devolve None.

Função validate_data(df: pd.DataFrame) -> bool

Checa se o DataFrame tem as colunas mínimas para coordenadas.

Busca colunas que possam ser latitude (lat ou latitude) e longitude (lon, longitude, lng).

Retorna True só se achar as duas. Caso contrário, False.

interface.py
Função process_file(file_info)

Recebe o arquivo enviado pelo usuário (via Gradio).

Usa load_data pra ler esse arquivo.

Gera o mapa com generate_map (do map_generator.py) usando o DataFrame.

Transforma o mapa do Folium em HTML (com generate_html_content) para mostrar na interface.

Se der erro, retorna um HTML com a mensagem do erro.

Função generate_html_content(folium_map)

Salva o mapa do Folium em uma variável na memória (string HTML).

Retorna o HTML pronto pra Gradio mostrar.

Função create_interface()

Cria a interface Gradio (blocos, botão, input de arquivo e um espaço pra mostrar o mapa).

Define o botão que chama process_file e mostra o resultado no componente HTML.

map_generator.py
Função generate_map(data: pd.DataFrame)

Recebe o DataFrame e gera o mapa interativo com Folium.

Normaliza os nomes das colunas (tudo minúsculo).

Tenta achar as colunas de latitude e longitude.

Converte os valores para número, descarta inválidos.

Cria o mapa centralizado na média das coordenadas.

Usa MarkerCluster para agrupar os pontos no mapa.

Adiciona marcadores, e se tiver coluna de nome/nome, coloca popup com nome.

Se algo der errado, gera mapa vazio com mensagem.

Função create_empty_map(message: str)

Gera um mapa vazio centralizado no 0,0, com um marcador vermelho e popup com mensagem de erro.

main.py
Configura variáveis de ambiente para evitar problemas no Windows (tipo diretório temporário e variáveis do PROJ_LIB do Folium).

Importa a interface (create_interface) e lança o app Gradio (launch()).

(não sei o que faltou para funcionar!)
