import pandas as pd

datos = pd.read_excel("datos_pacientes.xlsx")

#eliminar columna
#datos= datos.drop(columns=['Nivel_Glucosa'])

while True:
    print('Menu de procesamiento')
    print('1. Mostrar datos')
    print('2. Eliminar datos nulos')
    print('3. Eliminar datos duplicados')
    print('4. Estimar tiempos de atención')
    print('5. Contar personas por enfermedad')
    print('6. Generar archivo excel con datos procesados')
    print('7. Generar archivo json con datos procesados')
    print('8. Generar archivo csv con datos procesados')
    print('9. Generar archivo xml con datos procesados')
    print("10. Salir")
   
    opcion= int(input("Seleccione la opcion deseada"))

    if opcion ==1:
      print(datos)
      print("Datos estadisticos")
      print(datos.describe())
    elif opcion ==2:
      datos.dropna()
    elif opcion ==3:
      datos.drop_duplicates()
    elif opcion ==4:
      #Crear una columna para describir cuanto fue el tiempo que demoraron para atender una persona
     datos['demora_atencion'] = datos['Fecha_Hora_Atencion'] - datos['Fecha_Hora_Consulta']
    elif opcion ==5:
     datosAgrupados = datos.groupby("Enfermedad")['Sexo'].agg('count')
     print(datosAgrupados)
    elif opcion ==6:
     datos.to_excel("ProcesamientoPacientes1.xlsx")
    elif opcion ==7:
     datos.to_json("ProcesamientoPacientes1.json")
    elif opcion ==8:
     datos.to_csv("ProcesamientoPacientes1.csv")
    elif opcion ==9:
      datos.to_xml("ProcesamientoPacientes1.xml")
    elif opcion ==10:
      break
    else:
      print("Elija un opcion Correcta")