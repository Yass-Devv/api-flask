import os
from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/crea')
def test_mysql():
    # On récupère le mot de passe depuis la variable d'environnement 'DB_PASSWORD'
    db_password = os.environ.get('DB_PASSWORD')
    
    if not db_password:
        return "Erreur : La variable d'environnement DB_PASSWORD n'est pas définie.", 500

    try:
        # Connexion à la base de données MySQL
        # 'host.docker.internal' permet au conteneur de l'API de parler au conteneur MySQL de ton PC
        connection = pymysql.connect(
            host='host.docker.internal',
            user='root',
            password=db_password,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # On exécute une requête simple pour demander la version de MySQL
            cursor.execute("SELECT VERSION() AS version;")
            result = cursor.fetchone()
            
        connection.close()
        return f"Connexion réussie ! Version de MySQL récupérée : {result['version']}"

    except Exception as e:
        return f"Échec de la connexion à MySQL : {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)