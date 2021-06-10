from flask import Flask
from flask_migrate import Migrate
#from flask_cors import CORScors = CORS()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object(config)

    with app.app_context():
        #cors.init_app(app)

        from .auth import auth
        auth.init_app(app)

        from .socketio import socketio
        socketio.init_app(app)

        from .models import db
        db.init_app(app)
        migrate.init_app(app, db)

        db.create_all()

    return app