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

class PetepController(Controller):
    def __init__(self):
        super().__init__()
        self.loader = domain.TableLoader(self.conn, 'petep')

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



