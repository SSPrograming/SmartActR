from threading import Timer
from application.service import ReserveService

def start_timer():
    t = Timer(3, auto_update)
    t.start()

def auto_update():
    ReserveService.update_all_record_status()
