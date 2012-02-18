import os
import random

from util import util

class RandomFilePicker:
    def __init__(self, path_list, file_type_list, config_file):
        self.file_list = []
        self.path_list = path_list
        self.file_type_list = file_type_list
        self.config_file = config_file
        self.current_file = ''
        
        # Ist die Config-Datei vorhanden, so nimm die Dateien, die in ihr stehen:
        if os.path.isfile(self.config_file):
            self.file_list = get_file_list_from_file(self.config_file)
        if not self.file_list:
            self.file_list = path_list2file_list('', self.path_list, self.file_type_list)
    
    def get_current_file(self):
        return self.current_file
    
    def get_next_file(self, files_to_ignore=[]):
        
        got_new_file_list = False
        count_ignored_files = self.__get_count_ignored_files(files_to_ignore)
        while True:
            # Die Dateiliste muss neu aufgebaut werden:
            if len(self.file_list) - count_ignored_files == 0:
                if got_new_file_list:       # Die Datenliste wurde schon mal in diesem Aufruf neu aufgebaut
                    raise NoValidEntryError('File list contains no valid entries.')
                self.file_list = path_list2file_list('', self.path_list, self.file_type_list)
                if not self.file_list:
                    raise NoValidEntryError('File list contains no entries at all.')
                count_ignored_files = self.__get_count_ignored_files(files_to_ignore)
                got_new_file_list = True
            random_number = random.randint(0, len(self.file_list)-1)
            file_name = self.file_list[random_number]
            if os.path.isfile(file_name) and file_name not in files_to_ignore:
                break
            if file_name not in files_to_ignore:
                del self.file_list[random_number]
            file_name = ''
            
        del self.file_list[random_number]
        self.current_file = file_name
        return file_name
    
    def __get_count_ignored_files(self, files_to_ignore):
        '''
        Ueberprueft, wie viele der zu ignorierenden Dateien sich in der Dateliste befinden
        '''
        
        count = 0
        for file in files_to_ignore:
            if file in self.file_list:
                count += 1
        return count
        
    def __del__(self):
        with open(self.config_file, 'w') as f:
            for file in self.file_list:
                f.write(file + '\n')
    
    def __len__(self):
        return len(self.file_list)
    
    
class NoValidEntryError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
    
    
    
def path_list2file_list(base_dir, path_list, file_type_list):
    file_list = []

    if base_dir != '' and base_dir[-1] != util.PATH_DELIM:
        base_dir += util.PATH_DELIM
    for path in path_list:
        try:
            if os.path.isdir(base_dir + path):
                file_list.extend(path_list2file_list(base_dir + path, os.listdir(base_dir + path), file_type_list))
            elif os.path.isfile(base_dir + path):
                # Pruefen, ob diese Datei einem der gewuenschten Typen entspricht:
                for file_type in file_type_list:
                    if path[-len(file_type):].lower() == file_type.lower():
                        file_list.append((base_dir + path).replace(util.PATH_DELIM * 2, util.PATH_DELIM))
        except OSError:
            pass
    
    return file_list

def get_file_list_from_file(config_file):
    file_list = []
    
    with open(config_file, 'r') as f:
        for line in f:
            file_list.append(line.strip())
            
    return file_list
