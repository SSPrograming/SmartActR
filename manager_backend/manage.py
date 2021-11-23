from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import query_yaml
from application import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = query_yaml('db.MYSQL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
