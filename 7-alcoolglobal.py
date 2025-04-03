# Flask: Framework web para Python, utilizado para criar a aplicação web.

# pandas: Biblioteca para manipulação e análise de dados, que é usada aqui para ler e manipular os dados do arquivo CSV e do banco de dados SQLite.

# sqlite3: Biblioteca para interagir com bancos de dados SQLite.

# plotly.express: Biblioteca para criação de gráficos interativos de maneira simples.

# plotly.io: Usado para configurar o renderer (método de exibição) dos gráficos.

# random: Biblioteca para gerar números aleatórios (não usada explicitamente no código mostrado).
from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random

# Configura o método de renderização do Plotly para exibir gráficos diretamente no navegador.
pio.renderers.default = "browser"

# Carrega o arquivo CSV que contém os dados sobre o consumo de bebidas alcoólicas em vários países para um DataFrame do Pandas.
df = pd.read_csv(r"C:\Prof.eduardo\xpert\drinks.csv")

# Conecta ao banco de dados SQLite consumo_alcool.db.

# O DataFrame df (lido do CSV) é convertido em uma tabela chamada "drinks" no banco de dados SQLite. Caso já exista uma tabela com esse nome, ela será substituída.

# As mudanças são confirmadas (commit) e a conexão com o banco de dados é fechada.
conn = sqlite3.connect(r"C:\Prof.eduardo\xpert\consumo_alcool.db")

df.to_sql("drinks", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

# Cria uma instância do aplicativo Flask.
app = Flask(__name__)

# código html + css para montagem da página
html_template = '''
<head>
<style type="text/css">
a{
    text-decoration: none;
    padding: 8px 16px; 
    background-color: #3498db;
    color: white;
    border: 2px solid #2980b9;
    border-radius: 12px;
    transition: all 0.3s ease;
}
a:hover{
    text-decoration: underline;
}
</style></head><body>
    <div align="center">
        <h1>DashBoard - Consumo de Alcool</h1>
        <h2>
        <ul style="display:inline; list-style:none; padding:0;">
            <li style="display:inline-block; margin-right: 10px;">
                <a href="/grafico1">Top 10 países em consumo</a>
            </li>
            <li style="display:inline-block; margin-right: 10px;">
                <a href="/grafico2">Média de consumo por tipo</a>
            </li>
            <li style="display:inline-block; margin-right: 10px;">
                <a href="/grafico3">Consumo total por região</a>
            </li>
        </ul></h2><br>
        <!-- Use relative path to the static folder -->
        <img src="{{ url_for('static', filename='drink.jpg') }}">
    </div>
</body>
'''
@app.route('/')
def index():
    return render_template_string(html_template)

# A rota /grafico1 executa uma consulta SQL para obter os 10 países com o maior consumo de álcool.

# O resultado é utilizado para gerar um gráfico de barras utilizando Plotly.

# O gráfico é renderizado em HTML e o botão "VOLTAR" é adicionado para retornar à página inicial.
@app.route('/grafico1')
def grafico1():
    conn = sqlite3.connect(r"C:\Prof.eduardo\xpert\consumo_alcool.db")
    df = pd.read_sql_query('''
    SELECT country, total_litres_of_pure_alcohol FROM drinks ORDER BY total_litres_of_pure_alcohol DESC LIMIT 10
    ''', conn)
    conn.close()
    fig = px.bar(
        df,
        x = "country",
        y = "total_litres_of_pure_alcohol",
        title = "TOP 10 MAIORES CONSUMIDORES DE ALCOOL"
    )
    return fig.to_html() + "<div align='center'><br><br><a href='/' style='text-decoration: none; padding: 8px 16px; background-color: #3498db; color: white;border: 2px solid #2980b9; border-radius: 12px;transition: all 0.3s ease;'>VOLTAR</a></div>"

# A rota /grafico2 calcula a média de consumo de cerveja, destilados e vinhos e gera um gráfico de barras com essas médias.

# A função melt() do Pandas é usada para reorganizar os dados para que fiquem no formato adequado para o gráfico.
@app.route('/grafico2')
def grafico2():
    conn = sqlite3.connect(r"C:\Prof.eduardo\xpert\consumo_alcool.db")
    df = pd.read_sql_query('''
    SELECT AVG(beer_servings) AS cerveja, AVG(spirit_servings) AS destilados, AVG(wine_servings) AS vinhos FROM drinks
    ''', conn)
    conn.close()
    df_melted = df.melt(var_name="Bebidas", value_name="Média de Porções")
    fig = px.bar(df_melted, x="Bebidas", y="Média de Porções", title="CONSUMO GLOBAL POR TIPO - MÉDIA")
    return fig.to_html() + "<div align='center'><br><br><a href='/' style='text-decoration: none; padding: 8px 16px; background-color: #3498db; color: white;border: 2px solid #2980b9; border-radius: 12px;transition: all 0.3s ease;'>VOLTAR</a></div>"

# A rota /grafico3 calcula o consumo total de álcool por região (Europa, Ásia, África, e Américas).

# Para cada região, a consulta SQL é realizada para somar o consumo dos países dessa região.

# O resultado é utilizado para gerar um gráfico de pizza (pie chart) com o consumo total por região.
@app.route('/grafico3')
def grafico3():
    regioes = {
        "Europa": ["France", "Germany", "Italy", "Spain", "Portugal", "UK"],
        "Asia":  ["China","Japan","India","Thailand"],
        "Africa":  ["Angola","Nigeria","Egypt","Algeria"],
        "Americas":  ["USA","Brazil","Canada","Argentina","Mexico"]
    }
    dados = []
    conn = sqlite3.connect(r"C:\Prof.eduardo\xpert\consumo_alcool.db")
    for regiao, paises in regioes.items():
        placeholders = ",".join([f"'{p}'" for p in paises])
        query =  f"""
            SELECT SUM(total_litres_of_pure_alcohol) as total FROM drinks WHERE country IN ({placeholders})
        """
        total = pd.read_sql_query(query, conn).iloc[0]['total'] or 0
        dados.append({"Região": regiao, "Consumo Total":total})
    conn.close()
    df_regioes = pd.DataFrame(dados)
    fig = px.pie(df_regioes, names="Região", values="Consumo Total", title="Consumo total por região do mundo")
    return fig.to_html() + "<div align='center'><br><br><a href='/' style='text-decoration: none; padding: 8px 16px; background-color: #3498db; color: white;border: 2px solid #2980b9; border-radius: 12px;transition: all 0.3s ease;'>VOLTAR</a></div>"

# inicia o servidor flask
if __name__ == "__main__":
    app.run(debug=True)