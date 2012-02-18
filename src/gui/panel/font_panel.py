import wx
from util import util

class FontPanel(wx.Panel):
    def __init__(self, parent, id, labels=[]):
        '''
        labels ist eine Liste von Strings, die die Elemente enthaelt, deren Schriften gesetzt werden sollen (z.B. >Titel<)
        '''
        wx.Panel.__init__(self, parent, id)
        
        self.ids = util.IdGetter()
        
        # Sizer
        self.sizer = wx.GridBagSizer(5, 5)
        
        self.st_labels =   []
        self.fs_settings = []
        for i, label in enumerate(labels):
            # StaticText
            self.st_labels.append(wx.StaticText(self, self.ids.st_labels[i], label + ':'))
            self.sizer.Add(self.st_labels[-1], (2*i, 0), (1, 1), wx.TOP, 5)
            # FontSettingsPanel
            self.fs_settings.append(FontSettingsPanel(self, self.ids.fs_settings[i]))
            self.sizer.Add(self.fs_settings[-1], (2*i+1, 0), (1, 1), wx.BOTTOM, 5)
            
        # set sizer
        self.SetSizerAndFit(self.sizer)
            
    
    
class FontSettingsPanel(wx.Panel):
    
    font_types = []
    font_styles = []
    font_width = []
    
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.ids = util.IdGetter()
        
        # Sizer
        self.sizer = wx.GridBagSizer(5, 10)
        
        # StaticText
        self.st_type = wx.StaticText(self, self.ids.st_type, 'type:')
        self.sizer.Add(self.st_type, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.st_style = wx.StaticText(self, self.ids.st_style, 'style:')
        self.sizer.Add(self.st_style, (0, 2), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.st_width = wx.StaticText(self, self.ids.st_width, 'width:')
        self.sizer.Add(self.st_width, (0, 4), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        # ComboBox
        self.cb_type = wx.ComboBox(self, self.ids.cb_type)
        self.sizer.Add(self.cb_type, (0, 1), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.cb_style = wx.ComboBox(self, self.ids.cb_style)
        self.sizer.Add(self.cb_style, (0, 3), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.cb_width = wx.ComboBox(self, self.ids.cb_width)
        self.sizer.Add(self.cb_width, (0, 5), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        
        # set sizer
        self.SetSizerAndFit(self.sizer)
        