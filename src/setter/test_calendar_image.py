import wx
import calendar_image

if __name__ == '__main__':
    app = wx.PySimpleApp()
    cal_im = calendar_image.CalendarImage((11, 7, 2011), (600, 400))
    cal_im.get_calendar_image().SaveFile('/home/ingo/cal.bmp', wx.BITMAP_TYPE_BMP)