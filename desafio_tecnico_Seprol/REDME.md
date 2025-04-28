
# Seprol - IT by Experts - Processo Seletivo - Analista de Dados Júnior 

Descrição do desáfio:

"Seu cliente deseja ter os valores da tabela fipe de todos os veículos do tipo "carros" e da última data de referência disponível. Após algumas pesquisas, você se deparou com uma API pública que pode usar de referência:
https://github.com/giovanigenerali/fipe-json?tab=readme-ov-file"

# Desenvolvimento do código para resolver o desáfio

Criei dois códigos para resolver, o primeiro ambos são idependentes e extrai os dados.
Ambos feitos em Python

1. Primeiro código: extracao_dados_api.py extrai os dados utilizando a explicação do site da API 
https://deividfortuna.github.io/fipe/ 

Eu comecei fazendo este código, porém tem limitaçoes de acesso, então o segundo usa a do github os HEADERS:
https://github.com/giovanigenerali/fipe-json?tab=readme-ov-file"

2. Segundo código: extracao_dados_2_api.py
Esse extrair os dados utilizando os HEADERS o código é maior e consegue ter mais acesso na requisição.

Como rodar:
É necessário ter o pandas instalado 
comando: pip install pandas

O pandas foi utlizado pra salvar a tabela em csv. 

## Para rodar é simples.

Compile extracao_dados_api.py ou extracao_dados_2_api.py, espere até completar a extração. Durante o processo de extração dos dados é salvo um csv contendo os dados extraídos, também é apresentado durante o processo de extração os dados na saída do terminal.

## Autores

- [@ninivehelen](https://github.com/ninivehelen)
