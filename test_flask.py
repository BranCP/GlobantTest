from flask import Flask, request, jsonify
import boto3
import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from config import DB_CONFIG
from config import AWS_CONFIG


app = Flask(__name__)

# Constantes S3
session = boto3.Session( aws_access_key_id=AWS_CONFIG['aws_access_key_id'], 
                         aws_secret_access_key=AWS_CONFIG['aws_secret_access_key'])
s3 = session.resource('s3')
bucket_name = 'bcerontestgbnt'
# Constantes Postgre
DB_HOST = DB_CONFIG['DB_HOST']
DB_PORT = DB_CONFIG['DB_PORT']
DB_NAME = DB_CONFIG['DB_NAME']
DB_USER = DB_CONFIG['DB_USER']
DB_PASSWORD = DB_CONFIG['DB_PASSWORD']
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


def get_columnnames(table):
    inspector = inspect(engine)
    columns = inspector.get_columns(table)
    column_names = [column['name'] for column in columns]
    return column_names

@app.route('/upload_data', methods=['POST'])
def upload_data():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_download_directory = os.path.join(script_directory, '.', 'data_download')
    

    try:
        data = request.get_json()
        mensaje = data.get("mensaje", "Mensaje no proporcionado")
        file = data.get("file", "Nombre archivo no proporcionado")
        table = data.get("table", "Tabla no proporcionado")
        csv_path = os.path.join(data_download_directory, file)
        print(f"{mensaje}")
        
        # Descarga S3
        try:
            s3.Bucket(bucket_name).download_file(f'data/{file}', csv_path)
            print(f'Archivo descargado correctamente')
        except Exception as e:
            print(f'Error al descargar el archivo: {str(e)}')

        # Carga db
        df = pd.read_csv(csv_path, header=None, names=get_columnnames(table))
        try: 
            df.to_sql(table, engine, if_exists="replace", index=False, method='multi', chunksize=10000)
        except Exception as e:
            print(f'Error al cargar el archivo: {str(e)}')
        engine.dispose()
        os.remove(csv_path)
        return jsonify({"mensaje": 'CSV cargado en la tabla de PostgreSQL.'})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)