from kivy.app import App
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
import requests


# Window.size = (200, 200)
# Config.set('graphics', 'width', '200')
# Config.set('graphics', 'height', '200')

API_ENDPOINT = "127.0.0.1:8180"
MAX_ITER = 20

class Pixel(Widget):
    def __init__(self, request_parms, position, size, **kwargs):
        self.request_parms = request_parms
        self.position = position
        self.pixel_size = size
        super(Pixel, self).__init__(**kwargs)

        r = requests.get(f'http://{API_ENDPOINT}?complex_r={self.request_parms[0]}&complex_i={self.request_parms[1]}&iter={MAX_ITER}')
        self.color = abs(1-(r.json()["response"]/MAX_ITER))
        print(r.json())
        # Arranging Canvas
        with self.canvas:
            Color(self.color, 0, 0)  # set the colour
            # Setting the size and position of canvas
            self.rect = Rectangle(pos = self.position, size=(self.pixel_size, self.pixel_size))
 
    #         # Update the canvas as the screen size change
    #         self.bind(pos = self.update_rect,
    #               size = self.update_rect)

    #     # update function which makes the canvas adjustable.
    # def update_rect(self, *args):
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size

class Grid(Widget):
    cols = NumericProperty(800)
    rows = NumericProperty(400)
    pixel_size = NumericProperty(5)
    zoom = NumericProperty(1)

    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)

        with self.canvas:
            layout = GridLayout(cols=self.cols, rows=self.rows)

            for i in range(0, self.cols, self.pixel_size):
                for j in range(0, self.rows, self.pixel_size):
                    layout.add_widget(Pixel((((i/self.cols)*4)-2, ((j/self.rows)*2)-1), (i, j), self.pixel_size))
 

class MandelbrotView(Widget):
    def build(self):
        pass

class MandelbrotApp(App):
    def build(self):
        parent = Widget()

        parent.add_widget(Grid())
        return parent


if __name__ == '__main__':
    MandelbrotApp().run()