import wx
from util import config, section, util
from setter import wallpaper_setter


MAIN_CONFIG =              'main_config.cfg'
PATH_LIST_FILE =           'path_list.cfg'
FILE_PICKER_CONFIG_FILE =  'file_picker.cfg'
PASSED_DAYS_CONFIG_FILE =  'passed_days.cfg'
APPOINTMENTS_CONFIG_FILE = 'appointments.cfg'
DAY_THRESHOLD = 1       # Anzahl der Tage, die mindestens vergangen sein muessen, damit das Hintergrundbild aktualisiert wird

FILE_TYPE_LIST = ['.bmp', '.jpg', '.jpeg', '.png']

# cal_pos_X == -1 bedeutet, dass cal_pos_Y die Position des Kalenders per Konstante angibt
STD_CONFIG = {'main':      {'dest_file': 'wallpaper.bmp', 'mask_color': (0, 0, 0), 'stretch': False, 'keep_aspect_ratio': True,
                            'last_wallpaper_image': ''},
              'calendar' : {'draw_cal': False, 'appointment_descriptions_of_next_days': 7,
                            'cal_pos': (-1.0, wallpaper_setter.CAL_BOTTOM_RIGHT),
                            'cal_size': (0.25, 0.25), 'cal_alpha': 153,
                            'cal_heading_font_desc': 'Arial 10',
                            'cal_wday_font_desc': 'Arial 10',
                            'cal_mday_font_desc': 'Arial 10',
                            'cal_font_color': (255, 255, 255),
                            'cal_sunday_font_color': (255, 0, 0),
                            'cal_line_color': (255, 255, 255),
                            'cal_day_color1': (255, 128, 0),
                            'cal_day_color2': (255, 128, 0),
                            'cal_background_color1': (0, 3, 153),
                            'cal_background_color2': (59, 136, 242),
                            'cal_appointment_color': (245, 229, 43)}
              }

              
def get_config_parser():
    return config.Config(MAIN_CONFIG, STD_CONFIG)