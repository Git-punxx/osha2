import sqlite3
import app_config

connection = None
mapper_registry = {}

def get_mapper(cls):
    global mapper_registry
    return mapper_registry[cls.__name__]

def assign_mapper(mapper):
    def deco(func):
        global mapper_registry
        mapper_registry[mapper] = func 
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return deco


class ItemCompositor:
    def __init__(self, item_id):
        self.petep_list = []

    def add(self, petep_id):
        self.petep_list.append(petep_id)

    def remove(self, petep_id):
        self.petep_list.remove(petep_id)


class Composite:
    def __init__(self):
        self.children = []
    
    def get_children(self):
        return iter(self.children)
    
    def load(self):
        raise NotImplementedError

class HazardType(Composite):
    def __init__(self):
        super().__init__()
    
    @assign_mapper('HazardType')
    def load(self):
        mapper = get_mapper(self.__class__)
        self.children.extend(mapper.fetch())

class  Loader:
    def __init__(self, connection):
        self.cursor = connection.cursor()

    def load(self, item_id):
        raise NotImplementedError

    def columns(self):
        return tuple([t[0] for t in self.cursor.description])

class TableLoader(Loader):
    def __init__(self, connection, table_name):
        super().__init__(connection)
        self.table_name = table_name

    def load(self, item_id):
        result = self.cursor.execute(f'select * from {self.table_name} where {self.table_name}.id = ?', (item_id, ))
        return result.fetchone()

    def load_all(self):
        result = self.cursor.execute(f'select * from {self.table_name}')
        return result.fetchall()

def connect():
    global connection
    if connection is None:
        connection = sqlite3.connect(app_config.DBNAME)
    return connection


if __name__ == '__main__':
    t = HazardType()
