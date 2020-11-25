import sqlite3
from app_config import DB_COMPANY, DB_PATH
from controllers import personnel_controller

class Employee:
    def __init__(self, _id, first, last):
        self._id = _id
        self.first = first
        self.last = last
    def __str__(self):
        return f'{self.first}.{self.last}'

class HSSubject:
    def __init__(self, _id, desc):
        self._id = _id
        self.description = desc
    def __str__(self):
        return f'{self.description}'

p = personnel_controller(DB_COMPANY)

for row in p.load_all():
    print(row)


