import wx
import app_config
import controller as ctrl
import sys

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
        self.Fit()

    def OnActivate(self, event):
        res = int(event.GetItem().GetText())
        petep = self.list.controller.fetch(res)
        parent = self.GetParent()
        parent.Append(petep)

class MainPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.item_list = ItemListCtrl(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.item_list, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()

class MainFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.panel = MainPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()

class OshaApp(wx.App):
    def OnInit(self):
        frame = MainFrame(parent = None)
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == '__main__':
    app = OshaApp()
    app.MainLoop()
