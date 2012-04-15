# -*- coding: utf-8 -*-

import wx
import time
import math

from util import util, graphics


day_counts = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
wday_names = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
month_names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

is_leap_year = lambda year: (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0)


class CalendarImage:
    def __init__(self, date=(2010, 1, 1), size=(500, 300), appointment_list=[],
                 heading_font_desc='Arial 10', 
                 wday_font_desc='Arial 10',
                 mday_font_desc='Arial 10',
                 font_color=wx.WHITE, sunday_font_color=wx.RED, line_color=wx.WHITE, 
                 day_colors=(wx.Colour(255, 128, 0), wx.Colour(255, 128, 0)), 
                 background_colors=(wx.Colour(0, 3, 153), wx.Colour(59, 136, 242)),
                 appointment_color=wx.GREEN):
        
        # date: (Tag, Monat, Jahr)
        # size: (Breite, Hoehe)
        self.given_date = time.strptime(str(date[2]) + ' ' + str(date[1]) + ' ' + str(date[0]), '%d %m %Y')
        self.wday1st = time.strptime('1 ' + str(date[1]) + ' ' + str(date[0]), '%d %m %Y').tm_wday
        self.is_leap_year = is_leap_year(date[0])
        self.day_count = day_counts[self.given_date.tm_mon - 1]
        if self.is_leap_year:
            self.day_count += 1

        self.cal_image = None
        self.size = size
        self.appointment_list = zip(*appointment_list)[0]
        self.heading_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.heading_font.SetNativeFontInfoFromString(heading_font_desc)
        self.wday_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.wday_font.SetNativeFontInfoFromString(wday_font_desc)
        self.mday_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.mday_font.SetNativeFontInfoFromString(mday_font_desc)
        self.font_color = font_color
        self.sunday_font_color = sunday_font_color
        self.line_color = line_color
        self.day_colors = day_colors
        self.background_colors = background_colors
        self.appointment_color = appointment_color
        
        self.font2cell_ratio = 2.0 / 3      # Groessenanteil der Schriftgroesse an der Zellenbreite bzw. -hoehe
        
        
    def get_calendar_image(self):
        '''
        Liefert eine grafische Darstellung des Kalenders als Bitmap.
        '''
        if self.cal_image:
            return self.cal_image
        
        width, height = self.size
        columns = 7
        rows = int(math.ceil(1.0 * (self.day_count + self.wday1st) / columns)) + 2    # + 2 fuer die Zeile des Monats und Jahrs + Leiste der Wochentage
        cell_width  = int(round(1.0 * width / columns))
        cell_height = int(round(1.0 * height / rows))
        
        get_top_left_corner = lambda mday: (((mday + self.wday1st - 1) % columns)     * cell_width,
                                            ((mday + self.wday1st - 1) / columns + 2) * cell_height)
        
        self.cal_image = wx.EmptyBitmap(*self.size, depth=32)
        dc = wx.GCDC(wx.MemoryDC(self.cal_image))
        # Hintergrundfarbe setzen:
        dc.GradientFillLinear(wx.Rect(0, 0, width, height), self.background_colors[0], self.background_colors[1], wx.DOWN)
        # aktuellen Tag markieren:
        x, y = get_top_left_corner(self.given_date.tm_mday)
        dc.GradientFillLinear(wx.Rect(x, y, cell_width, cell_height), self.day_colors[0], self.day_colors[1], wx.DOWN)
        # Gitter zeichnen:
        dc.SetPen(wx.Pen(self.line_color))
        # in x-Richtung:
        for i in range(1, columns):
            x = i * cell_width
            dc.DrawLinePoint((x, 2*cell_height), (x, height))
        # in y-Richtung:
        for i in range(1, rows):
            y = i * cell_height
            dc.DrawLinePoint((0, y), (width, y))  
        # Titel zeichnen:
        # Optimale Fontgroesse bestimmen
        title = month_names[self.given_date.tm_mon-1] + ' - ' + str(self.given_date.tm_year)
        dc.SetFont(self.heading_font)
        point_size_and_extent = util.get_optimal_font_size_and_text_extent(dc, title, (width - self.font2cell_ratio*cell_height, self.font2cell_ratio*cell_height))
        self.heading_font.SetPointSize(point_size_and_extent[0])
        dc.SetFont(self.heading_font)
        dc.SetTextForeground(self.font_color)
        dc.DrawTextPoint(title, ((width-point_size_and_extent[1][0]) / 2, ((cell_height-point_size_and_extent[1][1]) / 2)))
        # Leiste mit Wochentagen zeichnen
        dc.SetFont(self.wday_font)
        point_size = util.get_optimal_font_size_and_text_extent(dc, 'Mo', (self.font2cell_ratio*cell_width, self.font2cell_ratio*cell_height))[0]
        self.wday_font.SetPointSize(point_size)
        dc.SetFont(self.wday_font)
        dc.SetTextForeground(self.font_color)
        for (i, wday) in enumerate(wday_names):
            # Sonntag
            if i == 6:
                dc.SetTextForeground(self.sunday_font_color)
            extent = dc.GetTextExtent(wday)
            x = i * cell_width + (cell_width - extent[0]) / 2
            y = cell_height + (cell_height - extent[1]) / 2
            dc.DrawTextPoint(wday, (x, y))
        # Terminmarkierungen und Zahlen eintragen:
        dc.SetFont(self.mday_font)
        point_size = util.get_optimal_font_size_and_text_extent(dc, '30', (self.font2cell_ratio*cell_width, self.font2cell_ratio*cell_height))[0]
        self.mday_font.SetPointSize(point_size)
        dc.SetFont(self.mday_font)
        for i in range(1, day_counts[self.given_date.tm_mon-1] + 1):
            # Zahl zeichnen:
            if ((i-1) + self.wday1st) % 7 < 6:
                dc.SetTextForeground(self.font_color)
            else:
                dc.SetTextForeground(self.sunday_font_color)
            extent = dc.GetTextExtent(str(i))
            x, y = get_top_left_corner(i)
            x, y = (x + (cell_width - extent[0]) / 2, y + (cell_height - extent[1]) / 2)
            dc.DrawTextPoint(str(i), (x, y))
            # Evtl. Terminmarkierung eintragen:
            if (self.given_date.tm_year, self.given_date.tm_mon, i) in self.appointment_list:
                dc.SetPen(wx.Pen(self.appointment_color))
                x, y = get_top_left_corner(i)
                x, y = (x + cell_width/2, y + cell_height/2)
                minimum = min(cell_width, cell_height)
                graphics.draw_doted_spiral(dc, (x, y), minimum*0.75, minimum*0.5, -85, 400, minimum*0.5, lambda x: (x-1)**8)
            
        return self.cal_image