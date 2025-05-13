INSTRUÇÕES PARA ABRIR O PROJETO ( Windows )

para abrir o ambiente virtual:
cria ambiente : python -m venv venv
abri o ambiente : .\venv\Scripts\Activate

para instalar as dependências, coloque no bash:
pip install -r requirements.txt

Lógica da Construção do Projeto
Agora vou explicar o raciocínio por trás de cada parte do projeto para que você entenda como cada arquivo se encaixa na estrutura:

1. Função de Leitura e Tratamento dos Dados (utils.py)
   O arquivo utils.py é responsável por ler e tratar os dados de arquivos CSV, JSON e XML. Cada tipo de arquivo tem uma função própria, que usa a biblioteca correta para ler os dados e retorná-los em um formato de lista de dicionários.

CSV: Usamos a biblioteca csv para ler os dados e armazená-los em um formato adequado.

JSON: Utilizamos json para carregar o arquivo e transformá-lo em uma lista de dicionários.

XML: Usamos a biblioteca xml.etree.ElementTree para fazer o parsing do XML e retornar os dados como uma lista de dicionários.

Essas funções estão separadas em blocos, para que quando você quiser adicionar mais tipos de arquivos no futuro, só precise seguir o mesmo padrão.

2. Funções de Visualização (viz.py)
   Aqui é onde acontece a criação e exibição do mapa. Usamos a biblioteca Plotly para a visualização dos dados geoespaciais:

A função exibir_mapa recebe os dados de latitude e longitude e os plota no mapa.

O mapa interativo é gerado com a função go.Scattergeo do Plotly. Usamos esse gráfico para exibir os pontos de localização e personalizar a visualização.

Essas funções são responsáveis por transformar os dados geoespaciais em uma visualização interativa.

3. Interface Gradio (interface.py)
   A interface de usuário foi criada com Gradio. A interface tem:

Entrada de Arquivo: O usuário pode selecionar o tipo de arquivo (CSV, JSON ou XML) e enviar o arquivo para o sistema.

Botão de Visualização: Quando o arquivo é carregado, o sistema chama a função de leitura dos dados (de acordo com o tipo de arquivo) e depois chama a função de visualização para mostrar o mapa.

Botão de Tabela: Depois de exibir o mapa, o usuário pode clicar para ver os dados em formato de tabela.

A interface é simples, com a interação mínima, mas suficiente para testar a funcionalidade.

4. Entrypoint (main.py)
   O main.py é o entrypoint do projeto. Ele apenas importa e executa a função launch() da interface (que está em interface.py). Isso é o que realmente inicia o aplicativo Gradio.

Resumo da Lógica
Leitura de Arquivos:

O arquivo de entrada (CSV, JSON ou XML) é lido pelas funções em utils.py.

Cada tipo de arquivo é tratado por uma função diferente.

Exibição de Mapa:

Após ler os dados, o código em viz.py usa Plotly para criar um mapa interativo com os pontos de latitude e longitude.

Interface do Usuário:

Gradio é usado para criar a interface onde o usuário seleciona o arquivo, visualiza o mapa e vê a tabela de dados.

A lógica de exibição é controlada pela interface, que chama as funções de leitura e visualização.

Estrutura do Projeto:

O projeto é modularizado, com funções específicas para cada parte: leitura de dados, visualização e interface.

Isso facilita a manutenção e expansão do projeto, pois você pode adicionar novos tipos de arquivos ou novos tipos de visualizações sem mexer no restante do código.
