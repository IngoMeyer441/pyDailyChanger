import wx
import sys
from setter import random_file_picker, wallpaper_setter
from util import util
from config.config import *


def run_main():
    passed_days = util.get_number_of_passed_days(PASSED_DAYS_CONFIG_FILE)
    
    if passed_days is None or passed_days >= DAY_THRESHOLD:     # ansonten terminiere
        app = wx.PySimpleApp()
        cfg = get_config_parser()
        file_picker = random_file_picker.RandomFilePicker(util.get_path_list(PATH_LIST_FILE), FILE_TYPE_LIST, FILE_PICKER_CONFIG_FILE)
        
        if cfg.calendar.cal_pos[0] < 0:
            cal_pos = int(round(cfg.calendar.cal_pos[1]))
        else:
            cal_pos = cfg.calendar.cal_pos
          
        files_to_ignore = [cfg.main.last_wallpaper_image]
         
        w_setter = wallpaper_setter.WallpaperSetter(
                   '', 
                   cfg.main.dest_file, 
                   wx.Colour(*cfg.main.mask_color),
                   cfg.main.stretch, 
                   cfg.main.keep_aspect_ratio,
                   cfg.calendar.draw_cal,
                   cfg.calendar.appointment_descriptions_of_next_days,
                   util.get_appointment_list(APPOINTMENTS_CONFIG_FILE),
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
                   wx.Colour(*cfg.calendar.cal_appointment_color))
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
                    print 'Es gibt keine gueltige Bilddatei unter den angegeben Dateien / Verzeichnissen.'
                    wx.MessageDialog(None, 'Es gibt keine gueltige Bilddatei unter den angegeben Dateien / Verzeichnissen.',
                                     'Fehler:', wx.OK | wx.CENTRE).ShowModal()
                    sys.exit(1)