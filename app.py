import os
from dotenv import load_dotenv
from flask import Flask
from routes import bp as routes_bp

# Loads environment variables from .env file (if it exists)
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "")
    # dev only: re-read templates on change instead of caching them
    app.config["TEMPLATES_AUTO_RELOAD"] = os.environ.get("TEMPLATES_AUTO_RELOAD") == "1"
    app.register_blueprint(routes_bp)
    return app


app = create_app()

if __name__ == "__main__":
    app.run()
