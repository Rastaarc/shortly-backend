from run import app
from api.models import db
from flask_migrate import MigrateCommand
from flask_script import Manager

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
