import requests
import time
import pandas as pd 
import datetime
import locale

# Para ter certeza que o mes de referência é o atual compara com o mes e ano atual
# Porém notei que a API já faz isso, puxa dados do mes e ano atual, mas esta tendo o confere por garantia de esta pegando mes e ano atual 
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
mes_ano = datetime.date.today()
atual = mes_ano.strftime("%B de %Y")

#Para salvar sempre um novo arquivo com a data nova, para sabel qual é o atual
# Caso o codigo der erro nao precise excluir o arquivo antes de rodar novamente
hora_atual = datetime.datetime.now()
hora_atu = hora_atual.strftime("%H:%M:%S")

# Headers da API no site Github da API tem
HEADERS = {
    'Content-Type': 'application/json',
    'Referer': 'https://veiculos.fipe.org.br/'
}

# URL de inicio padrao para cada extração
inicio_url = 'https://veiculos.fipe.org.br/api/veiculos'

# Requisição na Api. Caso a API der erro de limite vai ter um time para tentar novamente.
def acessando_api(url, body=None):
    # Contador para o número de tentativas
    tentativas = 0
    while True:
        try:
            # Envia a requisição POST
            response = requests.post(url, headers=HEADERS, json=body)

            # Conexão bem-sucedida
            if response.status_code == 200:
                return response.json()
            
            # Limite de requisições atingido 429
            elif response.status_code == 429:
                tentativas += 1
                atraso = min(2 ** tentativas, 60)  # Tentativa (até 60 segundos)
                print(f"Limite atingido 429. Tentando novamente em {atraso} segundos...")
                time.sleep(atraso)

            # Outros erros de conexão ou de servidor
            else:
                print(f"Erro ao acessar API {url}: {response.status_code}")
                return None

        # Verfica exceções de rede, problemas de conexão
        except requests.exceptions.RequestException as e:
            tentativas += 1
            atraso = min(2 ** tentativas, 60)  # Tentativa (até 60 segundos)
            print(f"Erro de rede ou conexão: {e}. Tentando novamente em {atraso} segundos...")
            time.sleep(atraso)
        
#Para acessar API que inicia os dados, pois para progredir com extração precida do código dessa tabela
def acessando_tabela_principal():
    url = f'{inicio_url}/ConsultarTabelaDeReferencia'
    return acessando_api(url)

# Para extrair esse dado precisa do código da tabela Consulta tabela referência a função acima
def extraindo_marca(codigo_tabela_referencial, tipo_veiculo=1):
    url = f'{inicio_url}/ConsultarMarcas'

    #Esse body é dado pela API no Github
    Body = {
        "codigoTabelaReferencia": codigo_tabela_referencial,
        "codigoTipoVeiculo": tipo_veiculo
    }
    return acessando_api(url, Body)

# Para extrair precisa do código extraido das duas funções acima.
def extraindo_modelo(codigo_tabela_referencial, codigo_marca, tipo_veiculo=1):
    url = f'{inicio_url}/ConsultarModelos'

    #Esse body é dado pela API no Github
    Body = {
        "codigoTabelaReferencia": codigo_tabela_referencial,
        "codigoTipoVeiculo": tipo_veiculo,
        "codigoMarca": codigo_marca
    }
    response = acessando_api(url, Body)
    if response:
        return response.get('Modelos', [])
    else:
        return []
# Para extrair precisa do código dos códigos extrídos das funções acima.
def extrair_anos(codigo_tabela_referencial, codigo_marca, codigo_modelo, tipo_veiculo=1):
    url = f'{inicio_url}/ConsultarAnoModelo'

    #Esse body é dado pela API no Github
    Body = {
        "codigoTabelaReferencia": codigo_tabela_referencial,
        "codigoTipoVeiculo": tipo_veiculo,
        "codigoMarca": codigo_marca,
        "codigoModelo": codigo_modelo
    }
    return acessando_api(url, Body)

# Precisa de todos os códigos das funções acima.
# Está tabela é a que contém todas as informaçẽs.
def extrair_valor(codigo_tabela, codigo_marca, codigo_modelo, ano_modelo, codigo_combustivel, tipo_veiculo=1):
    url = f'{inicio_url}/ConsultarValorComTodosParametros'

    #Esse body é dado pela API no Github
    Body = {
        "codigoTabelaReferencia": codigo_tabela,
        "codigoTipoVeiculo": tipo_veiculo,
        "codigoMarca": codigo_marca,
        "codigoModelo": codigo_modelo,
        "anoModelo": ano_modelo,
        "codigoTipoCombustivel": codigo_combustivel,
        "tipoVeiculo": tipo_veiculo,
        "tipoConsulta": "tradicional"
    }
    return acessando_api(url, Body)

# Função que chama as funções acima e extrai os dados
def coletando_dados():
    dados_valores = []
    dados_tab_referencia = acessando_tabela_principal()
    
    # Código é o primeiro da tabela por isso o O 
    codigo_tab_referencial = dados_tab_referencia[0]['Codigo']
    marcas = extraindo_marca(codigo_tab_referencial)

    # Esse value e label contém a saída a no github da API 
    for marca in marcas:
        codigo_marca = marca['Value']
        nome_marca = marca['Label']
    
    # Agora só pecorre e passar o codigo da extração anterior para a proxima
    # A resposta de função ir pecorrendo cada uma e salvado os dados.
        print("Extraindo marca")
        modelos = extraindo_modelo(codigo_tab_referencial, codigo_marca)
        
        # Esse value e label contém a saída a no github da API 

        for modelo in modelos:
            codigo_modelo = modelo['Value']
            nome_modelo = modelo['Label']
            
            print("Extraindo modelo e ano")
            ano = extrair_anos(codigo_tab_referencial, codigo_marca, codigo_modelo)
            
            for anos in ano:
                # O ano e o combustivel é um dic, foi partido para pegar a informação
                if isinstance(anos, dict) and 'Value' in anos:
                    partido_valor = anos['Value'].split('-')
                    if len(partido_valor ) == 2:
                        
                        #Precisou converte, pois são inteiros
                        ano_modelo = int(partido_valor[0])
                        codigo_combustivel = int(partido_valor[1])

                        #Extraindo dados que contém varias informações      
                        print("Extraindo todos os valores do parametro")
                        dado_valor = extrair_valor(
                                    codigo_tab_referencial,
                                    codigo_marca,
                                    codigo_modelo,
                                    ano_modelo,
                                    codigo_combustivel
                                )
                        salvar_dados(dado_valor)
            time.sleep(0.5)  

# Função para salvar os dados usando pandas 
def salvar_dados(dados):
    dados_valores = []
    # Precisa verificar se existe ainda informação para salvar
    if dados.get('CodigoFipe') != None:
       mes_referencia = dados.get('MesReferencia').strip()
       #Conferindo se o mes de refência é igual atual, para pegar dados atuais
       if mes_referencia == atual: 
        dados_valores.append({
        'CodigoFipe': dados.get('CodigoFipe'),
        'MesReferencia': dados.get('MesReferencia'),
        'Marca': dados.get('Marca'),
        'Modelo': dados.get('Modelo'),
        'AnoModelo': dados.get('AnoModelo'),
        'Combustivel': dados.get('Combustivel'),
        'Valor': dados.get('Valor')
        })
        df = pd.DataFrame(dados_valores)
        df.to_csv(f'extra_dados_script2_info_carros_{hora_atu}.csv', sep = ',', mode = 'a', encoding='utf-8', index=False)  
        # Mostrar o data set quando salvo
        print(df)
    else:
       print("Todos os dados extráidos")

# Função principal
if __name__ == '__main__':
    #Função para coletar dados e chamar as outras funções
    coletando_dados()
   
