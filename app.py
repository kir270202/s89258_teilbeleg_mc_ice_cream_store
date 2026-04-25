"""Application entry point for the ice cream shop simulation web app."""

from flask import Flask

from routes import ui


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(ui)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
