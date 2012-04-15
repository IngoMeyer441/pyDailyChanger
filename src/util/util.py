import wx
import sys
import subprocess
import time
import os.path

if sys.platform.startswith('win'):
    from ctypes import windll
    import win32con
elif sys.platform.startswith('darwin'):
    from appscript import app, mactypes

if sys.platform.startswith('win'):
    PATH_DELIM = '\\'
else:
    PATH_DELIM = '/'

XFCE = 0
UNITY = 1
WIN = 10
MAC = 11
UNKNOWN = -1

linux_desktop_list = {XFCE:  'xfdesktop',
                      UNITY: ''}


def get_path_list(file):
    '''
    Liest eine Pfadliste aus einer Datei und liefert sie als Pythonliste zurueck.
    Die Pfade/Dateien muessen durch Zeilenumbrueche getrennt sein.
    '''
    
    path_list = []
    with open(file, 'r') as f:
        for line in f:
            path_list.append(line.strip().replace(PATH_DELIM * 2, PATH_DELIM))
    return path_list

def get_number_of_passed_days(file):
    '''
    Liefert auf Basis der angegebenen Datei, wie viele Tage seit dem letzten Aufruf der Funktion vergangen sind
    und aktualisiert dann die Datei mit dem aktuellen Zeitstempel.
    '''
    result = None
    if os.path.isfile(file):
        current_time = int(time.time())
        with open(file, 'r') as f:
            file_time = int(f.read())
        # Passe die timestamps vor der Umrechnung in Tage an die lokale Zeitzone an
        result = (current_time - time.timezone + time.localtime(current_time).tm_isdst*3600)/(24*60*60) - (file_time - time.timezone + time.localtime(file_time).tm_isdst*3600)/(24*60*60)
    
    with open(file, 'w') as f:
        f.write(str(int(time.time())))
    
    return result

def get_appointment_list(file):
    '''
    Liest aus einer Datei eine Liste von Termintagen. Ein Termintag umfasst mindestens zwei Zeilen 
    und hat folgendes Format:
    yyyy-mm-dd: \n <whitespace> <Beschreibung zu Termin 1> \n <whitespace> <Beschreibung zu Termin 2> \n ....
    Rueckgabe der Termine geschieht im Format:
    ((yyyy, mm, dd), Beschreibung1, Beschreibung2, ...) und die Listeneintraege sind nach Datumsangaben sortiert.
    Kommentare beginnen mit "#".
    '''
    
    appointment_list = []
    with open(file, 'r') as f:
        within_block = False
        read_date_line_before = False
        date_tuple = (None, )
        current_descs = []
        delim_pos = -1
        for i, line in enumerate(f):
            if not line.startswith('#'):
                within_block = line[0].isspace()
                if not within_block:
                    if read_date_line_before and len(current_descs) > 0:
                        appointment_list.append(tuple([date_tuple] + current_descs))
                    delim_pos = line.find(',')
                    if delim_pos < 0:
                        has_color = False
                        delim_pos = line.find(':')
                        if delim_pos < 0:
                            raise ValueError(': missing in line number %d.' % i)
                    else:
                        has_color = True
                    try:
                        date_tuple =  tuple(map(int, line[:delim_pos].split('-')))
                        if len(date_tuple) != 3:
                            raise ValueError
                    except ValueError:
                        raise ValueError('Invalid date format (line %d).' % i)
                    if has_color:
                        delim2_pos = line.find(':')
                        if delim2_pos < 0:
                            raise ValueError(': missing in line number %d.' % i)
                        color = line[delim_pos+1:delim2_pos].strip().lower()
                        date_tuple = tuple(list(date_tuple) + [color])
                    else:
                        date_tuple = tuple(list(date_tuple) + ['default'])
                    current_descs = []
                    read_date_line_before = True
                else:
                    current_descs.append(line.strip())
                    
        if read_date_line_before and len(current_descs) > 0:
            appointment_list.append(tuple([date_tuple] + current_descs))
    
    # 3-stufige Sortierung: primaer Jahre, sekundaer Monate, tertiaer Tage
    for i in (2, 1, 0):
        appointment_list.sort(key=lambda x: x[0][i])

    return appointment_list

def get_optimal_font_size_and_text_extent(dc, text, rect):
    ''' 
    Findet die Schriftgroesse (Pointsize), mit der der gegebene Text noch so grade in das gegebene
    Rechteck hineinpasst und liefert diese Groesse zurueck
    '''
    
    font = dc.GetFont()
    previous_value = 0
    current_value = 1
    previous_extent = 0
    current_extent = 0
    
    font.SetPointSize(current_value)
    dc.SetFont(font)
    current_extent = dc.GetTextExtent(text)
    while current_extent[0] <= rect[0] and current_extent[1] <= rect[1]:
        previous_value = current_value
        current_value += 1
        font.SetPointSize(current_value)
        dc.SetFont(font)
        previous_extent = current_extent
        current_extent = dc.GetTextExtent(text)
    
    return (previous_value, previous_extent)

def check_desktop_manager():
    
    if   sys.platform.startswith('linux'):
        p = subprocess.Popen(['/bin/ps', '-e'], stdout=subprocess.PIPE)
        processes = p.stdout.read().lower()
        p.communicate()
        for desktop_item in linux_desktop_list.iteritems():
            if desktop_item[1] in processes:
                return desktop_item[0]
        return UNKNOWN
    elif sys.platform.startswith('win'):
        return WIN
    elif sys.platform.startswith('darwin'):
        return MAC
    else:
        return UNKNOWN
    
def set_wallpaper(file):
    '''
    Setzt die angegebene Datei als Hintergrundbild des Systems
    '''
    
    manager = check_desktop_manager()
    if   manager == XFCE:
        # Altes Hintergrundbild loeschen
        subprocess.Popen('xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s'.split(' ') + ['/']).communicate()
        # Neues Bild setzen
        subprocess.Popen('xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s'.split(' ') + [os.path.abspath(file)]).communicate()
    elif manager == UNITY:
        subprocess.Popen('gsettings set org.gnome.desktop.background picture-uri'.split(' ') + ['file://' + os.path.abspath(file)]).communicate()
    elif manager == WIN:
        windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER, 0, file, win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDWININICHANGE)
    elif manager == MAC:
        app('Finder').desktop_picture.set(mactypes.File(file))
        
        
# --- Id-Getter ---
# Der Id-Getter hilft automatisch generierte Ids zu verwalten.
# Die Datenstruktur ist hierbei rekursiv angelegt, Id-Getter koennen
# zur Gruppierung von Komponenten beliebig geschachtelt werden.

class IdGetter(object):
    def __init__(self, id=-1):                      # Alle im Kontruktor gesetzten Attribute muessen per object definiert werden.
        object.__setattr__(self, '_id_dict', {})   # Danach koennen sie normal genutzt werden (wird in __setattr__ korrekt gehandelt).
        if id is None:
            wx.RegisterId(wx.ID_HIGHEST)   # Verhindern, dass Stock-Ids genutzt werden.
            object.__setattr__(self, '_id_value', wx.NewId())
        else:
            object.__setattr__(self, '_id_value', 0)
            self._id_value = id            # Ruft __setattr__ auf und setzt die Id auf reserved.
        
    # Eine eindeutige Id kann erzeugt werden, indem der Id-Getter einfach per "id_getter.window" aufgerufen wird
    # (sofern das window noch nicht in die Verwaltung aufgenommen wurde). Existert "window" schon, so wird dessen
    # schon vorhandene id geliefert.
    def __getattr__(self, window):
        return self.__getitem__(window)
        
    # Ermoeglicht die Id zu einem "window" manuell zu setzen.
    # Das Window wird entfernt, wenn als Id None angegeben wird.
    def __setattr__(self, window, id):
        if window in self.__dict__:   # Handelt es sich um interne Attribute?
            object.__setattr__(self, window, id)
            if(window == '_id_value'):
                wx.RegisterId(id)
        else:
            self.__setitem__(window, id)
        
    # Loescht eine vorhandene Id aus der Liste, z.B. sinnvoll wenn Komponenten zerstoert werden.
    def __delattr__(self, window):
        self.__delitem__(window)
    
    # Liefert aus einem dict von Ids das Element "elem". Aufruf z.B.: id_getter.window[0] -> Element 0, welches window untergeordnet ist.
    # elem kann ein beliebiges Objekt sein und stellt somit eine Verallgemeinerung von id_getter.window dar. id_getter.window und
    # id_getter['window'] sind aequivalent! Werden ints verwendet, so muss die Zaehlung nicht lueckenlos sein.
    def __getitem__(self, elem):
        if not elem in self._id_dict:
            self._id_dict[elem] = IdGetter(None)
        return self._id_dict[elem]
            
    # Setzt die Id eines Elementes des dict neu. Verallgemeinerung von __setattr__.         
    def __setitem__(self, elem, id):
        if id is None:
            self.__delitem__(elem)
        elif elem in self._id_dict:
            self._id_dict[elem]._id_value = id
        else:
            self._id_dict[elem] = IdGetter(id)
          
    # Loescht ein Element aus dem dict. Verallgemeinerung von __delattr__.  
    def __delitem__(self, elem):
        if elem in self._id_dict:
            del self._id_dict[elem]
                
    # (id) ist als Alternative zur Zuweisung angelegt, da Zuweisungen keinen Rueckgabewert liefern koennen.
    # () ohne Uebergabeparameter wird eine Referenz auf die wx-Konponente geliefert, mit der die Id verbunden ist.
    # (window) liefert wie bei () die Referenz zur Id, jedoch wird mit der Suche bei dem parent "window" gestartet.
    # (menu) liefert die id zu einem MenuItem.
    # Bei anderen Typen wird ein TypeError geworfen.
    def __call__(self, id=None):
        if id is None:
            return wx.FindWindowById(self._id_value)
        elif isinstance(id, wx.Window):
            return wx.FindWindowById(self._id_value, id)
        elif isinstance(id, wx.Menu):
            return id.FindItemById(self._id_value)
        elif isinstance(id, int):
            self._id_value = id
            return self._id_value
        else:
            raise TypeError
         
    # Die folgenden Member stellen die wichtigsten dict-Funktionalitaeten zur Verfuegung:
       
    def __contains__(self, elem):
        return elem in self._id_dict
       
    def __len__(self):
        return len(self._id_dict)
       
    def __iter__(self):
        return self._id_dict.iterkeys()
    
    def iterkeys(self):
        return self.__iter__()
    
    def iteritems(self):
        return self._id_dict.iteritems()
        
    def itervalues(self):
        return self._id_dict.itervalues()
            
    def keys(self):
        return self._id_dict.keys()
    
    def items(self):
        return self._id_dict.items()
    
    def values(self):
        return self._id_dict.values()
            
    # Liefert in einem Integerkontext die zu einer Windowkomponente gehoerige Id
    # (kann so z.B. direkt in einem Wx-Kontruktoraufruf verwendet werden).
    def __int__(self):
        return self._id_value
