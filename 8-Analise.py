import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io
import base64

os.chdir(os.path.dirname(__file__))

# Inicializando o app Dash
app = dash.Dash(__name__)
# Carrega os dados de vendas, gerado pelo arquivo gerar.py
df = pd.read_csv('vendas.csv')

# Cria a classe para a estrutura de análise de dados
class AnalisadorDeVendas:
    def __init__(self, dados):
        # Inicializa a classe com o dataframe da tabela de vendas
        self.dados = dados
        self.limpar_dados()

    def limpar_dados(self):
        # Limpeza e preparação dos dados para análise com as demais funções
        self.dados['data'] = pd.to_datetime(self.dados['data'], errors='coerce')  # Converte as datas
        self.dados['valor'] = self.dados['valor'].replace({',': '.'}, regex=True).astype(float)
        self.dados['mes'] = self.dados['data'].dt.month
        self.dados['ano'] = self.dados['data'].dt.year
        self.dados['dia'] = self.dados['data'].dt.day
        self.dados['dia_da_semana'] = self.dados['data'].dt.weekday
        # Remove os dados ausentes nas colunas
        self.dados.dropna(subset=['produto', 'valor'], inplace=True)
        
    #gráfico de barras para vendas por produto
    def analise_vendas_por_produto(self, produtosFiltrados):
        df_produto = self.dados[self.dados['produto'].isin(produtosFiltrados)]
        df_produto = df_produto.groupby(['produto'])['valor'].sum().reset_index().sort_values(by='valor', ascending=True)
        fig = px.bar(
            df_produto,
            x='produto',
            y='valor',
            title="Vendas por Produto",
            color="valor"
        )
        return fig  # único objeto de figura
    
    #gráfico de pizza para vendas por região
    def analise_vendas_por_regiao(self, regioes_filtradas):
        df_regiao = self.dados[self.dados['regiao'].isin(regioes_filtradas)]
        df_regiao = df_regiao.groupby(['regiao'])['valor'].sum().reset_index().sort_values(by='valor', ascending = False)
        fig = px.pie(
            df_regiao,
            names='regiao',
            values='valor',
            title='vendas',
            color='valor'
        )
        return fig
    
   #gráfico de linhas para vendas por mês
    def analise_vendas_mensais(self, ano_filtrado):
        df_mes = self.dados[self.dados['ano'] == ano_filtrado]
        df_mes = df_mes.groupby(['ano', 'mes'])['valor'].sum().reset_index()
        fig = px.line(
            df_mes,
            x = 'mes',
            y = 'valor',
            color = 'ano',
            title = f'Vendas Mensais - {ano_filtrado}',
            markers = True,
            line_shape = 'spline'
        )
        return fig

    #gráfico de vendas diárias
    def analise_vendas_diarias(self, data_inicio, data_fim):
        df_dia = self.dados[(self.dados['data'] >= data_inicio) & (self.dados['data'] <= data_fim)]
        df_dia = df_dia.groupby('data')['valor'].sum().reset_index()
        fig = px.line(
            df_dia,
            x = 'data',
            y = 'valor',
            title = 'Vendas Diárias',
            markers = 'True'
        )
        return fig

    #grafico de vendas por dia da semana
    def analise_vendas_por_dia_da_semana(self):
        df_dia_semana = self.dados.groupby('dia_da_semana')['valor'].sum().reset_index()
        df_dia_semana['dia_da_semana'] = df_dia_semana['dia_da_semana'].map({
            0:'Segunda',
            1:'Terça',
            2:'Quarta',
            3:'Quinta',
            4:'Sexta',
            5:'Sábado',
            6:'Domingo'
        })
        fig = px.bar(
            df_dia_semana,
            x = 'dia_da_semana',
            y = 'valor',
            title = 'Vendas por dia da semana',
            color = 'valor'
        )
        return fig

    def analise_outliers(self):
        q1 = self.dados['valor'].quantile(0.25)
        q3 = self.dados['valor'].quantile(0.75)
        iqr = q3 - q1
        lim_inferior = q1 - 1.5 * iqr
        lim_superior = q3 + 1.5 * iqr
        outliers = self.dados[(self.dados['valor'] < lim_inferior) | (self.dados['valor'] < lim_superior)]
        fig = px.scatter(
            outliers,
            x = 'data',
            y = 'valor',
            title = 'Outliers de Vendas'
        )
        return fig

    def distribuicao_vendas(self):
        fig = px.histogram(
            self.dados,
            x = 'valor',
            title = 'Distribuição de vendas',
            nbins = 30
        )
        return fig

# análise de vendas
analise = AnalisadorDeVendas(df)

# app Dash
app.layout = html.Div([
    html.H1('Análise de Vendas', style={'text-align': 'center','margin-top':'-50px'}),
    # filtros de seleção para o painel
    html.Div([
        html.Label('PRODUTOS:', style={'color':'#ffffff','margin-left':'100px'}),
        dcc.Dropdown(
            id='produto-dropdown',
            options=[{'label': produto, 'value': produto} for produto in df['produto'].unique()],
            multi=True,
            value=df['produto'].unique().tolist(),
            style={'width': '100%','margin-left':'-95px'}
        ),
        html.Label('REGIÕES:', style={'color':'#ffffff','margin-left':'100px'}),
        dcc.Dropdown(
            id='regiao-dropdown',
            options=[{'label': regiao, 'value': regiao} for regiao in df['regiao'].unique()],
            multi=True,
            value=df['regiao'].unique().tolist(),
            style={'width': '100%','margin-left':'-95px'}
        ),
        html.Label('ANO:', style={'color':'#ffffff','margin-left':'40px'}),
        dcc.Dropdown(
            id='ano-dropdown',
            options=[{'label': str(ano), 'value': ano} for ano in df['ano'].unique()],
            value=df['ano'].min(),
            style={'width': '100%','margin-left':'-70px'}
        ),
        html.Label('PERÍODO:', style={'color':'#ffffff'}),
        dcc.DatePickerRange(
            id='data-picker-range',
            start_date=df['data'].min().date(),
            end_date=df['data'].max().date(),
            display_format='DD/MM/YY',
            style={'width': '100%','margin-left':'-180px','margin-top':'-20px'}
        ),
    ], style={'display': 'flex', 'margin-left':'20px' }),
    # Gráficos
    html.Div([
        dcc.Graph(id='grafico-produto'),
        dcc.Graph(id='grafico-regiao'),
        dcc.Graph(id='grafico-mensal'),
        dcc.Graph(id='grafico-diario'),
        dcc.Graph(id='grafico-dia-semana')
    ])
])

# Callback
@app.callback(
    Output('grafico-produto', 'figure'),
    Output('grafico-regiao', 'figure'),
    Output('grafico-mensal', 'figure'),
    Output('grafico-diario', 'figure'),
    Output('grafico-dia-semana', 'figure'),
    Input('produto-dropdown', 'value'),
    Input('regiao-dropdown', 'value'),
    Input('ano-dropdown', 'value'),
    Input('data-picker-range', 'start_date'),
    Input('data-picker-range', 'end_date')
)
def upgrade_graphs(produtos, regioes, ano, start_date, end_date):
    try:
        # Converte para o formato correto
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # Atualiza os gráficos 
        fig_produto = analise.analise_vendas_por_produto(produtos)
        fig_regiao = analise.analise_vendas_por_regiao(regioes)
        fig_mensal = analise.analise_vendas_mensais(ano)
        fig_diario = analise.analise_vendas_diarias(start_date, end_date)
        fig_dia_semana = analise.analise_vendas_por_dia_da_semana()
        return fig_produto, fig_regiao, fig_mensal, fig_diario, fig_dia_semana  # retorna todos os gráficos
    except Exception as e:
        # Sempre que ocorrer algum erro, retorna gráficos vazios
        print(f'Erro ao atualizar os gráficos: {str(e)}')
        empty_fig = go.Figure()  # Cria um gráfico vazio
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig  # Retorna gráficos vazios em caso de erro

# Rodar o app
if __name__ == '__main__':
    app.run(debug=True)