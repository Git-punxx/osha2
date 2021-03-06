import domain
import sys

class Controller:
    def __init__(self):
        self.conn = domain.connect()

    def fetch_all(self):
        return self.loader.load_all()

    def fetch(self, id):
        return self.loader.load(id)

    def columns(self):
        return self.loader.columns()

class ProjectController(Controller):
    def __init__(self):
        super().__init__()
        self.loader = domain.TableLoader(self.conn, 'project')


    def add_project(self, title, code, start_date, timetable, contractor, subcontractor, in_progress):
        cursor = self.loader.cursor
        print(f'Inserting project {title} {code} in db')
        row_id = cursor.execute('insert into project (title, code, start_date, timetable, contractor, subcontractor,'
                                ' in_progress) values (?, ?, ?, ?, ?, ?, ?)', (title, code, start_date, timetable, contractor, subcontractor, in_progress))
        cursor.connection.commit()
        return row_id

    def load_contractors(self):
        cursor = self.loader.cursor
        return [row for row in cursor.execute("select * from company")]

    def remove_project(self, project_id):
        cursor = self.loader.cursor
        row_id = cursor.execute('remove * from project where project.id = ?', (project_id, ))
        cursor.connection.commit()


class PetepController(Controller):
    def __init__(self):
        super().__init__()
        self.loader = domain.TableLoader(self.conn, 'petep')

    def add_measure(self, petep_id, measure_id):
        cursor = self.loader.cursor
        row_id = cursor.execute('insert into petep_analysis (petep_id, measure_id) values (? , ?)', (petep_id, measure_id))
        cursor.connection.commit()
        print(f'Inserted data {petep_id} and {measure_id} at {row_id}')
        sys.stdout.flush()
        return row_id


    def remove_measure(self, petep_id, measure_id):
        cursor = self.loader.cursor
        row_id = cursor.execute('delete from petep_analysis where petep_id = ? and measure_id = ?', (item_id, petep_id))
        cursor.connection.commit()
        print(f'Deleted data {measure_id} and {petep_id} at {row_id}')
        sys.stdout.flush()
        return row_id

    def fetch_measure_list(self, item_id):
        cursor = self.loader.cursor
        rows = cursor.execute(f'select measure.id, measure.subsector_id, measure.description from measure')
        data = rows.fetchall()
        return data

class ItemController(Controller):
    def __init__(self):
        super().__init__()
        self.loader = domain.TableLoader(self.conn, 'moh_items')

    def add_petep(self, item_id, petep_id):
        cursor = self.loader.cursor
        row_id = cursor.execute('insert into item_analysis (item_id, petep_id) values (? , ?)', (item_id, petep_id))
        cursor.connection.commit()
        print(f'Inserted data {item_id} and {petep_id} at {row_id}')
        sys.stdout.flush()
        return row_id

    def remove_petep(self, item_id, petep_id):
        cursor = self.loader.cursor
        row_id = cursor.execute('delete from item_analysis where item_id = ? and petep_id = ?', (item_id, petep_id))
        cursor.connection.commit()
        print(f'Deleted data {item_id} and {petep_id} at {row_id}')
        sys.stdout.flush()
        return row_id

    def fetch_petep_list(self, item_id):
        cursor = self.loader.cursor
        rows = cursor.execute(f'select petep.id, petep.code, petep.title from petep left join item_analysis where petep.id = item_analysis.petep_id and item_analysis.item_id = {item_id} ')
        data =  rows.fetchall()
        return data


class MeasureController(Controller):
    def __init__(self):
        super().__init__()
        self.loader = domain.TableLoader(self.conn, 'measure')
