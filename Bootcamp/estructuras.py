import pandas as pd 
DatosExcel= pd.read_excel("notas_estudiantes.xlsx") 

print("Promedio Biologia")
print(DatosExcel["Biologia"].mean())
semana=['Lunes', 'Martes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
print(semana[0])
print(semana[0:3])

for dia in semana:
    print(dia)

notasEstudiantes=[3.2,4,2,1.8,2.7]
sumatoria=0

for nota in notasEstudiantes:
    ponderado=nota*0.2
    print (ponderado)
    sumatoria= sumatoria + ponderado

print (sumatoria)

personas= {
    "Nombre": [" Jorge", "Ana", "567"],
    "Identificacion": ["1057", "234", "567"],
    "Edad":[31, 28,25]
}

datospersona= pd.DataFrame(personas)
print(datospersona)
print("Promedio Edad:")
print (datospersona["Edad"].mean())
print (datospersona.keys())
print(datospersona.dtypes)