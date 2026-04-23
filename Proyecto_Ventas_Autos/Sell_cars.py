import pandas as pd

Sell_Cars = pd.DataFrame()

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
        Sell_Cars = pd.read_excel("proventas_autos.xlsx")
        print("Archivo cargado correctamente")

    elif opcion == 2:
        print(Sell_Cars)
        print(Sell_Cars.isnull())
        print(Sell_Cars.isnull().sum())
        print(Sell_Cars.duplicated())
        
    elif opcion == 3:
        Sell_Cars = Sell_Cars.dropna()
        print("Datos nulos eliminados")

    elif opcion == 4:
        Sell_Cars = Sell_Cars.drop_duplicates()
        print("Datos duplicados eliminados")
    elif opcion == 5:
        Sell_Cars['Columna Nueva'] = Sell_Cars ['Ventas 2025'] *0.3
    elif opcion == 6:
        Sell_Cars.to_excel('ArchivoProcesadoCars.xlsx')
    elif opcion == 7:
        break

    else:
        print("Ingrese una Opción Válida")
