
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/empleado/empleados', methods=['GET'])
def obtener_empleados():
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

        query = 'SELECT e.nombre, CASE WHEN g.empleado IS NOT NULL THEN \'Es gestor\' WHEN p.empleado IS NOT NULL THEN \'Es programador\' ELSE \'Otro puesto\' END AS tipo_puesto FROM public."Empleado" e LEFT JOIN public."Gestor" g ON e.id = g.empleado LEFT JOIN public."Programador" p ON e.id = p.empleado;'

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