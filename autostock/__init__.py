from flask import Flask
from autostock.config import Config



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from autostock.main.routes import main
    from autostock.mechanics.routes import mechanics
    from autostock.inventory.routes import inventory
    app.register_blueprint(main)
    app.register_blueprint(mechanics)
    app.register_blueprint(inventory)

    return app