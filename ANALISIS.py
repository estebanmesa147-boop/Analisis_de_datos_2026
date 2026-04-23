import pandas as pd 
notas = pd.read_excel("notas_estudiantes.xlsx")
#notas = pd.read_csv("https://docs.google.com/spreadsheets/d/17IWeHXCjm6B9BKoQW-uJCSNEafNZs-df/export?format=csv")
#https://docs.google.com/spreadsheets/d/17IWeHXCjm6B9BKoQW-uJCSNEafNZs-df/edit?gid=1180726054#gid=1180726054
cols = ["Matematicas", "Biologia", "Sociales", "Lenguaje", "Artes"]
for c in cols:
    notas[c] = notas[c].astype(str).str.replace(",", ".").astype(float)
print(notas)
print(notas.describe())
print("promedio de matemáticas:",notas["Matematicas"].mean())
print((notas["Genero"] == "F").sum()) 
print
