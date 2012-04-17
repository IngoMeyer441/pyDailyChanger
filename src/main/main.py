#coding: utf-8

import wx
import optparse
import sys
from setter import random_file_picker, wallpaper_setter
from util import util
from config.config import *

options_list = [{'short': '-u', 'long': '--update', 'action': 'store_true', 'dest': 'update', 'default': False}]

def parse_command_line_options():
    parser = optparse.OptionParser()
    for option_dict in options_list:
        tmp_dict = dict(option_dict)
        del tmp_dict['short']
        del tmp_dict['long']
        parser.add_option(option_dict['short'], option_dict['long'], **tmp_dict)
    return parser.parse_args()

def run_main():
    options, args = parse_command_line_options()
    passed_days = None
    
    if not options.update:
        passed_days = util.get_number_of_passed_days(PASSED_DAYS_CONFIG_FILE)
    
    if not (options.update or passed_days is None or passed_days >= DAY_THRESHOLD):
        sys.exit()
        
    app = wx.App()
    cfg = get_config_parser()
    
    if options.update and cfg.main.last_wallpaper_image == '':
        sys.exit()
        
    if not options.update:
        file_picker = random_file_picker.RandomFilePicker(util.get_path_list(PATH_LIST_FILE), FILE_TYPE_LIST, FILE_PICKER_CONFIG_FILE)
    
    if cfg.calendar.cal_pos[0] < 0:
        cal_pos = int(round(cfg.calendar.cal_pos[1]))
    else:
        cal_pos = cfg.calendar.cal_pos
        
    if cfg.memo.memo_pos[0] < 0:
        memo_pos = int(round(cfg.memo.memo_pos[1]))
    else:
        memo_pos = cfg.memo.memo_pos
      
    files_to_ignore = [cfg.main.last_wallpaper_image]
     
    w_setter = wallpaper_setter.WallpaperSetter(
               '', 
               cfg.main.dest_file, 
               wx.Colour(*cfg.main.mask_color),
               cfg.main.stretch, 
               cfg.main.keep_aspect_ratio,
               cfg.calendar.draw_cal,
               util.get_appointment_list(APPOINTMENTS_CONFIG_FILE),
               cfg.calendar.cal_continuous, 
               cfg.calendar.cal_continuous_rows, 
               cfg.calendar.cal_current_day_row,
               cal_pos, 
               cfg.calendar.cal_size,
               cfg.calendar.cal_alpha, 
               cfg.calendar.cal_heading_font_desc,
               cfg.calendar.cal_wday_font_desc,
               cfg.calendar.cal_mday_font_desc,
               wx.Colour(*cfg.calendar.cal_font_color),
               wx.Colour(*cfg.calendar.cal_sunday_font_color),
               wx.Colour(*cfg.calendar.cal_line_color),
               (wx.Colour(*cfg.calendar.cal_day_color1), wx.Colour(*cfg.calendar.cal_day_color2)),
               (wx.Colour(*cfg.calendar.cal_background_color1), wx.Colour(*cfg.calendar.cal_background_color2)),
               wx.Colour(*cfg.calendar.cal_appointment_color),
               cfg.memo.draw_memo,
               memo_pos,
               cfg.memo.memo_size, 
               cfg.memo.memo2cal_border,
               cfg.memo.memo_alpha, 
               cfg.memo.memo_font_desc,
               wx.Colour(*cfg.memo.memo_font_color),
               (wx.Colour(*cfg.memo.memo_background_color1), wx.Colour(*cfg.memo.memo_background_color2)))
    
    if options.update:
        w_setter.set_source_file(cfg.main.last_wallpaper_image)
        if not w_setter.set_wallpaper():
            print 'Das Hintergrundbild konnte nicht aktualisiert werden, da es nicht mehr zur Verfügung steht.'
            wx.MessageDialog(None, 'Das Hintergrundbild konnte nicht aktualisiert werden, da es nicht mehr zur Verfügung steht.',
                             'Fehler:', wx.OK | wx.CENTRE).ShowModal()
    else:
        while(True):
            try:
                w_setter.set_source_file(file_picker.get_next_file(files_to_ignore))
                # Solange das Setzen des Hintergrundbildes aufgrund einer fehlerhaften Bilddatei nicht funktioniert
                while not w_setter.set_wallpaper():
                    files_to_ignore.append(file_picker.get_current_file())
                    w_setter.set_source_file(file_picker.get_next_file(files_to_ignore))
                # Das gefundene Bild in die Konfigdatei eintragen
                cfg.main.last_wallpaper_image = file_picker.get_current_file()
                break
            except random_file_picker.NoValidEntryError:
                # Ist kein gueltiges Bild dabei, so lasse auch wieder das Bild aus dem vorherigen Schritt zu,
                # falls es nicht schon aus der Ignore-Liste genommen wurde. Ansonsten beende das Programm mit
                # einer Fehlermeldung
                if cfg.main.last_wallpaper_image in files_to_ignore:
                    files_to_ignore.remove(cfg.main.last_wallpaper_image)
                else:
                    print 'Es gibt keine gültige Bilddatei unter den angegeben Dateien / Verzeichnissen.'
                    wx.MessageDialog(None, 'Es gibt keine gültige Bilddatei unter den angegeben Dateien / Verzeichnissen.',
                                     'Fehler:', wx.OK | wx.CENTRE).ShowModal()
                    sys.exit(1)