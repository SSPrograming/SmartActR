from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import query_yaml
from application import db
from application.api import bp
from verify_identity import verify_identity
from threading import Timer
from application.utils import now
from application.service import ReserveService, UserService, AdminService
from timetasks import FileLock
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = query_yaml('db.MYSQL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)
app.lock = FileLock()

app.before_request(verify_identity)
for bluep in bp:
    app.register_blueprint(bluep)

manager.add_command('db', MigrateCommand)

def start_timer_perminute():
    t = Timer(5, auto_update_perminute)
    t.start()

def start_timer_perday():
    now_datetime = now()
    next_update_time = datetime.datetime(now_datetime.year, now_datetime.month, now_datetime.day+1)
    interval = (next_update_time-now_datetime).total_seconds()
    t = Timer(interval,auto_update_daily)
    t.start()


def auto_update_perminute():
    interval = query_yaml('app.INTERVAL')
    with app.app_context():
        ReserveService.update_all_record_status()
    t = Timer(interval, auto_update_perminute)
    t.start()


def auto_update_daily():
    with app.app_context():
        UserService.daily_update_userStatus()
    t = Timer(86400, auto_update_daily)
    t.start()

start_timer_perminute()

with app.app_context():
    AdminService.create_admin()
if __name__ == '__main__':
    manager.run()
