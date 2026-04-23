import matplotlib.pyplot as plt
import pandas as pd

ventas= pd.read_excel("proventas_autos.xlsx")

colors= ["yellow","blue","red","green" ]

#grafico de barras
plt.bar(ventas["Modelo"],ventas["Ventas 2025"],color=colors)
plt.title("Ventas por Modelo")
plt.xlabel("Modelo")
plt.ylabel("Ventas")
plt.show()
