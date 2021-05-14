import sqlite3
from app_config import DB_COMPANY, DB_PATH
import wx

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


def load_employees():
    employees = []
    conn = sqlite3.connect(DB_PATH + DB_COMPANY)
    cur = conn.cursor()
    query = "select id, first_name, last_name from personnel where active = 'ΕΝΕΡΓΟΣ'"
    cur.execute(query)
    for _id, first, last in cur.fetchall():
        employees.append(Employee(_id, first, last))
    return employees

def load_subjects():
    subjects = []
    conn = sqlite3.connect(DB_PATH + DB_COMPANY)
    cur = conn.cursor()
    query = "select id, description from education_points"
    cur.execute(query)
    for _id, description in cur.fetchall():
        subjects.append(HSSubject(_id, description))
    return subjects


class TrainingPanel(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, -1)
        self.empl_txt = wx.StaticText(self, label = 'Employee:')
        emps = load_employees()
        self.empl_choice = wx.Choice(self, choices = [str(e) for e in emps])
        print('choice set')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.empl_txt, -1)
        sizer.Add(self.empl_choice, 1)

        self.SetSizer(sizer)
        self.Fit()


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__()
        self.training_panel = TrainingPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame()
        self.frame.Show(True)
        return True

app = MyApp()
print('entering mainloop')

app.MainLoop()
