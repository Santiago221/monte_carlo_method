import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy  as np
from tqdm import tqdm

## Intevalo de Confiança
p = 0.9545
## Amostras
M = 1e4

## Barras histograma
bars = 500
## Variáveis
v = {### Dimensões do Robô
            'Massa':[[1.5,2],['Retangular']],                          #Massa              [tonelada]
            'L':3,                                                      #Comprimento        [m]
            'W':1,                                                   #Largura            [m]
            'H':1,                                                   #Altura             [m]
            'Nr':4,
            ### Onda e Corrente
            'w':0.1,                                                  #Frequência angular [rad/s]
            'Hw':1,                                                   #Amplitude da onda  [m]
            'c':[[0.3,0.6],['Retangular']],                            #Corrente           [m/s]
            'v_cin_h2o':1.37E-6,                                      #Viscosidade H2O    [m²/s]
            'rho_h2o':1100,
            ### Posição Longitudinal
            'rx':161,                                                 #longitudinal       [m]
            'ry':32,                                                  #transversal       [m]
            'rz':10,                                                  #elevação       [m]
            ### Elemento Flexível
            'Lf':0.35,                                                #Comprmento [m]
            'Ef':1,                                                   #Módulo de Elasticidade [GPa]
            'Sf':10,                                                  #Limite de Escoamento [MPa]
            'hf':0.02,                                                #Seção Transversal [m]
            'tf':0.01,
            'Nf':11,                                                   #Quantidade de Elementos
            ### Mangote
            'w_m':30,                                                  #
            'To_m':300,
            'S_m':30,
            'ODm':100,                                                   # [mm]
            'IDm':75,
            'Qs':25,
            'x':15,
            'Pm':2200,
            'Ncb':6,
            'Qcb':22,
            ### Dados Operacionais
            'VaZ':0.1,
            'Rtrit':200,
            'Nt':7,
            'Ndt':23,
            'az':0.1,
            'mi':0.3
            }



def Func_Forma(data):
    '''
    Retorna um resultado dependendo da função de forma utilizada para a variável
    Retangular - algum valor entre o mínimo e o máximo
    Triangular - algum valor entre o mínimo e o máximo
    Gaussiana - algum valor a média e o desvio padrão
    '''
    try:
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
    except:
        value = data
        return value

def Robot_Model(v):
    '''
    Define o modelo do Robô
    Importante retornar apenas as variáveis de interesse para reduzir problemas de alocamneto de memória
    '''

    M = Func_Forma(v['Massa'])
    c = Func_Forma(v['c'])

    #Momentos de Inércia
    Ixr = M * (v['L']**2 + v['H']**2)/12
    Iyr = M * (v['L'] ** 2 + v['W'] ** 2) / 12
    Izr = M * (v['W'] ** 2 + v['H'] ** 2) / 12

    #Amplitudes:
    Su = v['Hw']*0.5
    Sw = v['Hw']*0.95
    He = v['Hw']*1
    Ro = v['Hw']*0.1*180/np.pi
    Pi = v['Hw']*0.1*180/np.pi
    Ya = v['Hw']*0.0254*180/np.pi

    f = v['w']/(2*np.pi)
    T = 1/f


    Spitch = v['rx'] * np.pi * Pi / 180
    Sroll = v['ry'] * np.pi * Pi / 180
    Syall = v['rz'] * np.pi * Pi / 180

    #Direção Z
    Vz = [0,0,He/T,Spitch/T,Sroll/T,0] # surge,sway,heave,pitch,roll,yaw
    Vy = [0, Sw/T, He/T, 0, Sroll/T, Syall/T]  # surge,sway,heave,pitch,roll,yaw
    Vx = [Su/T,0,0,Spitch/T,0,Syall/T] # surge,sway,heave,pitch,roll,yaw

    vr = [Vx,Vy,Vz]
    Va = [c,0,v['VaZ']]
    Vr = np.zeros(3)
    for i in range(3):
        v_r = 0
        for ii in range(len(vr[0])):
            v_r += vr[i][ii]
        Vr[i] = v_r
    Vxr = Vr[0]
    Vyr = Vr[1]
    Vzr = Vr[2]

    return M,c, Vxr,Vyr,Vzr

## Roda e armazena o model odo robô para M testes.
matriz_resultados = []
for i in tqdm(range(int(M)),desc="Processing Monte Carlo Method: "):
    resultados = Robot_Model(v)
    matriz_resultados.append(resultados)

# Salva os dados em um data frame
df = pd.DataFrame(np.array(matriz_resultados), columns = ['M','c', 'Ixr', 'Iyr' , 'Izr'])
df.to_csv('Resultados.csv')

# Mostra os Resultados
fig, ax = plt.subplots(1,4,tight_layout=True)

ax[0].hist(df['M'],bins=bars)
ax[0].set_title('Massa')
ax[1].hist(df['c'],bins=bars)
ax[1].set_title('c')
'''ax[1].hist(df['L'],bins=bars)
ax[1].set_title('L')
ax[2].hist(df['H'],bins=bars)
ax[2].set_title('H')
ax[3].hist(df['W'],bins=bars)
ax[3].set_title('W')'''



fig2, ax2 = plt.subplots(1,3,tight_layout=True)

ax2[0].hist(df['Ixr'],bins=bars)
ax2[0].set_title('Ixr')

ax2[1].hist(df['Iyr'],bins=bars)
ax2[1].set_title('Iyr')

ax2[2].hist(df['Izr'],bins=bars)
ax2[2].set_title('Izr')

plt.show()