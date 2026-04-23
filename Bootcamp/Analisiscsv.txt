import pandas as pd 


#notas = pd.read_excel("notas_estudiantes.xlsx")
notas = pd.read_csv("https://docs.google.com/spreadsheets/d/17IWeHXCjm6B9BKoQW-uJCSNEafNZs-df/export?format=csv")
print(notas)

print(notas.describe())

print("promedio de matematicas:",notas["matematicas"].mean())