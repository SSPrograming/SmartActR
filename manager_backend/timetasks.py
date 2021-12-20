import os
import fcntl

class FileLock():
    def __init__(self):
        lock_dir = '/tmp'
        lock_file = 'FLASK_LOCK'
        self.file = '%s%s%s' % (lock_dir, os.sep, lock_file)
        if not os.path.exists(self.file):
            n_file = open(self.file, 'w+')
            n_file.close()
        self._fn = None
        self.release()
    
    def acquire(self):
        self._fn = open(self.file, 'w')
        fcntl.flock(self._fn.fileno(), fcntl.LOCK_EX)
        self._fn.write('1')
    
    def release(self):
        if self._fn:
            try:
                self._fn.close()
            except:
                pass