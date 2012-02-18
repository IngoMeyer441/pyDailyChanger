#coding: utf-8
'''
Created on 16.03.2011

@author: knodt
'''
import section
import convert
import ConfigParser

class Config(object):
    '''
    In der Klasse Konfig existiert ein Dictionary zur Verarbeitung der Sections (Zuordnung : Name -> SectionObj)
    Das Attribut conf ist ein Objekt der Klasse ConfigParser und verwaltet die Aktualisierung des Konfigurationsfiles und den Zugriff auf diesen
    '''
    def __init__(self,dateiname,standard_input={}):
        self.st_inp=standard_input
        self.dateiname=dateiname
        self.sections=dict()
        self.conf = ConfigParser.RawConfigParser()
        self.read_config()
        self.write_config()
        self.save_config()
    
    def read_config(self):
        '''Standardeingabe auslesen aus Dict( Form: Dict in Dict)'''
        if self.st_inp != {}:
            for section,attributes in self.st_inp.iteritems():
                if section not in self.sections:
                    self.register(section)
                for attribute in attributes:
                    self.sections[section].__setattr__(attribute,self.st_inp[section][attribute])

        '''Auslesen der Daten aus der Konfigurationsdatei (Es werden nur die Daten ausgelesen, die schon durch die Standardbelegung beschrieben sind'''
        self.conf.read(self.dateiname)
        if self.st_inp != {}:
            for section, section_items in self.st_inp.iteritems():
                if self.conf.has_section(section):
                    for option, value in section_items.iteritems():
                        if self.conf.has_option(section, option):
                            if   isinstance(value, bool):
                                val = self.conf.getboolean(section, option)
                            elif isinstance(value, int):
                                val = self.conf.getint(section, option)
                            elif isinstance(value, float):
                                val = self.conf.getfloat(section, option)
                            elif isinstance(value, tuple):
                                val = convert.str2tuple(self.conf.get(section, option), type(value[0]))
                            else:
                                val = self.conf.get(section, option)
                            self.sections[section].__setattr__(option,val)
        else:
            for section in self.conf.sections():
                self.register(section)
                for item in self.conf.items(section):
                    self.sections[section].__setattr__(item[0],item[1])
            
    '''Registriert eine neue Sektion im Attribut sections'''                    
    def register(self,name):
        self.sections[name]=section.Section()
    
    
    '''Methode, die beim Zugriff auf ein nicht vorhandenes Attribut ausgefuehrt wird'''
    def __getattr__(self,name):
        return self.sections[name]
    
    '''Schreibt die Sektionen und Variablen aus dem sections Attribut in das conf Attribut'''    
    def write_config(self):
        for section in self.sections:
            if section not in self.conf.sections():
                self.conf.add_section(section)
            for variable in self.sections[section].getValues():
                self.conf.set(section, variable, self.sections[section].getValues()[variable])
    
    '''Speichert die Konfiguration indem sie das moeglicherweise geaenderte conf Attribut in die Datei schreibt'''
    def save_config(self):
        self.write_config()
        f = open(self.dateiname, "wb")
        self.conf.write(f)
        f.close()

    def __del__(self):
        self.write_config()
        self.save_config()
        
if __name__ == '__main__':
    print 'Soll nicht ausgefuehrt werden!'