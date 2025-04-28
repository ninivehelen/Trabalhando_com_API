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


#https://deividfortuna.github.io/fipe/   tem explicação de como coletar dados da API

#Esse código seria mais simples, mas aconteceu limite de acesso, ele estava funcionando coletando os dados

#Acessando o link da api principal
def acessando_api():
    while True:
        url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"

        response = requests.get(url)

        if response.status_code == 200:
            api_acesso = response.json()
            return api_acesso 
        
        elif response.status_code == 429:
            print("Limite atingido (429)")
            time.sleep(3)
        else:
          print("Erro ao acessar a API:", response.status_code)

#Acessar api novamente quando necessária 
def acessar_api_novamente(url):
    while True:
        response = requests.get(url)

        if response.status_code == 200:
            api_acesso = response.json()
            return api_acesso 
        else:
          print("Erro ao acessar a API:", response.status_code)
   
def coletando_dados(dados):
    #Para extrair os dados, é necessário seguir uma sequencia
    # pois, para ir extraindo marca, modelo, todos os parametros precisa do código anterior de cada um
    # Esse código segue esse padra, pega o codigo e vai repassando, acessando api e extraindo os dados
    # Poŕem deu erro de limite, então precisa do token para continuar
    # mas é mais simples que o outro código
    for dados_api in  dados:
      codigo_carros = dados_api['codigo']
      url = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_carros}/modelos'
      modelo = acessar_api_novamente(url)
      for dados_modelo in modelo['modelos']:
          codigo_modelo = dados_modelo['codigo']
          url = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_carros}/modelos/{codigo_modelo}/anos'
          ano = acessar_api_novamente(url)
          for dado_ano in ano:
           ano_codigo = dado_ano['codigo']
           url = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_carros}/modelos/{codigo_modelo}/anos/{ano_codigo}'
           dados = acessar_api_novamente(url)
           print(dados)
           salvar_dados(dados)
    
    print("Dados extraídos e salvos")

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
        df.to_csv(f'extra_dados_script1_info_carros_{hora_atu}.csv', sep = ',', mode = 'a', encoding='utf-8', index=False)  
        # Mostrar o data set quando salvo
        print(df)
    else:
       print("Todos os dados extráidos")

# Função principal
if __name__ == '__main__':
    response_indicarores = acessando_api()
    #Função para coletar dados e chamar as outras funções
    coletando_dados(response_indicarores)
   