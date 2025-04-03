import pandas as pd
import random
from datetime import datetime, timedelta

def gerar_dados_vendas(num_linhas):
    regioes = ["Norte","Nordeste","Sul","Sudeste","Centro","Centro-Oeste"]
    dados = []
    
    for xis in range(num_linhas):
        produto = random.choice(produtos)
        regiao = random.choice(regioes)
        valor = round(random.uniform(31,484),2)
        data = datetime.today() - timedelta(days=random.randint(0,364))
        dados.append([produto, regiao, valor, data])
    return dados

produtos = []
produto = 4
contador = 1

if  contador >= 1 and contador < produto:
    for i in range(produto):
        componente = str(input(f"Digite o produto {contador} : "))
        produtos.append(componente)
        contador += 1

dados_vendas = gerar_dados_vendas(100)

df_vendas = pd.DataFrame(dados_vendas, columns=['produto','regiao','valor','data'])

df_vendas.to_csv('vendas.csv', index=False)

print("Arquivo vendas criado com sucesso")
      