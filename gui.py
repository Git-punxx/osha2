import wx
import app_config
import controller as ctrl
import sys

class ProjectInput(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = ctrl.ProjectController()

        self.title_lbl = wx.StaticText(self, -1, 'Title:')
        self.code_lbl = wx.StaticText(self, -1, 'Code:')
        self.start_date_lbl = wx.StaticText(self, -1, 'Starting date:')
        self.timetable_lbl = wx.StaticText(self, -1, 'Duration')

        self.title_txt = wx.TextCtrl(self, -1, '', style = wx.TE_MULTILINE)
        self.code_txt = wx.TextCtrl(self, -1, '')
        self.start_date_txt = wx.TextCtrl(self, -1, '')
        self.timetable_txt = wx.TextCtrl(self, -1, '')

        self.ok = wx.Button(self, wx.ID_OK, "Save...")
        self.cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        msizer = wx.GridBagSizer(hgap = 10, vgap = 10)
        msizer.Add(self.title_txt, pos = (0, 1), span = (1, 20), border = 5, flag = wx.EXPAND)
        msizer.Add(self.code_txt, pos = (1, 1), span = (1, 20), border = 5,flag = wx.EXPAND)
        msizer.Add(self.start_date_txt, pos = (2, 1), span = (1, 20), border = 5,flag = wx.EXPAND)
        msizer.Add(self.timetable_txt, pos = (3, 1), span = (1, 20), border = 5,flag = wx.EXPAND)


        msizer.Add(self.title_lbl, pos = (0, 0), border = 5)
        msizer.Add(self.code_lbl, pos = (1, 0), border = 5)
        msizer.Add(self.start_date_lbl, pos = (2, 0), border = 5)
        msizer.Add(self.timetable_lbl, pos = (3, 0), border = 5)

        msizer.Add(self.ok, pos = (4, 0))
        msizer.Add(self.cancel, pos = (4, 1))

        self.Bind(wx.EVT_BUTTON, self.OnOk, self.ok)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel)

        self.SetSizer(msizer)
        self.Fit()

    def GetData(self):
        data = [b.GetValue() for b in [self.title_txt, self.code_txt, self.start_date_txt, self.timetable_txt]]
        return data

    def OnOk(self, event):
        data = self.GetData()
        if data is None:
            return
        self.controller.add_project(*data)
        self.Destroy()

    def OnCancel(self, event):
        self.Destroy()


class ItemDetails(wx.Dialog):
    def __init__(self, parent, item_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.item_id = item_id
        self.controller = ctrl.ItemController()
        data = self.controller.fetch_petep_list(self.item_id)

        self.petep_list = PetepListCtrl(self)
        self.petep_list.DeleteAllItems()
        self.petep_list.PopulateList(data)

        descr = self.controller.fetch(item_id)[2]
        cols = self.controller.columns()
        for index, title in enumerate(cols):
            self.petep_list.InsertColumn(index, title)

        self.descr = wx.TextCtrl(self, -1, descr, style = wx.TE_MULTILINE)


        self.add = wx.Button(self, -1, 'Add')
        self.remove = wx.Button(self, -1, 'Remove')

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        lsizer = wx.BoxSizer(wx.VERTICAL)
        rsizer = wx.BoxSizer(wx.VERTICAL)

        lsizer.Add(self.descr, 1, wx.EXPAND)
        lsizer.Add(self.petep_list, 2, wx.EXPAND)

        rsizer.Add(self.add)
        rsizer.Add(self.remove)

        sizer.Add(lsizer, 1, wx.EXPAND)
        sizer.Add(rsizer, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()
        self.SetSize((900, 600))

        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.add)
        self.Bind(wx.EVT_BUTTON, self.OnRemove, self.remove)

    def OnAdd(self, event):
        dlg = ComposeDialog(parent = self)
        res = dlg.ShowModal()
        dlg.Destroy()

    def OnRemove(self, event):
        index= self.petep_list.GetFirstSelected()
        petep_id = self.petep_list.GetItem(index).GetText()
        self.petep_list.DeleteItem(index)
        self.controller.remove_petep(self.item_id, petep_id)
        self.petep_list.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def Append(self, data):
        petep_id = data[0]
        self.petep_list.Append(data)
        self.controller.add_petep(self.item_id, petep_id)

class ItemListCtrl(wx.ListCtrl):
    def __init__(self, parent):
        super().__init__(parent, style = wx.LC_REPORT)
        self.controller = ctrl.ItemController()
        self._setup()

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivate)


    def _setup(self):
        data = self.controller.fetch_all()
        cols = self.controller.columns()
        for index, title in enumerate(cols):
            self.InsertColumn(index, title)
        self.PopulateList(data)
        for index in range(len(cols)):
            self.SetColumnWidth(index, wx.LIST_AUTOSIZE)


    def PopulateList(self, data):
        for row in data:
            self.Append(row)

    def OnActivate(self, event):
        item = event.GetItem()
        item_id = int(item.GetText())
        compositor = ItemDetails(parent = self, item_id = item_id)
        res = compositor.ShowModal()
        if res == wx.ID_OK:
            print(f'received {item_id}')
            sys.stdout.flush()
        else:
            print('Cancel')
        compositor.Destroy()

class PetepListCtrl(wx.ListCtrl):
    def __init__(self, parent):
        super().__init__(parent, style = wx.LC_REPORT)
        self.controller = ctrl.PetepController()
        self._setup()

    def _setup(self):
        data = self.controller.fetch_all()
        cols = self.controller.columns()
        for index, title in enumerate(cols):
            print(title)
            sys.stdout.flush()
            self.InsertColumn(index, title)
        self.PopulateList(data)
        for index in range(len(cols)):
            self.SetColumnWidth(index, wx.LIST_AUTOSIZE)

    def PopulateList(self, data):
        for row in data:
            if row is not None:
                self.Append(row)

class ComposeDialog(wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.list = PetepListCtrl(self)
        self.ok = wx.Button(self, wx.ID_OK, "OK")
        self.cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivate)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list, 1, wx.EXPAND)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.ok, 1)
        hsizer.Add(self.cancel, 1)

        sizer.Add(hsizer, 0)
        self.SetSizer(sizer)
        self.SetSize((800, 400))

    def OnActivate(self, event):
        res = int(event.GetItem().GetText())
        petep = self.list.controller.fetch(res)
        parent = self.GetParent()
        parent.Append(petep)

class ItemPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.item_list = ItemListCtrl(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.item_list, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
        self.SetSize((900, 450))

class MainMenu(wx.MenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self._create_menus()

    def _create_menus(self):
        file_menu = wx.Menu()
        file_menu.Append(-1, 'Open')
        project_menu = wx.Menu()

        projects = wx.MenuItem(project_menu, -1, 'New Project')
        project_menu.Append(projects)

        item_menu = wx.Menu()
        item_choice = wx.MenuItem(item_menu, -1, 'Manage Item List')
        item_menu.Append(item_choice)


        self.Append(item_menu, 'Items')
        self.Append(project_menu, 'Manage Projects')

        self.Bind(wx.EVT_MENU, self.OnNewProject, projects)
        self.Bind(wx.EVT_MENU, self.OnItem, item_choice)

    def OnNewProject(self, event):
        dlg = ProjectInput(self)
        res = dlg.ShowModal()
        dlg.Destroy()

    def OnItem(self, event):
        dlg = ComposeDialog(self)
        res = dlg.ShowModal()
        dlg.Destroy()

    def OnFile(self, event):
        print('File choice')
        sys.stdout.flush()

class MainFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.panel = ItemPanel(self)

        self.menu = MainMenu()
        self.SetMenuBar(self.menu)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
        self.SetSize((1000, 500))

class OshaApp(wx.App):
    def OnInit(self):
        frame = MainFrame(parent = None)
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == '__main__':
    app = OshaApp()
    app.MainLoop()
