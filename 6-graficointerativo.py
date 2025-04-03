# Importando as bibliotecas necessaras
import dash #biblioteca principal para criar aplicativos dash
import dash_core_components as dcc # para utilizar componentes interativos
import dash_html_components as html #permite criar o html do aplicativo
import plotly.graph_objs as go #permite criar graficos interativos
from dash.dependencies import Input, Output #para definir callbacks

# Definindo a classe do aplicativo
class DashApp:
    def __init__(self): 
        #inicializa o aplicativo dash
        self.app = dash.Dash(__name__)
        # define o layout da aplicação
        self.layout = self.create_layout()
        #define o layout com a estrutura criada
        self.app.layout = self.layout
        # cria os callbacks para interação (interatividade do grafico)
        self.create_callbacks()

    # Método para definir o layout da aplicação
    def create_layout(self):
        # define a estrutura html do layout, utilizando os componentes do dash
        layout = html.Div([
            html.H1('Exemplo de Gráfico Interativo com Plotly e Dash'),
            
            # adiciona um grafico interativo na aplicação
            dcc.Graph(
                id='grafico-interativo', #define a id do grafico(importante para referenciar)
                figure=self.create_figure() #define a figura do grafico chamando create_figure
            ),
        ])
        return layout #retorna o layout configurado para ser usado na aplicação

    # Método para criar a figura do gráfico
    def create_figure(self):
        # dados para o grafico (exemplo de grafico de linha com pontos marcados)
        x = [1, 2, 3, 4, 5] 
        y = [10, 11, 12, 13, 14] 

        # Configuração do gráfico usando plotly
        figure = {
            'data': [
                go.Scatter( #cria um grafico de dispersão (scatter) com linhas e marcadores
                    x=x, 
                    y=y, 
                    mode='lines+markers', #define o tipo de grafico: linha com marcadores
                    name='Linha de Exemplo' # nome da linha do grafico
                )
            ],
            'layout': go.Layout( #configura o layout do grafico
                title='Gráfico Interativo', #titulo do grafico
                xaxis={'title': 'Eixo X'},  #titulo do eixo x
                yaxis={'title': 'Eixo Y'}   # titulo do eixo y
            )
        }
        return figure #retorna a figura configurada para o grafico

    # Método para adicionar callbacks (interatividade, se necessário)
    def create_callbacks(self):
        # define o callback para atualizar o gráfico
        @self.app.callback(
            Output('grafico-interativo', 'figure'), #define a saida do callback
            [Input('grafico-interativo', 'relayoutData')] #define a entrada do callback (dados de layout do grafico)
        )
        def update_graph(input_data):
            # função que atualiza o grafico (aqui por enquanto não altera nada)
            return self.create_figure() # retorna a figura do grafico sem mudanças neste momento.

    # Método para rodar o servidor da aplicação dash
    def run(self):
        #roda o servidor do dash tornando o apicativo acessivel pelo navegador no endereço local.
        self.app.run(debug=True)

# Instanciando e rodando o aplicativo
if __name__ == '__main__':
    app = DashApp() #cria uma instancia do aplicativo
    app.run()  #roda o servidor do dash iniciando a aplicação