import os

from flask import Flask
from config import Config
from models import db
from routes import main

app = Flask(__name__)
app.config.from_object(Config)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# Inicializa banco de dados
db.init_app(app)

# Registra rotas
app.register_blueprint(main)

# Cria banco automaticamente
with app.app_context():
    db.create_all()

# Inicialização
if __name__ == "__main__":
    app.run(debug=True)