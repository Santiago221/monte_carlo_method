import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy  as np
from tqdm import tqdm

## Intevalo de Confiança
p = 0.9545
## Amostras
M = 1e5

## Barras histograma
bars = 500
## Variáveis
variables = {'Massa':[[1.5,2],['Retangular']],
             'L':[[2.9,3.3],['Retangular']],
             'W':[[1,0.2],['Gauss']],
             'H':[[0.9,1.1],['Triangular']]}

def Func_Forma(data):
    '''
    Retorna um resultado dependendo da função de forma utilizada para a variável
    Retangular - algum valor entre o mínimo e o máximo
    Triangular - algum valor entre o mínimo e o máximo
    Gaussiana - algum valor a média e o desvio padrão
    '''
    if len(data) > 1:
        if data[1][0] == 'Retangular':
            value = random.uniform(data[0][0], data[0][1])
            return value
        elif data[1][0] == 'Gauss':
            value = random.gauss(data[0][0], data[0][1])
            return value
        elif data[1][0] == 'Triangular':
            value = random.triangular(data[0][0], data[0][1])
            return value
    else:
        value = data[0]
        return value

def Robot_Model(variables):
    '''
    Define o modelo do Robô
    Importante retornar apenas as variáveis de interesse para reduzir problemas de alocamneto de memória
    '''

    M = Func_Forma(variables['Massa'])
    L = Func_Forma(variables['L'])
    H = Func_Forma(variables['H'])
    W  = Func_Forma(variables['W'])



    Ixr = M * (L**2 + H**2)/12
    Iyr = M * (L ** 2 + W ** 2) / 12
    Izr = M * (W ** 2 + H ** 2) / 12
    return M, L, H, W, Ixr, Iyr , Izr

## Roda e armazena o model odo robô para M testes.
matriz_resultados = []
for i in tqdm(range(int(M)),desc="Processing Monte Carlo Method: "):
    resultados = Robot_Model(variables)
    matriz_resultados.append(resultados)

# Salva os dados em um data frame
df = pd.DataFrame(np.array(matriz_resultados), columns = ['M', 'L', 'H', 'W', 'Ixr', 'Iyr' , 'Izr'])
df.to_csv('Resultados.csv')

# Mostra os Resultados
fig, ax = plt.subplots(1,4,tight_layout=True)

ax[0].hist(df['M'],bins=bars)
ax[0].set_title('Massa')
ax[1].hist(df['L'],bins=bars)
ax[1].set_title('L')
ax[2].hist(df['H'],bins=bars)
ax[2].set_title('H')
ax[3].hist(df['W'],bins=bars)
ax[3].set_title('W')



fig2, ax2 = plt.subplots(1,3,tight_layout=True)

ax2[0].hist(df['Ixr'],bins=bars)
ax2[0].set_title('Ixr')

ax2[1].hist(df['Iyr'],bins=bars)
ax2[1].set_title('Iyr')

ax2[2].hist(df['Izr'],bins=bars)
ax2[2].set_title('Izr')

plt.show()

