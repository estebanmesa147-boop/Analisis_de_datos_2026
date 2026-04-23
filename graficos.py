import matplotlib.pyplot as plt
import pandas as pd

personas= pd.read_excel("pers.xlsx")


nombres = ["Andrés","Luisa","Diego","Lucia"]
edades = [21,34,26,19]
colors= ["yellow","blue","red","green" ]

genero= ["F", "M"]
cantidad=[23,37]

cantidadMujeres= personas[personas["Genero"]=="F"].shape[0]
CantidadHombres= personas[personas["Genero"]=="M"].shape[0]
cantidadExcel=[cantidadMujeres, CantidadHombres]
print(cantidadMujeres)
plt.bar(personas["Nombre"], personas["Edad"], color=colors)
plt.title("Edad por Persona")
plt.xlabel("Nombres")
plt.xticks(rotation=90)
plt.ylabel("Edades")
plt.show()

#grafico de barras
plt.bar(nombres,edades,color=colors)
plt.title("Edad por Persona")
plt.xlabel("Nombres")
plt.ylabel("Edades")
plt.show()

#grafico de linea
plt.plot(nombres,edades,marker="x")
plt.title("Edad por Persona")
plt.xlabel("Nombres")
plt.ylabel("Edades")
plt.show()

#grafico de 
plt.scatter(nombres,edades)
plt.title("edad por persona")
plt.xlabel("nombres")
plt.ylabel("edades")
plt.show()

plt.pie(cantidad,labels=genero,startangle=90)
plt.title("Cantidad de Personas por genero")
plt.axis("equal")
plt.show()