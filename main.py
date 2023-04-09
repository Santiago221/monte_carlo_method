import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy  as np
from tqdm import tqdm

x1_min = 1
x1_max = 2

x2_min = 3
x2_max = 4

x3_avg = 3
x3_sigma = 0.55

p = 0.9545
M = 1e7

def func(x1,x2,x3):
    return ((x1 + x2)**(x3/x1))*np.sin(x2)

x1_vet = np.zeros(int(M))
x2_vet = np.zeros(int(M))
x3_vet = np.zeros(int(M))
y_vet = np.zeros(int(M))


for i in tqdm(range(int(M)),desc="Processing Monte Carlo Method: "):
    x1 = random.uniform(x1_min, x1_max)
    x1_vet[i] = x1
    x2 = random.triangular(x2_min, x2_max)
    x2_vet[i] = x2
    x3 = random.gauss(x3_avg, x3_sigma)
    x3_vet[i] = x3
    y_vet[i] = func(x1,x2,x3)

matrix = [x1_vet,x2_vet,x3_vet,y_vet]

df = pd.DataFrame(np.array(matrix).T, columns = ['x1','x2','x3','y'])



fig, ax = plt.subplots(1,4,tight_layout=True)

ax[0].hist(df['x1'], range=[x1_min,x1_max],bins=1000)
ax[1].hist(df['x2'], range=[x2_min,x2_max],bins=1000)
ax[2].hist(df['x3'], range=[x3_avg -2*x3_sigma,x3_avg + 2*x3_sigma],bins=1000)

ax[3].hist(df['y'], range=[df['y'].mean()-2*df['y'].std(),df['y'].mean()+2*df['y'].std()],bins=1000)

plt.show()

