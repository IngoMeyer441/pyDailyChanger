

if __name__ == '__main__':
    
    import util
    from config.config import *
    from util.graphics import *
    
    class TestFrame(wx.Frame):
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, *args, **kwargs)
            
            self.main_panel = wx.Panel(self, -1)
            
            self.main_panel.Bind(wx.EVT_PAINT, self.on_paint)
            self.main_panel.Bind(wx.EVT_LEFT_DCLICK, lambda evt: self.Refresh())
            
            self.appointment_list = util.get_appointment_list(APPOINTMENTS_CONFIG_FILE)
            
            self.Centre()
            self.Show()
            
            
        def on_paint(self, event):
            dc = wx.GCDC(wx.PaintDC(self.main_panel))
            
            draw_memo(dc, (0, 0), self.main_panel.GetSizeTuple(), (wx.Colour(255, 255, 255), wx.Colour(200, 200, 200)), self.appointment_list)
            
            '''
            dc.DrawRectangle(100, 100, 50, 50)
            draw_doted_spiral(dc, (125, 125), 15, 5, -85, 400, 10, lambda x: (x-1)**2)
            '''
            event.Skip()
            
    app = wx.App()
    frame = TestFrame(None, -1, size=(500, 500))
    app.MainLoop()