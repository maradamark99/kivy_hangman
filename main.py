from kivy.app import App
from string import ascii_lowercase
import requests
import re

from kivy.graphics import Line, Ellipse
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.config import Config

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'width', '1280')
Config.write()

# index of the drawing phase
index = 0
# half of the screen width
half_x = 640
# half of the screen height
half_y = 360


class MyLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

        self.drawing = [
            Line(points=[half_x - 50, half_y, half_x + 50, half_y]),
            Line(points=[half_x, half_y, half_x, half_y + 100]),
            Line(points=[half_x, half_y + 100, half_x + 100, half_y + 100]),
            Line(points=[half_x + 100, half_y + 100, half_x + 100, half_y + 70]),
            Ellipse(pos=(half_x + 92.5, half_y + 57.5), size=(15, 15)),
            Line(points=[half_x + 100, half_y + 57.5, half_x + 100, half_y + 35]),
            Line(points=[half_x + 100, half_y + 57.5, half_x + 85, half_y + 45]),
            Line(points=[half_x + 100, half_y + 57.5, half_x + 115, half_y + 45]),
            Line(points=[half_x + 100, half_y + 35, half_x + 105, half_y + 20]),
            Line(points=[half_x + 100, half_y + 35, half_x + 95, half_y + 20])
        ]

        url = "https://random-word-api.herokuapp.com/word?number=1"
        r = requests.get(url)
        self.data = r.json()
        self.data = str(self.data).translate({ord(i): None for i in '[]\'\''})

        self.word = ""
        for i in range(0, len(self.data)):
            self.word += "_"
        print(self.data)

        self.label = Label(text=self.word, font_size=36)

        self.rows = 2
        self.add_widget(self.label)

        stack_layout = StackLayout(size_hint_y = .75)
        self.add_widget(stack_layout)
        buttons = []

        for c in ascii_lowercase:
            btn = Button(text=c,size_hint=(.1,.1))
            btn.bind(on_press=self.callback)
            buttons.append(btn)
            stack_layout.add_widget(btn)

    def callback(self, instance):
        global index
        if self.word == self.data:
            self.canvas.clear()
            self.clear_widgets()
            self.add_widget(Label(text="You guessed it!", font_size=48, color=(0,1,0)))
            return
        if index == len(self.drawing)-1:
            self.canvas.clear()
            self.clear_widgets()
            self.add_widget(Label(text="Game Over!", font_size=48, color=(1,0,0)))
            return

        indexes = [x.start() for x in re.finditer(instance.text, self.data)]
        print(indexes)
        if indexes:
            for i in indexes:
                self.word = self.word[:i] + instance.text + self.word[i+1:]
            self.label.text = self.word
        else:
            with self.canvas:
                if hasattr(self.drawing[index], 'points'):
                    Line(points = self.drawing[index].points)
                else:
                    Ellipse(pos= self.drawing[index].pos, size= self.drawing[index].size)
                index += 1
        instance.disabled = True


class HangMan(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    HangMan().run()
