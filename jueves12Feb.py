import pandas as pd

notasEstudiantes = pd.DataFrame()

while True:
    print("Menú de Opciones")
    print("1. Leer Archivo")
    print("2. Mostrar Datos")
    print("3. Eliminar datos nulos")
    print("4. Eliminar duplicados")
    print("5. Añadir columna")
    print("6. Guardar Archivo Procesado")
    print("7. Salir")


    opcion = int(input("Elige una de las Opciones: "))

    if opcion == 1:
        notasEstudiantes = pd.read_excel("notas_estudiantes.xlsx")
        print("Archivo cargado correctamente")

    elif opcion == 2:
        print(notasEstudiantes)
        print(notasEstudiantes.isnull())
        print(notasEstudiantes.isnull().sum())
        print(notasEstudiantes.duplicated())
        
    elif opcion == 3:
        notasEstudiantes = notasEstudiantes.dropna()
        print("Datos nulos eliminados")

    elif opcion == 4:
        notasEstudiantes = notasEstudiantes.drop_duplicates()
        print("Datos duplicados eliminados")
    elif opcion == 5:
        notasEstudiantes['Columna Nueva'] = notasEstudiantes ['Matematicas'] *0.3
    elif opcion == 6:
        notasEstudiantes.to_excel('ArchivoProcesado.xlsx')
    elif opcion == 7:
        break

    else:
        print("Ingrese una Opción Válida")
