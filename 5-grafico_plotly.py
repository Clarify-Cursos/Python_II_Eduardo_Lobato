# Flask: É um framework para criar aplicações web em Python. Aqui, estamos importando o Flask para criar o aplicativo e render_template_string para renderizar uma string de template diretamente no código.

# Plotly Express (plotly.express): Uma biblioteca muito popular para criação de gráficos interativos. Aqui, você está utilizando para criar um gráfico de pizza.

# Pandas: Biblioteca para manipulação e análise de dados, usada aqui para criar e manipular um DataFrame.

from flask import Flask, render_template_string
import plotly.express as px
import pandas as pd

# Inicia o Flask
app = Flask(__name__)

# Cria nosso dataframe.Esse DataFrame possui uma coluna chamada Status, com vários valores representando o status de algo (como "Ativo", "Inativo", "Cancelado"). O DataFrame é criado com 9 entradas.
df_consolidado = pd.DataFrame({
    'Status': [
        'Ativo',
        'Inativo',
        'Ativo',
        'Inativo',
        'Ativo',
        'Inativo',
        'cancelado',
        'cancelado',
        'Ativo'
    ]
})

# Rota do gráfico de pizza usando o plotly.@app.route('/'): Define uma rota para o caminho raiz ('/'). Quando o usuário acessa a URL principal do aplicativo, a função grafico_pizza() será chamada.
@app.route('/')
def grafico_pizza():
    # Contar as ocorrências de cada status
    status_dist = df_consolidado['Status'].value_counts().reset_index()
    status_dist.columns = ['Status', 'Quantidade']

    # Criar o gráfico com plotly.Aqui, você cria um gráfico de pizza usando a função px.pie() da biblioteca Plotly.O gráfico é gerado a partir do DataFrame status_dist, usando a coluna 'Quantidade' para os valores (tamanho das fatias da pizza) e a coluna 'Status' para os nomes das fatias.
    fig = px.pie(
        status_dist,
        values='Quantidade',
        names='Status',
        title='Distribuição do Status'
    )

    # Converter o gráfico para HTML (isso já gera um HTML pronto com <div>, <style>, e { })
    grafico_html = fig.to_html(full_html=False)

    html = '''
        <html>
            <head>
                <meta charset="UTF-8">
                <title>Prof. Eduardo - Gráfico Python</title>
            </head>
            <body>
                <h2>Gráfico com plotly</h2>
                <!-- Aqui usamos {{ grafico_html | safe }} ao invés de {grafico_html} -->
                {{ grafico_html | safe }}
            </body>
        </html>
    '''

    # Passamos a variável grafico_html como argumento para o template
    return render_template_string(html, grafico_html=grafico_html)

if __name__ == '__main__':
    app.run(debug=True)
