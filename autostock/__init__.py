from flask import Flask



app = Flask(__name__)


from autostock.main.routes import main
app.register_blueprint(main)

from autostock.users.routes import users
app.register_blueprint(users)

from autostock.inventory.routes import inventory
app.register_blueprint(inventory)