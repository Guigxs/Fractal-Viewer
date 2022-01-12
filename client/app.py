from kivy.app import App
from kivy.app import async_runTouchApp
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
import requests
import time, threading


Window.size = (900, 900)

API_ENDPOINT = "127.0.0.1:8180"

def inter_1d(pos, min, max):
    return min + pos * (max - min)


class Pixel(Widget):
    max_iter = NumericProperty()
    def __init__(self, request_parms, position, size, **kwargs):
        self.request_parms = request_parms
        self.position = position
        self.pixel_size = size
        super(Pixel, self).__init__(**kwargs)

        r = requests.get(f'http://{API_ENDPOINT}?complex_r={self.request_parms[0]}&complex_i={self.request_parms[1]}&iter={self.max_iter}')
        self.color = abs(1-(r.json()["response"]/self.max_iter))
        
        # Arranging Canvas
        with self.canvas:
            Color(self.color, 0, 0)  # set the colour
            # Setting the size and position of canvas
            self.rect = Rectangle(pos = self.position, size=(self.pixel_size, self.pixel_size))

class Grid(Widget):
    width = NumericProperty(800)
    height = NumericProperty(800)

    start_x = NumericProperty(-2)
    end_x = NumericProperty(1)
    start_y = NumericProperty(-1.5)
    end_y = NumericProperty(1.5)
    start_cols = NumericProperty(0)
    cols = NumericProperty(800)
    start_rows = NumericProperty(0)
    rows = NumericProperty(800)
    pixel_size = NumericProperty(100)
    zoom = NumericProperty(1)

    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.build()
        
        
    def build(self, monitor=False):
        
        start = time.time()
        with self.canvas:
            layout = GridLayout(cols=self.cols, rows=self.rows)

            for i in range(self.start_cols, self.cols, self.pixel_size):
                for j in range(self.start_rows, self.rows, self.pixel_size):
                    real_values = (inter_1d(i/self.cols, self.start_x, self.end_x), inter_1d(j/self.rows, self.start_y, self.end_y))
                    graph_values = (i, j)

                    layout.add_widget(Pixel(real_values, graph_values, self.pixel_size))
                
                if (monitor):
                    App.get_running_app().pop_up.update_value(i/(self.cols))

        print(f"Widget ({self.width}, {self.height}) built in x : [{self.start_x}...{self.end_x}] y : [{self.start_y}...{self.end_y}] with pixel size = {self.pixel_size} in {round(time.time() - start, 2)}s")

    def refresh(self):
        self.build(monitor=True)
        App.get_running_app().dismiss_popup()


class PopupBox(Popup):
    pop_up_text = ObjectProperty()
    loading_value = ObjectProperty()

    def update_pop_up_text(self, p_message):
        self.pop_up_text.text = p_message

    def update_value(self, value):
        self.loading_value.value = value*100

class MandelbrotApp(App):
    zoom = NumericProperty(1)

    def dismiss_popup(self):
        self.pop_up.dismiss()

    def show_popup(self):
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text('Rebuilding the area, please wait...')
        self.pop_up.open()

    def add(self, val):
        self.show_popup()

        self.grid.pixel_size = int(self.grid.pixel_size * 2)
        self.pixel_size.text = f"Pixel size: {self.grid.pixel_size}"

        mythread = threading.Thread(target=self.grid.refresh)
        mythread.start()

    def sub(self, val):
        self.show_popup()

        self.grid.pixel_size = int(self.grid.pixel_size / 2)
        self.pixel_size.text = f"Pixel size: {self.grid.pixel_size}"

        mythread = threading.Thread(target=self.grid.refresh)
        mythread.start()

    def change_coord(self, val):
        self.show_popup()

        self.grid.start_x = float(self.x0_input.text)
        self.grid.end_x = float(self.x1_input.text)
        self.grid.start_y = float(self.y0_input.text)
        self.grid.end_y = float(self.y1_input.text)

        mythread = threading.Thread(target=self.grid.refresh)
        mythread.start()

    def build(self):
        parent = Widget()

        self.grid = Grid()
        self.pixel_size = Label(text=f"Pixel size: {self.grid.pixel_size}", pos= (100, 800),)
        self.label = Label(text=f"To:", pos= (800, 500), font_size=40)
        self.x0_input = TextInput(hint_text='x0', multiline=False, pos=(800, 400), font_size=40, halign="center")
        self.x1_input = TextInput(hint_text='x1', multiline=False, pos=(800, 300), font_size=40, halign="center")
        self.y0_input = TextInput(hint_text='y0', multiline=False, pos=(800, 200), font_size=40, halign="center")
        self.y1_input = TextInput(hint_text='y1', multiline=False, pos=(800, 100), font_size=40, halign="center", line_height=10)
        self.button_go = Button(text='GO', pos=(800, 0), on_press=self.change_coord, font_size=40)
        
        parent.add_widget(self.grid)
        parent.add_widget(Button(text="+", pos=(0, 800), on_press=self.add, font_size=50))
        parent.add_widget(self.pixel_size)
        parent.add_widget(Button(text="-", pos= (200, 800), on_press=self.sub, font_size=50))
        parent.add_widget(self.x0_input)
        parent.add_widget(self.x1_input)
        parent.add_widget(self.y0_input)
        parent.add_widget(self.y1_input)
        parent.add_widget(self.button_go)
        parent.add_widget(self.label)

        return parent


if __name__ == '__main__':
    MandelbrotApp().run()