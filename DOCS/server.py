from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos (El alumno debe completar esto)
DB_CONFIG = {
    'host': 'localhost',
    'database': 'tu_base_datos',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'port': 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/formularios', methods=['POST'])
def crear_formulario():
    try:
        datos = request.get_json()
        if not all(datos.get(field) for field in ['nombre', 'email', 'asunto', 'mensaje']):
            return jsonify({'error': 'Faltan campos obligatorios'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO formularios (nombre, email, asunto, mensaje)
            VALUES (%s, %s, %s, %s)
            RETURNING id, nombre, email, asunto, mensaje, fecha_creacion;
        """, (datos['nombre'], datos['email'], datos['asunto'], datos['mensaje']))
        resultado = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'mensaje': 'Formulario enviado correctamente',
            'id': resultado[0],
            'nombre': resultado[1],
            'email': resultado[2],
            'asunto': resultado[3],
            'mensaje': resultado[4],
            'fecha_creacion': resultado[5].isoformat()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/formularios', methods=['GET'])
def obtener_formularios():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM formularios ORDER BY fecha_creacion DESC;")
        formularios = cur.fetchall()
        cur.close()
        conn.close()
        for f in formularios:
            if isinstance(f['fecha_creacion'], datetime):
                f['fecha_creacion'] = f['fecha_creacion'].isoformat()
        return jsonify(formularios), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
