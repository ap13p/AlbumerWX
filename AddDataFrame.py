#!/usr/bin/env python

import wx
import db


class AddDataFrame(wx.Dialog):
    def __init__(self, *args, **kwargs):
        #kwargs['style'] = wx.FRAME_FLOAT_ON_PARENT
        super(AddDataFrame, self).__init__(*args, **kwargs)
        
        self.SetSizer(wx.GridBagSizer())
        
        self.label_artis = wx.StaticText(self, label="Artis / Band : ")
        self.label_judul = wx.StaticText(self, label="Judul lagu : ")
        self.label_lirik = wx.StaticText(self, label="Lirik : ")
        self.input_artis = wx.TextCtrl(self)
        self.input_judul = wx.TextCtrl(self)
        self.input_lirik = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL, label="Cancel")
        self.btn_add = wx.Button(self, wx.ID_OK, label="Add")
        
        flag = wx.EXPAND|wx.ALL
        self.GetSizer().Add(self.label_artis, pos=(0,0), flag=flag, border=2)
        self.GetSizer().Add(self.label_judul, pos=(1,0), flag=flag, border=2)
        self.GetSizer().Add(self.label_lirik, pos=(2,0), flag=flag, border=2)
        self.GetSizer().Add(self.input_artis, pos=(0,2), span=(1,25), flag=flag, border=2)
        self.GetSizer().Add(self.input_judul, pos=(1,2), span=(1,25), flag=flag, border=2)
        self.GetSizer().Add(self.input_lirik, pos=(2,2), span=(18,25), flag=flag, border=2)
        self.GetSizer().Add(self.btn_cancel, pos=(20,23), flag=flag, border=2)
        self.GetSizer().Add(self.btn_add, pos=(20,25), flag=flag, border=2)
        
        self.SetSize(self.GetBestFittingSize())
        self.SetEscapeId(wx.ID_CANCEL)
        
        # ------------ Event
        self.Bind(wx.EVT_BUTTON, self.__on_add_clicked, self.btn_add)
        self.Bind(wx.EVT_BUTTON, self.__on_cancel_clicked, self.btn_cancel)
        # ------------ End Event
        
    def __on_add_clicked(self, evt):
        self.data = [
            self.input_artis.GetValue(),
            self.input_judul.GetValue(),
            self.input_lirik.GetValue()
        ]
        self.EndModal(wx.ID_OK)
    
    def __on_cancel_clicked(self, evt):
        self.EndModal(wx.ID_CANCEL)
        self.data = []
    
    def GetData(self):
        return self.data
        
# XXX: testing only
if __name__ == "__main__":
    app = wx.App()
    fr = AddDataFrame(None)
    fr.Show()
    app.MainLoop()
