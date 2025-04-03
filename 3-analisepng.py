import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Função para coletar nomes dos produtos
def coletar_produtos():
    produtos = []
    num_produtos = 4  # Definindo para 4 produtos
    
    for i in range(num_produtos):
        componente = input(f"Digite o produto {i+1}: ")
        produtos.append(componente)
    
    return produtos

# Criação de dados de exemplo
def criar_dados_exemplo(produtos):
    # Verificando se temos os 4 produtos necessários
    if len(produtos) != 4:
        print("Precisamos de exatamente 4 produtos. Usando nomes padrão para produtos faltantes.")
        # Completando a lista se necessário
        while len(produtos) < 4:
            produtos.append(f"Produto {len(produtos)+1}")
    
    # Criando um conjunto de dados de exemplo para 4 produtos ao longo de 12 meses
    meses = pd.date_range(start='2024-01-01', periods=12, freq='M')
    # Criando um DataFrame vazio
    df = pd.DataFrame()
    
    # Gerando dados aleatórios para cada produto
    for i, produto in enumerate(produtos):
        # Gerando vendas com alguma sazonalidade e tendência
        if i == 0:
            vendas = np.random.normal(1000, 200, 12) + np.sin(np.linspace(0, 2*np.pi, 12)) * 300 + np.linspace(0, 200, 12)
        elif i == 1:
            vendas = np.random.normal(800, 150, 12) + np.cos(np.linspace(0, 2*np.pi, 12)) * 200 + np.linspace(100, 0, 12)
        elif i == 2:
            vendas = np.random.normal(1200, 250, 12) + np.sin(np.linspace(0, 4*np.pi, 12)) * 150 + np.linspace(50, 300, 12)
        else:  # Produto 4
            vendas = np.random.normal(600, 100, 12) + np.cos(np.linspace(0, 3*np.pi, 12)) * 100 + np.linspace(0, 150, 12)
        
        # Garantindo que não tenhamos valores negativos
        vendas = np.maximum(vendas, 0)
        
        # Criando um DataFrame temporário para este produto
        temp_df = pd.DataFrame({
            'Data': meses,
            'Produto': produto,
            'Quantidade': vendas.astype(int),
            'Preco_Unitario': np.random.uniform(50, 200, 12).round(2)
        })
        
        # Adicionando ao DataFrame principal
        df = pd.concat([df, temp_df])
    
    # Calculando o valor total de cada venda
    df['Valor_Total'] = df['Quantidade'] * df['Preco_Unitario']
    
    # Adicionando uma coluna de região
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste']
    df['Regiao'] = np.random.choice(regioes, size=len(df))
    
    # Resetando o índice
    df = df.reset_index(drop=True)
    
    return df

# Função principal
def main():
    print("Iniciando análise de vendas de 4 produtos...")
    
    # Coletando nomes dos produtos
    produtos = coletar_produtos()
    print(f"Produtos coletados: {produtos}")
    
    # Criando ou carregando dados
    print("Criando dados de exemplo com os produtos informados...")
    df = criar_dados_exemplo(produtos)
    # Salvando os dados para uso futuro
    df.to_csv('dados_vendas.csv', index=False)
    print("Dados de exemplo salvos em 'dados_vendas.csv'")
    
    # Analisando os dados
    print("\nRealizando análise dos dados...")
    resultado = analisar_vendas(df)
    
    # Exibindo resultados
    print("\nResultados da análise:")
    print("\n1. Vendas Totais por Produto:")
    print(resultado['vendas_por_produto'])
    
    print("\n2. Preço Médio por Produto:")
    print(resultado['preco_medio'])
    
    print("\n3. Produto Mais Vendido por Mês:")
    print(resultado['produto_mais_vendido_mes'])
    
    print("\n4. Crescimento Mensal:")
    print(resultado['crescimento_mensal'])
    
    # Visualizando os dados
    print("\nGerando visualizações...")
    visualizar_dados(df, resultado)
    
    print("\nAnálise concluída!")
    
    return df, resultado

# As funções analisar_vendas e visualizar_dados permanecem inalteradas
def analisar_vendas(df):
    # Resultado da análise
    resultado = {}
    
    # 1. Vendas totais por produto
    vendas_por_produto = df.groupby('Produto')['Valor_Total'].sum().reset_index()
    vendas_por_produto = vendas_por_produto.sort_values('Valor_Total', ascending=False)
    resultado['vendas_por_produto'] = vendas_por_produto
    
    # 2. Vendas mensais por produto
    vendas_mensais = df.copy()
    vendas_mensais['Mes'] = vendas_mensais['Data'].dt.strftime('%Y-%m')
    vendas_mensais_produto = vendas_mensais.groupby(['Mes', 'Produto'])['Valor_Total'].sum().reset_index()
    resultado['vendas_mensais_produto'] = vendas_mensais_produto
    
    # 3. Quantidade vendida por produto
    quantidade_por_produto = df.groupby('Produto')['Quantidade'].sum().reset_index()
    quantidade_por_produto = quantidade_por_produto.sort_values('Quantidade', ascending=False)
    resultado['quantidade_por_produto'] = quantidade_por_produto
    
    # 4. Vendas por região
    vendas_por_regiao = df.groupby(['Regiao', 'Produto'])['Valor_Total'].sum().reset_index()
    resultado['vendas_por_regiao'] = vendas_por_regiao
    
    # 5. Produto mais vendido por mês
    produto_mais_vendido_mes = vendas_mensais.groupby(['Mes', 'Produto'])['Quantidade'].sum().reset_index()
    idx = produto_mais_vendido_mes.groupby('Mes')['Quantidade'].idxmax()
    produto_mais_vendido_mes = produto_mais_vendido_mes.loc[idx]
    resultado['produto_mais_vendido_mes'] = produto_mais_vendido_mes
    
    # 6. Média de preço por produto
    preco_medio = df.groupby('Produto')['Preco_Unitario'].mean().reset_index()
    resultado['preco_medio'] = preco_medio
    
    # 7. Crescimento mensal
    vendas_mensais_total = vendas_mensais.groupby('Mes')['Valor_Total'].sum().reset_index()
    vendas_mensais_total['Crescimento'] = vendas_mensais_total['Valor_Total'].pct_change() * 100
    resultado['crescimento_mensal'] = vendas_mensais_total
    
    return resultado

def visualizar_dados(df, resultado):
    # Configurando o estilo dos gráficos
    plt.style.use('ggplot')
    
    # 1. Gráfico de barras para vendas totais por produto
    plt.figure(figsize=(12, 6))
    plt.bar(resultado['vendas_por_produto']['Produto'], resultado['vendas_por_produto']['Valor_Total'])
    plt.title('Vendas Totais por Produto')
    plt.xlabel('Produto')
    plt.ylabel('Valor Total (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('vendas_por_produto.png')
    
    # 2. Gráfico de linha para vendas mensais
    plt.figure(figsize=(14, 7))
    for produto in df['Produto'].unique():
        dados = resultado['vendas_mensais_produto'][resultado['vendas_mensais_produto']['Produto'] == produto]
        plt.plot(dados['Mes'], dados['Valor_Total'], marker='o', label=produto)
    plt.title('Vendas Mensais por Produto')
    plt.xlabel('Mês')
    plt.ylabel('Valor Total (R$)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('vendas_mensais.png')
    
    # 3. Gráfico de pizza para percentual de vendas por produto
    plt.figure(figsize=(10, 10))
    plt.pie(resultado['vendas_por_produto']['Valor_Total'], 
            labels=resultado['vendas_por_produto']['Produto'],
            autopct='%1.1f%%',
            startangle=90,
            shadow=True)
    plt.axis('equal')
    plt.title('Percentual de Vendas por Produto')
    plt.tight_layout()
    plt.savefig('percentual_vendas.png')
    
    # 4. Gráfico de barras empilhadas para vendas por região
    vendas_regiao_pivot = resultado['vendas_por_regiao'].pivot(index='Regiao', columns='Produto', values='Valor_Total')
    plt.figure(figsize=(12, 6))
    vendas_regiao_pivot.plot(kind='bar', stacked=True)
    plt.title('Vendas por Região e Produto')
    plt.xlabel('Região')
    plt.ylabel('Valor Total (R$)')
    plt.legend(title='Produto')
    plt.tight_layout()
    plt.savefig('vendas_por_regiao.png')
    
    # 5. Gráfico de linha para crescimento mensal
    plt.figure(figsize=(12, 6))
    plt.plot(resultado['crescimento_mensal']['Mes'][1:], resultado['crescimento_mensal']['Crescimento'][1:], marker='o', linestyle='-', color='blue')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('Taxa de Crescimento Mensal')
    plt.xlabel('Mês')
    plt.ylabel('Crescimento (%)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('crescimento_mensal.png')
    
    plt.close('all')
    print("Gráficos salvos com sucesso!")

# Executar o programa se este arquivo for executado diretamente
if __name__ == "__main__":
    df, resultado = main()