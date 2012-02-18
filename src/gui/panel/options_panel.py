import wx
from util import util


class OptionsPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.ids = util.IdGetter()
        
        # Sizer
        self.sizer = wx.GridBagSizer(5, 5)
        
        # CheckBox
        self.cb_calendar = wx.CheckBox(self, self.ids.cb_calendar, 'show calendar')
        self.sizer.Add(self.cb_calendar, (0, 0), (1, 1))
        self.cb_stretch = wx.CheckBox(self, self.ids.cb_stretch, 'stretch images')
        self.sizer.Add(self.cb_stretch, (1, 0), (1, 1))
        
        # set sizer
        self.SetSizerAndFit(self.sizer)