import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.linear_model import LinearRegression

fechas= pd.date_range(start='2026-01-01', periods=12,freq='ME')

ventas=[100,120,130,150,170,200,210,190,180,220,250,300]

df= pd.DataFrame({'Fecha': fechas, 'Ventas': ventas})
df.set_index('Fecha', inplace=True)

X= np.array([1,2,3,4,5,6,7,8,9,10,11,12]).reshape(-1,1)
X2= np.array([13,14,15,16,17,18]).reshape(-1,1)
modelo= LinearRegression()
modelo.fit(X,df['Ventas'])
y_predicho= modelo.predict(X)
y2_predicho= modelo.predict(X2)
pendiente= modelo.coef_[0]
intercepto= modelo.intercept_

print(pendiente)
print(intercepto)

print(df)

plt.figure()
plt.plot(df.index, df['Ventas'])
plt.title("Ventas Mensuales 2026")
plt.xlabel("Fecha")
plt.ylabel("Ventas")
plt.show()

df['MediaMovil_3']=df['Ventas'].rolling(window=3).mean()

plt.figure()
plt.plot(df.index, df['Ventas'])
plt.plot(df.index, df['MediaMovil_3'])
plt.title("Ventas con Media Movil (3 meses)")
plt.show()

print("Cuanto Vendere en el mes 18?")

prediccion= (pendiente*18)+intercepto

print("Usted Vendera:",prediccion)

plt.scatter(X2, y2_predicho)
plt.xlabel("Meses a predecir")
plt.ylabel("Ventas Predichas")
plt.title("Proyeccion Primer Semestre 2027")
plt.show()