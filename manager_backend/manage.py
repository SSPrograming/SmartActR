from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import query_yaml
from application import db
from application.api import bp
from verify_identity import verify_identity
from threading import Timer
#from application.utils.autoupdate import start_timer
from application.service import ReserveService

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

def start_timer():
    interval = query_yaml('app.INTERVAL')
    t = Timer(interval, auto_update)
    t.start()

def auto_update():
    interval = query_yaml('app.INTERVAL')
    with app.app_context():
        ReserveService.update_all_record_status()
    t = Timer(interval, auto_update)
    t.start()

start_timer()

if __name__ == '__main__':
    manager.run()
