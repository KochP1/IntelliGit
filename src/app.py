# python -m venv venv
# .\venv\Scripts\Activate.ps1
from flask import Flask
from flask_cors import CORS
from os import getenv

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    # Configurar CORS para Angular
    CORS(app, origins=[getenv('ANGULAR_URL', 'http://localhost:4200')])
    
    #Registrar blueprints
    from routes.chat_routes import chat_bp
    from routes.github_routes import github_bp
    
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(github_bp, url_prefix='/api/github')
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(getenv('FLASK_PORT', 5000))
    app.run(debug=True, port=port)