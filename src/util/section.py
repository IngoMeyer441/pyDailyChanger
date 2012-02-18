#coding: utf-8
'''
Created on 16.03.2011

@author: knodt
'''
#from twisted.python.rebuild import __getattr__

class Section(object):
    
    '''
    In der Klasse Section existiert ein Dictionary (Attribut der Klasse) zur Verarbeitung der Variablen (Zuordnung : NameVar -> Wert)
    '''
    
    '''Speichert das Variablendictionary von Hand in dem Attributdictionary, das jede Klasse besitzt'''
    def __init__(self):
        self.__dict__['_attribute']=dict()
    
    '''Methode, die bei einer Zuweisung auf ein Objekt dieser Klasse aufgerufen wird'''
    def __setattr__(self,name,value):
        self._attribute[name]=value
    
    '''Methode, die beim Zugriff auf ein nicht vorhandenes Attribut ausgefuehrt wird'''
    def __getattr__(self,name):
        return self._attribute[name]
    
    '''getter-Methode fuer die in dieser Sektion gespeicherten Variablen'''
    def getValues(self):
        return self._attribute
    

if __name__ == '__main__':
    print 'Soll nicht ausgefuehrt werden!'
