
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/HolaMundo', methods=['GET'])
def hola_mundo():
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "postgres"

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            options="-c search_path=public"
        )

        cursor = connection.cursor()

        query = 'SELECT * FROM public."Empleado" ORDER BY id ASC LIMIT 100'
        cursor.execute(query)


        columnas = [desc[0] for desc in cursor.description]


        resultados = cursor.fetchall()
        empleados = [dict(zip(columnas, fila)) for fila in resultados]


        cursor.close()
        connection.close()

        return  jsonify(empleados)

    except psycopg2.Error as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)