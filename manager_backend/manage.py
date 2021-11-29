from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import query_yaml
from application import db
from application.api import bp
from verify_identity import verify_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = query_yaml('db.MYSQL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)

app.before_request(verify_identity)
for bluep in bp:
    app.register_blueprint(bluep)

manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()
