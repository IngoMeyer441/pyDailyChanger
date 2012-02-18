import wx
import wallpaper_setter


if __name__ == '__main__':
    app = wx.PySimpleApp()
    
    ws = wallpaper_setter.WallpaperSetter('/home/ingo/Bilder/xubuntu-wallpaper.png', '/home/ingo/test.bmp')
    ws.set_wallpaper()
    '''
    wc = wallpaper_setter.WallpaperCreator('/home/ingo/moz-screenshot.png')
    wc.createImage(False).SaveFile('/home/ingo/test.bmp', wx.BITMAP_TYPE_BMP)
    '''

