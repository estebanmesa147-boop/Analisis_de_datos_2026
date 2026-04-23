import mysql.connector
from flask import Flask, request, jsonify

app= Flask(__name__)

db= mysql.connector.connect(
    host="localhost",
    user= "root",
    password="Mysql2026!",
    database="analisis2026"
)
cursor=db.cursor(dictionary=True)

query="select * from estudiante"
cursor.execute(query)
resultados= cursor.fetchall()
print(resultados)

consulta2="select * from estudiante where edad >30"

cursor.execute(consulta2)
resultados2= cursor.fetchall()
print(resultados2)

@app.route("/datosEstudiantes", methods=['GET'])
def datos():
   return jsonify(resultados)

if __name__=='__main__':
  app.run(debug=True)