import wx
from util import graphics


class MemoImage:
    def __init__(self, appointment_list, memo_size=(100, 200),
                 memo_font_desc='Arial 8', memo_font_color=wx.BLACK,
                 memo_bg_colors = (wx.Colour(248, 255, 65), wx.Colour(252, 255, 172))):
        
        self.memo_image       = None
        self.appointment_list = appointment_list
        self.memo_size        = memo_size
        self.memo_font        = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.memo_font.SetNativeFontInfoFromString(memo_font_desc)
        self.memo_font_color  = memo_font_color
        self.memo_bg_colors   = memo_bg_colors
        
    def get_memo_image(self):
        '''
        Liefert eine grafische Darstellung des Memos als Bitmap.
        '''
        if self.memo_image:
            return self.memo_image
        
        self.memo_image = wx.EmptyBitmap(*self.memo_size, depth=32)
        dc = wx.GCDC(wx.MemoryDC(self.memo_image))
        
        dc.SetFont(self.memo_font)
        dc.SetTextForeground(self.memo_font_color)
        
        # Memo zeichnen
        graphics.draw_memo(dc, (0, 0), self.memo_size, self.memo_bg_colors, self.appointment_list)
            
        return self.memo_image
