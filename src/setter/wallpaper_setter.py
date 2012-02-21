import wx
import time

from util import util
import calendar_image

CAL_TOP_LEFT      = 0
CAL_TOP_RIGHT     = 1
CAL_BOTTOM_LEFT   = 2
CAL_BOTTOM_RIGHT  = 3
CAL_SCREEN_CENTER = 4

class WallpaperSetter():
    '''
    Uebernimmt das Setzen des neuen Hintergrundbildes
    '''
    
    def __init__(self, 
                 source_file, 
                 dest_file, 
                 mask_color=wx.BLACK, 
                 stretch=False,
                 keep_aspect_ratio=True, 
                 draw_cal=True,
                 appointment_descriptions_of_next_days=7,
                 appointment_list = [], 
                 cal_pos=CAL_BOTTOM_RIGHT, 
                 cal_size=(0.25, 0.25), 
                 cal_alpha=153, 
                 cal_heading_font_desc='Arial 10', 
                 cal_wday_font_desc=   'Arial 10', 
                 cal_mday_font_desc=   'Arial 10', 
                 cal_font_color=wx.WHITE, 
                 cal_sunday_font_color=wx.RED, 
                 cal_line_color=wx.WHITE, 
                 cal_day_colors=(wx.Colour(255, 128, 0), wx.Colour(255, 128, 0)), 
                 cal_background_colors=(wx.Colour(0, 3, 153), wx.Colour(59, 136, 242)),
                 cal_appointment_color=wx.GREEN):
        
        self.dest_file = dest_file
        self.w_creator = WallpaperCreator(source_file, mask_color, stretch, keep_aspect_ratio, draw_cal, appointment_descriptions_of_next_days,
                                          appointment_list, cal_pos, cal_size, cal_alpha,
                                          cal_heading_font_desc, cal_wday_font_desc, cal_mday_font_desc,
                                          cal_font_color, cal_sunday_font_color, cal_line_color, cal_day_colors,
                                          cal_background_colors, cal_appointment_color)
        self.w_im = None
        
    def set_wallpaper(self):
        '''
        Liefert True, wenn der Vorgang erfolgreich ist und False, wenn kein gueltiges Bild vorliegt
        '''
        
        if not self.w_im:
            self.w_im = self.w_creator.createImage()
            if not self.w_im:
                return False
        self.w_im.SaveFile(self.dest_file, wx.BITMAP_TYPE_BMP)
        util.set_wallpaper(self.dest_file)
        return True
        
    def set_source_file(self, file):
        self.w_creator.set_source_file(file)
        

class WallpaperCreator():
    '''
    Erstellt das neue Hintergrundbild, Hilfsklasse des WallpaperSetters
    '''
    
    def __init__(self, 
                 source_file='', 
                 mask_color=wx.BLACK, 
                 stretch=False,
                 keep_aspect_ratio=True,
                 draw_cal=True,
                 appointment_descriptions_of_next_days=7,
                 appointment_list = [],
                 cal_pos=CAL_BOTTOM_RIGHT, 
                 cal_size=(0.25, 0.25), 
                 cal_alpha=153, 
                 cal_heading_font_desc='Arial 10', 
                 cal_wday_font_desc=   'Arial 10', 
                 cal_mday_font_desc=   'Arial 10', 
                 cal_font_color=wx.WHITE, 
                 cal_sunday_font_color=wx.RED, 
                 cal_line_color=wx.WHITE,
                 cal_day_colors=(wx.Colour(255, 128, 0), wx.Colour(255, 128, 0)),
                 cal_background_colors=(wx.Colour(0, 3, 153), wx.Colour(59, 136, 242)),
                 cal_appointment_color=wx.GREEN):
        '''
        cal_pos enthaelt entweder eine vorgefertigte Konstante oder einen Tupel, der entweder relative oder absolute
        Positionsangaben enthalten kann ( < 1: relativ, >= 1 absolut)
        cal_size enthaelt auch entweder eine relative oder absolute Groessenangabe
        Alle relativen Angaben orientieren sich an der Bildschirmaufloesung
        '''
        
        self.source_file = source_file
        self.mask_color = mask_color
        self.stretch = stretch
        self.keep_aspect_ratio = keep_aspect_ratio
        self.draw_cal = draw_cal
        self.appointment_descriptions_of_next_days = appointment_descriptions_of_next_days
        self.appointment_list = appointment_list
        self.cal_pos = cal_pos
        self.cal_size = cal_size
        self.cal_heading_font_desc = cal_heading_font_desc
        self.cal_wday_font_desc = cal_wday_font_desc
        self.cal_mday_font_desc = cal_mday_font_desc
        self.cal_alpha = cal_alpha
        self.cal_font_color = cal_font_color
        self.cal_sunday_font_color = cal_sunday_font_color
        self.cal_line_color = cal_line_color
        self.cal_day_colors = cal_day_colors
        self.cal_background_colors = cal_background_colors
        self.cal_appointment_color = cal_appointment_color
        
        self.screen_size = wx.Display().GetGeometry().GetSize()
        
    def createImage(self):
        w_im = wx.Image(self.source_file)
        
        # Pruefen, ob es ein gueltiges Bild ist:
        if w_im.GetSize()[0] <= 0 or w_im.GetSize()[1] <= 0:
            return None
        
        # Hintergrundbild vorbereiten
        best_size = self.__get_optimal_size(w_im, self.stretch, self.keep_aspect_ratio)
        # Muss ein Resize vorgenommen werden?
        if best_size is not None:
            w_im.Rescale(*best_size, quality=wx.IMAGE_QUALITY_HIGH)
            real_size = best_size
        else:
            real_size = w_im.GetSize()
        # Fehlenden Platz fuer den Desktop auffuellen
        if (self.screen_size[0] > real_size[0]) or (self.screen_size[1] > real_size[1]):
            tmp_bm = wx.EmptyBitmap(*self.screen_size)
            tmp_dc = wx.MemoryDC(tmp_bm)
            tmp_dc.SetBackground(wx.Brush(self.mask_color))
            tmp_dc.Clear()
            tmp_im = tmp_bm.ConvertToImage()
            (x, y) = ((self.screen_size[0]-real_size[0]) / 2, (self.screen_size[1]-real_size[1]) / 2)
            tmp_im.Paste(w_im, x, y)
            w_im = tmp_im
            
        # Kalender zeichnen, falls dieser erwuenscht ist:
        if self.draw_cal:
            # Groesse in Pixeln
            abs_cal_size = list(self.cal_size)
            for i in range(len(self.cal_size)):
                if abs_cal_size[i] < 1:
                    abs_cal_size[i] = int(round(abs_cal_size[i] * self.screen_size[i]))
            # Position in Pixeln
            if isinstance(self.cal_pos, int):
                if   self.cal_pos == CAL_TOP_LEFT:
                    abs_cal_pos = (0, 0)
                elif self.cal_pos == CAL_TOP_RIGHT:
                    abs_cal_pos = (self.screen_size[0]-abs_cal_size[0], 0)
                elif self.cal_pos == CAL_BOTTOM_LEFT:
                    abs_cal_pos = (0, self.screen_size[1]-abs_cal_size[1])
                elif self.cal_pos == CAL_BOTTOM_RIGHT:
                    abs_cal_pos = (self.screen_size[0]-abs_cal_size[0], self.screen_size[1]-abs_cal_size[1])
                elif self.cal_pos == CAL_SCREEN_CENTER:
                    abs_cal_pos = ((self.screen_size[0]-abs_cal_size[0]) / 2, (self.screen_size[1]-abs_cal_size[1]) / 2)
            else:
                abs_cal_pos = list(self.cal_pos)
                for i in range(len(self.cal_pos)):
                    if abs_cal_pos[i] < 1:
                        abs_cal_pos[i] = int(round(abs_cal_pos[i] * self.screen_size[i]))
            cal = calendar_image.CalendarImage(time.localtime()[0:3], abs_cal_size, self.appointment_descriptions_of_next_days,
                                               self.appointment_list,
                                               self.cal_heading_font_desc,self.cal_wday_font_desc, self.cal_mday_font_desc, 
                                               self.cal_font_color, self.cal_sunday_font_color, self.cal_line_color, 
                                               self.cal_day_colors, self.cal_background_colors, self.cal_appointment_color)
            cal_im = cal.get_calendar_image().ConvertToImage()
            cal_im.InitAlpha()
            cal_im.SetAlphaData(chr(self.cal_alpha) * (abs_cal_size[0]*abs_cal_size[1]))
            tmp_bm = w_im.ConvertToBitmap()
            tmp_dc = wx.GCDC(wx.MemoryDC(tmp_bm))
            tmp_dc.DrawBitmap(cal_im.ConvertToBitmap(), abs_cal_pos[0], abs_cal_pos[1])
            w_im = tmp_bm.ConvertToImage()
            
        return w_im
        
    def set_source_file(self, file):
        self.source_file = file
                
    def __get_optimal_size(self, im, stretch=False, keep_aspect_ratio=True):
        '''
        Liefert die optimale Groesse des Bildes bzw. None, falls kein Rescale notwendig ist.
        '''
        
        size = None
        im_size = im.GetSize()
        
        while True:
            if stretch:
                # Passt das Bild schon genau auf den Bildschirm?
                if (im_size[0] == self.screen_size[0] and im_size[1] <= self.screen_size[1]) or (im_size[1] == self.screen_size[1] and im_size[0] <= self.screen_size[0]):
                    size = None
                else:
                    if keep_aspect_ratio:
                        im_format = float(im_size[0]) / im_size[1]
                        screen_format = float(self.screen_size[0]) / self.screen_size[1]
                        if im_format >= screen_format:
                            size = (self.screen_size[0], self.screen_size[0] / im_format)
                        else:
                            size = (self.screen_size[1] * im_format, self.screen_size[1])
                    else:
                        size = tuple(self.screen_size)
                break
            else:
                if (im_size[0] <= self.screen_size[0]) and (im_size[1] <= self.screen_size[1]):
                    size = None
                    break
                else:
                    stretch = True
                    keep_aspect_ratio = True
        
        return size