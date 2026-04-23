import pandas as pd 


ventas = pd.read_excel("proventas_autos.xlsx")
#notas = pd.read_csv("https://docs.google.com/spreadsheets/d/17IWeHXCjm6B9BKoQW-uJCSNEafNZs-df/export?format=csv")

#cols = ["Matematicas", "Biologia", "Sociales", "Lenguaje", "Artes"]

#for c in cols:
   # notas[c] = notas[c].astype(str).str.replace(",", ".").astype(float)

print(ventas)

print(ventas.describe())


print("promedio de Ventas 2025:",ventas["Ventas 2025"].mean())