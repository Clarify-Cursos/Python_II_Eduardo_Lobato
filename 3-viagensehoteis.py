import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
from matplotlib import pyplot

dfNY = pd.read_csv("https://www.dropbox.com/s/8i2nw6bd5ha7vny/listingsNY.csv?dl=1")
dfRJ = pd.read_csv("https://www.dropbox.com/s/yyg8hso7fbjf1ft/listingsRJ.csv?dl=1")


# id = identificação de cada imóvel
# hot_id = o número de identificação do anfitrião
# neighboarhood_group: conjunto de grupo de bairro
# latitude - coordenada latitude
# longitude - coordenada longitude
# room_type = o tipo de quarto
# price = valor da pernoite do imovel
# minimun_nights = noites minimas para locação
# number of reviews = numero de avaliações
# last_review = data da última avaliação
# reviews_per_mounth: quantidade de avaliações por mês
# calculed_host_listing_count - quantidade de imoveis do mesmo
# availability_365: dias que o anuncio esta disponivel por ano
# number_reviews_ltm: avaliações nos últimos 12 meses
# license: nenhum valor valido
# https://servicodados.ibge.gov.br/api/docs - site de serviço de dados do IBGE
# https://brasil.io/home/ - Dados para treinar python e power BI
# camelcase - variavelUtilizada
# snakecase - variavel_utilizada


display(dfNY.head(5))
display(dfRJ.head(5))

print(f'New York\nEntradas: {dfNY.shape[0]}\nVariáveis: {dfNY.shape[1]}\n')
print(f'Rio de Janeiro\nEntradas: {dfRJ.shape[0]}\nVariáveis: {dfRJ.shape[1]}\n')

display(dfNY.dtypes)
display(dfRJ.dtypes)

dfNY.last_review = pd.to_datetime(dfNY.last_review, format="%Y-%m-%d")
dfRJ.last_review = pd.to_datetime(dfRJ.last_review, format="%Y-%m-%d")

dfNY['year'] = dfNY.last_review.dt.year
dfNY.price = dfNY.price.mask(dfNY.year <= 2011, (dfNY.price / 1.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2012, (dfNY.price / 1.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2013, (dfNY.price / 2.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2014, (dfNY.price / 2.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2015, (dfNY.price / 3.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2016, (dfNY.price / 3.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2017, (dfNY.price / 3.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2018, (dfNY.price / 4.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2019, (dfNY.price / 4.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2020, (dfNY.price / 5.674))
dfNY.price = dfNY.price.mask(dfNY.year <= 2021, (dfNY.price / 5.674))

variaveis = ['id', 'name', 'host_id', 'host_name', 'neighbourhood_group', 'neighbourhood',
            'latitude', 'longitude', 'room_type', 'price', 'minimum_nights', 'number_of_reviews',
            'last_review', 'reviews_per_month', 'calculated_host_listings_count', 'availability_365',
            'number_of_reviews_ltm', 'license']

vz = [] #criação de um array vazio
dado = []

'''
Aqui, estamos verificando o seguinte: através do índice, verificamos os campos que estão vazios e somando
os mesmos. com essa soma, dividimos pela média dos campos preenchidos e adicionamos os resultados no
array vz. Ao final, limpamos o array dado
'''
for i in variaveis:
    dado.append(dfNY[i].isnull().sum() / dfNY[i].shape[0])
    dado.append(dfRJ[i].isnull().sum() / dfRJ[i].shape[0])
    vz.append(dado[:])
    dado.clear()
vz

pd.DataFrame(vz, columns=['New York','Rio de Janeiro'], index=variaveis)

''' 
gerar gráfico com os dados
'''

dfNY_clean = dfNY.dropna(subset=['name','host_name'], axis=0) #limpeza dos campos nulos(NaN) do eixo x, ou
                                                              #especificados nos registros, ou seja, linhas
dfRJ_clean = dfRJ.dropna(subset=['name','host_name'], axis=0)

#calculando a mediana e inserindo o valor na variavel
rpm_ny_median = dfNY_clean.reviews_per_month.median()

#pegando o valor da variável rpm_my_median e inserindo à Dfny_clean
dfNY_clean = dfNY_clean.fillna({"reviews_per_month":rpm_ny_median})

#pegando o valor de dfNY_clean, no campo last_review e definindo como datetime  
lr_ny_median = dfNY_clean['last_review'].astype('datetime64[ns]').quantile(0.5, interpolation="midpoint")

#pegando o valor da variável last_review e inserindo à Dfny_clean
dfNY_clean = dfNY_clean.fillna({"last_review":lr_ny_median})

#calculando a mediana e inserindo o valor na variavel
rpm_rj_median = dfRJ_clean.reviews_per_month.median()

#pegando o valor da variável rpm_my_median e inserindo à Dfny_clean
dfRJ_clean = dfRJ_clean.fillna({"reviews_per_month":rpm_rj_median})

#pegando o valor de dfNY_clean, no campo last_review e definindo como datetime  
lr_rj_median = dfRJ_clean['last_review'].astype('datetime64[ns]').quantile(0.5, interpolation="midpoint")

#pegando o valor da variável last_review e inserindo à Dfny_clean
dfRJ_clean = dfRJ_clean.fillna({"last_review":lr_rj_median})

#fazendo o gráfico:
'''criando a variável dx0 e inserindo nela os campos price e minimum_nights'''
dx0 = ['price', 'minimum_nights']

for n in dx0:
    data_a = dfNY_clean[n]
    data_b = dfRJ_clean[n]
    data_2d = [data_a, data_b]
    plt.boxplot(data_2d, vert = False, labels=["New York", "Rio de Janeiro"])
    plt.title(n)
    plt.show()

    dfNY_clean[['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'calculated_host_listings_count', 'availability_365']].describe()

    dfRJ_clean[['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'calculated_host_listings_count', 'availability_365']].describe()

    '''
    defino a variável dfNY_out e nele aplico uma cópia de dfNY_clean. Daí, eu defino para apagar os dados
    (drop) quando a propriedade price for maior que 1100, no eixo X, no local.
    '''
    dfNY_out = dfNY_clean.copy()
    dfNY_out.drop(dfNY_out[dfNY_out.price > 1100].index, axis=0, inplace=True)
    dfNY_out.drop(dfNY_out[dfNY_out.minimum_nights > 66].index, axis=0, inplace=True)

    dfRJ_out = dfRJ_clean.copy()
    dfRJ_out.drop(dfRJ_out[dfRJ_out.price > 600].index, axis=0, inplace=True)
    dfRJ_out.drop(dfRJ_out[dfRJ_out.minimum_nights > 4].index, axis=0, inplace=True)

    var = [ 'Entire home/apt',
            'Private room',
            'Shared room',
            'Hotel room' ]

    dado_var = {}
    for i in var:
        dado_var[i] = [ dfNY_out.loc[dfNY_out.room_type == i].shape[0] / dfNY_out.room_type.shape[0] , 
                        dfRJ_out.loc[dfRJ_out.room_type == i].shape[0] / dfRJ_out.room_type.shape[0] ]

    ima = pd.DataFrame(dado_var, index=['New York','Rio de Janeiro'])
    ima.plot(kind="barh", stacked=True, figsize=(6,4), color=['c','m','y','orange'])
    plt.legend(loc="lower left", bbox_to_anchor=(0.8,1.0))
    plt.show()
