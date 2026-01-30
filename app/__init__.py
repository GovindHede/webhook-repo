from flask import Flask
from .db import init_db
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.secret_key = os.getenv("SECRET_KEY", "dev")

    init_db(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
