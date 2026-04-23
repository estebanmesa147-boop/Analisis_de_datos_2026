import pandas as pd
from flask import Flask, request, jsonify

app= Flask(__name__)

datos= pd.read_excel("personas_colombia.xlsx")

#Preprocesamiento

datos= datos.dropna()
datos= datos.drop_duplicates()

@app.route("/listaPersonasColombia",methods=['GET'])
def listar():
    return jsonify(datos.to_dict(orient='records'))

@app.route("/EstadisticasPersonasColombia",methods=['GET'])
def estadisticas():
    mediaEdad = datos['Edad'].mean()
    desviacionEdad = datos['Edad'].std()
    return jsonify({
        "Media": mediaEdad,
        "Desviación": desviacionEdad,
        "Moda": float(datos['Edad'].mode()[0])
})

@app.route("/datosAgrupados", methods=['GET'])
def agrupacion():
     tablaNueva = datos.groupby('Género')['Edad'].agg(['mean','std','count']).reset_index()
     return jsonify(tablaNueva.to_dict(orient='records'))
if __name__ == '__main__':
    app.run(debug=True)






