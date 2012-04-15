#coding: utf-8

import math
import random
import time
import wx

SECTION_LENGTH = 1          # gibt an, wie gross die Teilstrecken beim Ablaufen der Spiralen sein sollen (in Pixel)
RADIUS_STEP = 1             # gibt an, mit welcher Pixelaufloesung die Radii abgegangen werden

def draw_doted_spiral(dc, central_point, inner_radius, outer_radius, start_angle, total_angle, width, probability_function):
    '''
    Zeichnet eine Spirale, welche nach aussen gepunktet auslaeuft. probability_function ist im Bereich 0 bis 1 definiert, wobei 
    0 der senkrechten Mitte zwischen den beiden Aussenraendern und 1 dem Aussenrand entspricht. Sie liefert eine Wahrscheinlichkeit,
    mit der ein bestimmter Punkt der Spirale gezeichnet werden soll.
    Winkel werden in Grad angegeben.
    '''
    r_offset = -width/2.0
    while r_offset <= width/2.0:
        # Strecken werden ueber Kreisstrecken angenaehert
        average_radius = (inner_radius + outer_radius) / 2.0 + r_offset
        distance = (total_angle / 360.0) * 2 * math.pi * average_radius
        n = distance / SECTION_LENGTH
        angle_step = 1.0 * total_angle / n
        
        probility_input = abs(r_offset) / (width/2.0)
        current_probability = probability_function(probility_input)
        random_function = lambda: random.random() < current_probability
        
        current_angle = start_angle
        while current_angle <= start_angle + total_angle:
            if random_function():
                current_r = inner_radius + r_offset + 1.0 * (outer_radius-inner_radius) * (current_angle-start_angle) / total_angle
                x = current_r * math.cos(current_angle * math.pi / 180) + central_point[0]
                y = current_r * math.sin(current_angle * math.pi / 180) + central_point[1]
                dc.DrawPoint(x, y)
            current_angle += RADIUS_STEP
        r_offset += RADIUS_STEP


MEMO_INDENTION = 2  # spaces
MEMO_BORDER = 5     # pixels
WEEKDAYS = ('Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So')
def draw_memo(dc, pos_tuple, size_tuple, bg_colors, sorted_appointment_list):
    '''
    Zeichnet einen Notizzettel, auf dem die uebergebenen Termine der appointment_list eingetragen werden.
    Dabei werden nur so viele  Termine eingetragen, wie der verfuegbare Platz zulaesst. Sollten Termine nicht
    eingetragen werden koennen, so wird dies am Ende des Notizzettels mit einem Eintrag der Art [x weitere]
    kenntlich gemacht. Der letzte Termin kann evtl. gekuerzt sein, doch dies wird auch mit [...] angezeigt.
    '''
    
    def fit_line(line, width):
        '''
        Schneidet eine Zeile solange hinten ab, bis sie mit Fuellung ('...') die Breitenangebe erfuellt.
        Sollte die Zeile schon so diese Angabe erfuellen, wird der String unveraendert zurueckgegeben.
        '''
        
        if dc.GetTextExtent(line)[0] <= width:
            return line
        else:
            next_pos = len(line)
            while next_pos > 0 and dc.GetTextExtent(line[:next_pos] + '...')[0] > width:
                next_pos -= 1
            return line[:next_pos] + '...'
    
    def get_day_lines(day):
        '''
        Liefert einen vollstaendigen Tageseintrag als Liste von Zeilen
        '''
        date = day[0]
        date_string = ''.join(['%02d'%date[2], '.', '%02d'%date[1], '.', '%04d'%date[0]])
        day_lines = [fit_line(''.join([WEEKDAYS[time.strptime(date_string, '%d.%m.%Y').tm_wday], ', ', date_string]), size_tuple[0] - 2*MEMO_BORDER - dc.GetTextExtent(':')[0]) + ':\n']
        for entry in day[1:]:
            day_lines.append(MEMO_INDENTION*' ' + fit_line(entry, size_tuple[0] - 2*MEMO_BORDER - dc.GetTextExtent(MEMO_INDENTION*' ')[0]) + '\n')
            
        return day_lines
    
    
    dc.GradientFillLinear(wx.Rect(0, 0, size_tuple[0], size_tuple[1]), bg_colors[0], bg_colors[1], wx.DOWN)
    
    memo_string = ''
    # Zunaechst ermitteln, wie viele ganze Termine sicher auf den Zettel passen:
    day_number = -1         # Ist nach der Schleife der Index des zulaesst hinzugefuegten Tages zum Memo-String
    for day in sorted_appointment_list:
        day_string = ''.join(get_day_lines(day))[:-1]   # Entferne abschliessendes \n
        if dc.GetMultiLineTextExtent(memo_string + day_string + 
            ('\n[]' if day_number < len(sorted_appointment_list)-2 else ''))[1] <= size_tuple[1]-2*MEMO_BORDER:
            memo_string += day_string + '\n'
        else:
            break
        day_number += 1
    print day_number
    # Falls noch Termine fehlen, so fuege vom naechsten nicht passenden Termin noch so viele Zeilen hinzu, wie moeglich:
    if day_number < len(sorted_appointment_list) - 1:
        day = sorted_appointment_list[day_number+1]
        day_string = ''
        day_lines = get_day_lines(day)
        left_days = len(sorted_appointment_list) - day_number - 2
        for day_line in day_lines:
            if dc.GetMultiLineTextExtent(memo_string + day_string + day_line + 
                '[]' + ('\n[]' if left_days > 0 else ''))[1] <= size_tuple[1]-2*MEMO_BORDER:
                day_string += day_line
            else:
                break
        if day_string != '':
            memo_string += ''.join([day_string, MEMO_INDENTION*' ', '[...]\n'])
        else:
            left_days += 1
        if left_days > 0:
            if left_days < len(sorted_appointment_list):
                memo_string += ''.join(['[', str(left_days), ' weitere', 
                                        'r]' if left_days == 1 else ']'])
            else:
                memo_string += ''.join(['[', str(left_days), ' Eintrag]' if left_days == 1 else ' Einträge]'])
        
    # Memo-String zeichnen
    dc.DrawLabel(memo_string, wx.Rect(MEMO_BORDER, MEMO_BORDER, size_tuple[0]-MEMO_BORDER, size_tuple[1]-MEMO_BORDER))

