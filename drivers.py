import sqlite3
import app_config

def placeholder(no, sep = '?'):
    return f'({" ,".join(list(no * sep))})'

class Driver:
    def __init__(self, resource):
        self.connection = None
        self.cursor = None
        self.connect(resource)

    def connect(self, resource):
        pass

    def disconnect(self):
        pass

    def database_list(self):
        pass

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

class SqliteDriver(Driver):
    def __init__(self, resource):
        super().__init__(resource)

    def connect(self, resource):
        self.connection = sqlite3.connect(resource)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def version(self):
        self._execute_command('select sqlite_version()', 1)
        return self.cursor

    def _table_info(self, table_name):
        self._execute_command(f'pragma table_info({table_name})')
        return self.cursor

    def database_list(self):
        self._execute_command('pragma database_list')
        return self.cursor

    def column_names(self, table_name):
        columns = [column[1] for column in self._table_info(table_name)]
        return columns

    def insert(self, table, values):
        cur = self._execute_command(f'insert into {table} values {placeholder(len(values))}', values)
        return cur

    def _execute_command(self, command, values = None, rows = None):
        try:
            self.cursor.execute(command, values)
            return self.cursor
        except sqlite3.Error as e:
            print(f'Error {e}')
        self.connection.commit()

if __name__ == '__main__':
    d = SqliteDriver(app_config.DB_MOH)
    d.column_names('project')
