import drivers as sql
import app_config

class Controller:
    def __init__(self, driver):
        self.driver = driver

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def find(self):
        pass

class ProjectController(Controller):
    tablename = 'project'
    def __init__(self, driver):
        super().__init__(driver)

    def columns(self):
        return self.driver.column_names(self.tablename)

    def insert(self, values):
        # we do not count the id column. Usually we only pass the rest because it is autoincremented
        assert len(values) == len(self.columns()) - 1, 'Wrong number of values'
        self.driver.insert(self.tablename, values)


class PersonnelController(Controller):
    tablename = 'personnel'
    def __init__(self, driver):
        super().__init__(driver)

    def load_all(self):
        self.driver._execute_command(f'select * from {self.tablename}')
        return self.driver.cursor.fetchall()

def project_controller(dbname):
    driver= sql.SqliteDriver(dbname)
    return ProjectController(driver)

def personnel_controller(dbname):
    driver= sql.SqliteDriver(dbname)
    return PersonnelController(driver)


if __name__ == '__main__':
    ctrl = project_controller(app_config.DB_MOH)
    project = ('Some title', 'some code', 'some start date', 'some duration', 'contractor', 'subcontractor', 'it is in progress')
