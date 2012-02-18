import wx
from util import util

class FilePanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.ids = util.IdGetter()
        
        # Sizer
        self.sizer = wx.GridBagSizer(5, 5)
        self.sb_dir_file_list_sizer = wx.GridBagSizer(5, 5)
        self.sb_dir_content_sizer = wx.GridBagSizer(5, 5)
        self.sb_preview_sizer = wx.GridBagSizer(5, 5)
        # StaticBox
        self.sb_dir_file_list = wx.StaticBoxSizer(wx.StaticBox(self, self.ids.sb_dir_file_list, 'directory/file list'))
        self.sb_dir_file_list.Add(self.sb_dir_file_list_sizer, 1, wx.EXPAND)
        self.sizer.Add(self.sb_dir_file_list, (0, 0), (2, 1), wx.EXPAND)
        self.sb_dir_content = wx.StaticBoxSizer(wx.StaticBox(self, self.ids.sb_dir_content, 'directory content'))
        self.sb_dir_content.Add(self.sb_dir_content_sizer, 1, wx.EXPAND)
        self.sizer.Add(self.sb_dir_content, (0, 1), (1, 1), wx.EXPAND)
        self.sb_preview = wx.StaticBoxSizer(wx.StaticBox(self, self.ids.sb_preview, 'preview'))
        self.sb_preview.Add(self.sb_preview_sizer, 1, wx.EXPAND)
        self.sizer.Add(self.sb_preview, (1, 1), (1, 1), wx.EXPAND)
        # ListCtrl
        self.lc_dir_file_list = wx.ListCtrl(self, self.ids.lc_dir_file_list, style=wx.LC_ICON)
        self.sb_dir_file_list_sizer.Add(self.lc_dir_file_list, (0, 1), (3, 1), wx.EXPAND)
        self.lc_dir_content   = wx.ListCtrl(self, self.ids.lc_dir_content, style=wx.LC_ICON)
        self.sb_dir_content_sizer.Add(self.lc_dir_content, (0, 0), (1, 1), wx.EXPAND)
        # StaticBitmap
        self.sbi_preview = wx.StaticBitmap(self, self.ids.sbi_preview)
        self.sb_preview_sizer.Add(self.sbi_preview, (0, 0), (1, 1), wx.EXPAND)
        # BitmapButton
        self.bb_add =    wx.BitmapButton(self, self.ids.bb_add, wx.ArtProvider().GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON))
        self.sb_dir_file_list_sizer.Add(self.bb_add, (0, 0), (1, 1), wx.ALIGN_CENTER)
        self.bb_delete = wx.BitmapButton(self, self.ids.bb_delete, wx.ArtProvider().GetBitmap(wx.ART_DELETE, wx.ART_BUTTON))
        self.sb_dir_file_list_sizer.Add(self.bb_delete, (1, 0), (1, 1), wx.ALIGN_CENTER)
        
        # set sizers
        self.sb_dir_file_list_sizer.AddGrowableRow(2)
        self.sb_dir_file_list_sizer.AddGrowableCol(1)
        self.sb_dir_content_sizer.AddGrowableRow(0)
        self.sb_dir_content_sizer.AddGrowableCol(0)
        self.sb_preview_sizer.AddGrowableRow(0)
        self.sb_preview_sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableCol(1)
        self.SetSizerAndFit(self.sizer)
        