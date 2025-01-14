from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from models import db
from app import app,Actor,Movie,Cast

#db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()