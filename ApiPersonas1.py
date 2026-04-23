from flask import Flask,jsonify, request
from Persona import PersonaEstructura
from flask_cors import CORS
app= Flask(__name__)

personas= []
persona1=PersonaEstructura("Jorge",31, "M")
persona2=PersonaEstructura("Ana",24, "F")
persona3=PersonaEstructura("Luis",26, "M")  

personas.append(persona1.to_json()) 
personas.append(persona2.to_json()) 
personas.append(persona3.to_json()) 

@app.route("/listaPersonas",methods=['GET'])
def obtenerInformacion():
 return jsonify(personas)


if __name__=='__main__':
   app.run(debug=True)