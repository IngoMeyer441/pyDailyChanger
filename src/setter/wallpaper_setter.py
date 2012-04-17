import wx
import time

from util import util
import calendar_image
import memo_image

CAL_TOP_LEFT      = 0
CAL_TOP_RIGHT     = 1
CAL_BOTTOM_LEFT   = 2
CAL_BOTTOM_RIGHT  = 3
CAL_SCREEN_CENTER = 4

MEMO_LEFT =   0
MEMO_TOP =    1
MEMO_RIGHT =  2
MEMO_BOTTOM = 3
    


def get_future_appointments(appointments_list, current_date):
    year, month, day = current_date
    index = 0
    for app in zip(*appointments_list)[0]:
        if app[0] > year or (app[0] == year and app[1] > month) or (app[0] == year and app[1] == month and app[2] >= day):
            break
        index += 1
    return appointments_list[index:]


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
                 appointment_list = [],
                 continuous=False, 
                 continuous_rows=7, 
                 current_day_row=1, 
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
                 cal_appointment_color=wx.GREEN,
                 draw_memo=False,
                 memo_pos=(-1.0, MEMO_LEFT),
                 memo_size=(0.1, 0.2), 
                 memo2cal_border=0.01,
                 memo_alpha=153, 
                 memo_font_desc='Arial 8',
                 memo_font_color=wx.BLACK,
                 memo_background_colors=(wx.Colour(248, 255, 65), wx.Colour(252, 255, 172)),
                 ):
        
        self.dest_file = dest_file
        self.w_creator = WallpaperCreator(source_file, mask_color, stretch, keep_aspect_ratio, draw_cal,
                                          appointment_list, continuous, continuous_rows, current_day_row,
                                          cal_pos, cal_size, cal_alpha,
                                          cal_heading_font_desc, cal_wday_font_desc, cal_mday_font_desc,
                                          cal_font_color, cal_sunday_font_color, cal_line_color, cal_day_colors,
                                          cal_background_colors, cal_appointment_color,
                                          draw_memo, memo_pos, memo_size,  memo2cal_border,
                                          memo_alpha, memo_font_desc, memo_font_color, memo_background_colors)
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
                 appointment_list = [],
                 continuous=False, 
                 continuous_rows=7, 
                 current_day_row=1,
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
                 cal_appointment_color=wx.GREEN,
                 draw_memo=False,
                 memo_pos=(-1.0, MEMO_LEFT),
                 memo_size=(0.1, 0.2), 
                 memo2cal_border=0.01,
                 memo_alpha=153, 
                 memo_font_desc='Arial 8',
                 memo_font_color=wx.BLACK,
                 memo_background_colors=(wx.Colour(248, 255, 65), wx.Colour(252, 255, 172)),
                 ):
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
        self.appointment_list = appointment_list
        self.continuous = continuous
        self.continuous_rows = continuous_rows
        self.current_day_row = current_day_row
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
        self.draw_memo = draw_memo
        self.memo_pos = memo_pos
        self.memo_size = memo_size 
        self.memo2cal_border = memo2cal_border
        self.memo_alpha = memo_alpha 
        self.memo_font_desc = memo_font_desc
        self.memo_font_color = memo_font_color
        self.memo_background_colors = memo_background_colors
        
        self.screen_size = wx.Display().GetGeometry().GetSize()
        
    def createImage(self):
        
        def convert_relative2absolute_pos(relative_pos):
            '''
            Konvertiert relative zu absoluten Koordinaten, falls diese relativ sind. Sind sie schon
            absolut, so bleiben sie unveraendert.
            '''
            abs_pos = list(relative_pos)
            for i in range(len(abs_pos)):
                if abs_pos[i] < 1:
                    abs_pos[i] = int(round(abs_pos[i] * self.screen_size[i]))
            return tuple(abs_pos)
        
        
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
            abs_cal_size = convert_relative2absolute_pos(self.cal_size)
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
                abs_cal_pos = convert_relative2absolute_pos(self.cal_pos)
            cal = calendar_image.CalendarImage(time.localtime()[0:3], abs_cal_size,
                                               self.appointment_list,
                                               self.continuous, self.continuous_rows, self.current_day_row,
                                               self.cal_heading_font_desc,self.cal_wday_font_desc, self.cal_mday_font_desc, 
                                               self.cal_font_color, self.cal_sunday_font_color, self.cal_line_color, 
                                               self.cal_day_colors, self.cal_background_colors, self.cal_appointment_color)
            cal_im = cal.get_calendar_image().ConvertToImage()
            cal_im.InitAlpha()
            cal_im.SetAlphaData(chr(self.cal_alpha) * (abs_cal_size[0]*abs_cal_size[1]))
            tmp_bm = w_im.ConvertToBitmap()
            tmp_dc = wx.GCDC(wx.MemoryDC(tmp_bm))
            tmp_dc.DrawBitmap(cal_im.ConvertToBitmap(), abs_cal_pos[0], abs_cal_pos[1])
            
            # Zusaetzlich Memo zeichnen, falls dies erwuenscht ist:
            if self.draw_memo:
                # Groesse in Pixeln
                abs_memo_size = convert_relative2absolute_pos(self.memo_size)
                # Rand
                memo2cal_border = convert_relative2absolute_pos((self.memo2cal_border, ))[0]
                # Position in Pixeln
                if isinstance(self.memo_pos, int):
                    if   self.memo_pos == MEMO_LEFT:
                        x = abs_cal_pos[0] - abs_memo_size[0] - memo2cal_border
                        y = abs_cal_pos[1] + abs_cal_size[1]/2 - abs_memo_size[1]/2     
                    elif self.memo_pos == MEMO_TOP:
                        x = abs_cal_pos[0] + abs_cal_size[0]/2 - abs_memo_size[0]/2
                        y = abs_cal_pos[1] - abs_memo_size[1] - memo2cal_border
                    elif self.memo_pos == MEMO_RIGHT:
                        x = abs_cal_pos[0] + abs_cal_size[0] + memo2cal_border
                        y = abs_cal_pos[1] + abs_cal_size[1]/2 - abs_memo_size[1]/2 
                    elif self.memo_pos == MEMO_BOTTOM:
                        x = abs_cal_pos[0] + abs_cal_size[0]/2 - abs_memo_size[0]/2
                        y = abs_cal_pos[1] + abs_cal_size[1] + memo2cal_border
                    x = min(self.screen_size[0]-abs_memo_size[0], max(0, x))
                    y = min(self.screen_size[1]-abs_memo_size[1], max(0, y))
                    abs_memo_pos = (x, y)
                else:
                    abs_memo_pos = convert_relative2absolute_pos(self.memo_pos)
                memo = memo_image.MemoImage(get_future_appointments(self.appointment_list, time.localtime()[0:3]),
                                            abs_memo_size, self.memo_font_desc, 
                                            self.memo_font_color, self.memo_background_colors)
                memo_im = memo.get_memo_image().ConvertToImage()
                memo_im.InitAlpha()
                memo_im.SetAlphaData(chr(self.memo_alpha) * (abs_memo_size[0]*abs_memo_size[1]))
                tmp_dc.DrawBitmap(memo_im.ConvertToBitmap(), abs_memo_pos[0], abs_memo_pos[1])
                     
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