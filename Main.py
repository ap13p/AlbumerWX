#!/usr/bin/env python2

import wx
import db
from AddDataFrame import AddDataFrame


class MainFrame(wx.Frame):
    def __setup_menubar(self):
        self.menubar = wx.MenuBar()
        self.menu_file = wx.Menu()
        self.menu_file_add = self.menu_file.Append(wx.ID_ANY, "Add")
        self.menu_file_rollback = self.menu_file.Append(wx.ID_ANY, "Rollback")
        self.menu_file_commit = self.menu_file.Append(wx.ID_ANY, "Commit")
        self.menu_file.AppendSeparator()
        self.menu_file_exit = self.menu_file.Append(wx.ID_ANY, "Exit")

        self.menubar.Append(self.menu_file, "File")
        self.SetMenuBar(self.menubar)

    def __setup_toolbar(self):
        self.toolbar = wx.ToolBar(self, style=wx.TB_HORZ_TEXT)

        tsize = (24,24)
        add_bmp =  wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR, tsize)
        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)

        self.toolbar.SetToolBitmapSize(tsize)
        self.tool_add = self.toolbar.AddLabelTool(10, "Add", add_bmp,
            shortHelp="Add", longHelp="Add new liric")
        self.tool_save = self.toolbar.AddLabelTool(20, "Save", save_bmp,
            shortHelp="Save", longHelp="Save change to database")

        self.SetToolBar(self.toolbar)

        # --------- Event
        self.Bind(wx.EVT_TOOL, self.__on_tool_add_clicked, self.tool_add)
        self.Bind(wx.EVT_TOOL, self.__on_tool_save_clicked, self.tool_save)
        # --------- End Event


    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)

        self.__setup_menubar()
        self.__setup_toolbar()
        self.__init_table()

        self.CenterOnScreen()
        self.SetSize((600,400))

        self.main_box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_box)
        self.main_panel = wx.Panel(self)
        self.main_box.Add(self.main_panel, 2, wx.EXPAND|wx.ALL, 2)

        self.main_panel.SetSizer(wx.BoxSizer(wx.VERTICAL))

        self.splitter = wx.SplitterWindow(self.main_panel, style=wx.SP_LIVE_UPDATE)
        self.main_panel.GetSizer().Add(self.splitter, 3, wx.EXPAND|wx.ALL, 2)

        self.vbox_kiri = wx.BoxSizer(wx.VERTICAL)
        self.panel_kiri = wx.Panel(self.splitter, style=wx.BORDER_SUNKEN)
        self.panel_kiri.SetSizer(self.vbox_kiri)

        self.vbox_kanan = wx.BoxSizer(wx.VERTICAL)
        self.panel_kanan = wx.Panel(self.splitter, style=wx.BORDER_SUNKEN)
        self.panel_kanan.SetSizer(self.vbox_kanan)

        self.splitter.SetMinimumPaneSize(200)
        self.splitter.SplitVertically(self.panel_kiri, self.panel_kanan, -100)


        _list_data = [list(hasil) for hasil in db.get_all_data()]
        list_data = []
        for i in _list_data:
            list_data.append(str(i[0] + ' - ' + i[1]))

        self.list_judul = wx.ListBox(self.panel_kiri,
                                     choices=list_data,
                                     style=wx.LB_SINGLE|wx.LB_NEEDED_SB|wx.LB_SORT)
        self.vbox_kiri.Add(self.list_judul, 2, wx.EXPAND|wx.ALL, 2)

        self.lirik_viewer = wx.TextCtrl(self.panel_kanan, style=wx.TE_MULTILINE)
        self.vbox_kanan.Add(self.lirik_viewer, 2, wx.EXPAND|wx.ALL, 2)

        self.main_box.Layout()


        # ----------------- Event
        self.Bind(wx.EVT_LISTBOX, self.__list_judul_clicked, self.list_judul)
        self.Bind(wx.EVT_MENU, self.__on_add, self.menu_file_add)
        self.Bind(wx.EVT_MENU, self.__on_rollback, self.menu_file_rollback)
        self.Bind(wx.EVT_MENU, self.__on_commit, self.menu_file_commit)
        self.Bind(wx.EVT_MENU, self.__on_exit, self.menu_file_exit)
        # ----------------- End Event

    def __init_table(self):
        db.connect()
        db.init_table()

    def __set_title(self, title):
        self.SetTitle(title + ' | Albumer')

    def __list_judul_clicked(self, evt):
        self.__set_title(str(evt.GetEventObject().GetStringSelection()))
        for i in db.get_data(evt.GetEventObject().GetStringSelection().split(' - ')[1]):
            self.lirik_viewer.ChangeValue(i[2])

    def __on_tool_add_clicked(self, evt):
        self.__on_add(None)

    def __on_tool_save_clicked(self, evt):
        db.update('lirik',
            self.lirik_viewer.GetValue(),
            self.list_judul.GetStringSelection()
        )

    def __on_add(self, evt):
        add_data_frame = AddDataFrame(self)
        if add_data_frame.ShowModal() == wx.ID_OK:
            data = add_data_frame.GetData()
            db.add_data(data[0], data[1], data[2])
            self.list_judul.Insert(str(data[0] + ' - ' + data[1]), 0)
            self.list_judul.Refresh()
            self.list_judul.SetStringSelection(str(data[0] + ' - ' + data[1]), True)
            db.commit()
        add_data_frame.Destroy()

    def __on_rollback(self, evt):
        db.rollback()

    def __on_commit(self, evt):
        db.commit()

    def __on_exit(self, evt):
        self.Close()
        db.close_all()


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(parent=None, title="Albumer")
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
