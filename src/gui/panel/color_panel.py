import wx
from util import util

class ColorPanel(wx.Panel):
    def __init__(self, parent, id, one_color_labels=[], two_color_labels=[], initial_one_colors=None, initial_two_colors=None):
        wx.Panel.__init__(self, parent, id)
        
        if initial_one_colors is None:
            initial_one_colors = len(one_color_labels) * [(0, 0, 0)]
        if initial_two_colors is None:
            initial_two_colors = len(two_color_labels) * [((0, 0, 0), (0, 0, 0))]
        
        self.ids = util.IdGetter()
        
        # Sizer
        self.sizer = wx.GridBagSizer(5, 10)
        
        # StaticText
        self.st_one_colors = []
        for i, label in enumerate(one_color_labels):
            self.st_one_colors.append(wx.StaticText(self, self.ids.st_one_colors[i], label+':'))
            self.sizer.Add(self.st_one_colors[-1], (i/3, 3*(i%3)), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.st_two_colors = []
        for i, label in enumerate(two_color_labels):
            self.st_two_colors.append(wx.StaticText(self, self.ids.st_two_colors[i], label+':'))
            self.sizer.Add(self.st_two_colors[-1], (int(len(self.st_one_colors)-1)/3 + 1 + i/3, 3*(i%3)), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        # (Color)Panel
        self.pa_one_colors = []
        for i in range(len(one_color_labels)):
            self.pa_one_colors.append(wx.Panel(self, self.ids.pa_one_colors[i], size=(20, 20)))
            self.pa_one_colors[-1].SetBackgroundColour(wx.Colour(*initial_one_colors[i]))
            self.sizer.Add(self.pa_one_colors[-1], (i/3, 3*(i%3)+1), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.pa_two_colors = []
        for i in range(len(two_color_labels)):
            self.pa_two_colors.append((wx.Panel(self, self.ids.pa_two_colors[i][0], size=(20, 20)), wx.Panel(self, self.ids.pa_two_colors[i][1], size=(20, 20))))
            self.pa_two_colors[-1][0].SetBackgroundColour(wx.Colour(*initial_two_colors[i][0]))
            self.pa_two_colors[-1][1].SetBackgroundColour(wx.Colour(*initial_two_colors[i][1]))
            self.sizer.Add(self.pa_two_colors[-1][0], (int(len(self.pa_one_colors)-1)/3 + 1 + i/3, 3*(i%3) + 1), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
            self.sizer.Add(self.pa_two_colors[-1][1], (int(len(self.pa_one_colors)-1)/3 + 1 + i/3, 3*(i%3) + 2), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
            
        # set sizer
        self.SetSizerAndFit(self.sizer)
        
        
class ColorChooser(wx.Panel):
    
    def __init__(self, parent, id, label, initial_colors=[(0, 0, 0)]):
        wx.Panel.__init__(self, parent, id)
        
        self.two_color = len(initial_colors) == 2
        
        self.ids = util.IdGetter()
        
        # Sizer
        self.sizer = wx.GridBagSizer(5, 10)
        
        # StaticText
        self.st_label = wx.StaticText(self, self.ids.st_label, label + ':')
        self.sizer.Add(self.st_label, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.pa_first_color = wx.Panel(self, self.ids.pa_first_color, size=(20, 20))
        self.pa_first_color.SetBackgroundColour(wx.Colour(*initial_colors[0]))
        self.sizer.Add(self.pa_first_color, (0, 1), (1, 1), wx.ALIGN_CENTER)
        if self.two_color:
            self.pa_second_color = wx.Panel(self, self.ids.pa_second_color, size=(20, 20))
            self.pa_second_color.SetBackgroundColour(wx.Colour(*initial_colors[1]))
            self.sizer.Add(self.pa_second_color, (0, 2), (1, 1), wx.ALIGN_CENTER)
        # ColorDialog
        self.cl_color = wx.ColourDialog(self)
            
        # set sizer
        self.SetSizerAndFit(self.sizer)