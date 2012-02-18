import math
import random
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


if __name__ == '__main__':
    class TestFrame(wx.Frame):
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, *args, **kwargs)
            
            self.main_panel = wx.Panel(self, -1)
            
            self.main_panel.Bind(wx.EVT_PAINT, self.on_paint)
            
            self.Centre()
            self.Show()
            
            
        def on_paint(self, event):
            dc = wx.GCDC(wx.PaintDC(self.main_panel))
            
            dc.DrawRectangle(100, 100, 50, 50)
            draw_doted_spiral(dc, (125, 125), 15, 5, -85, 400, 10, lambda x: (x-1)**2)
            
            event.Skip()
            
    app = wx.PySimpleApp()
    frame = TestFrame(None, -1, size=(500, 500))
    app.MainLoop()