import wx
from gui.panel.file_panel import FilePanel
from gui.panel.options_panel import OptionsPanel
from gui.panel.font_panel import FontPanel
from gui.panel.color_panel import ColorPanel

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1)
    frame.panel = ColorPanel(frame, -1, ['font color', 'sundays', 'lines', 'test'], ['current day', 'background'])
    frame.Fit()
    frame.Center()
    frame.Show()
    app.MainLoop()