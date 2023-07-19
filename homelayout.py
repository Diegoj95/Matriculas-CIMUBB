from kivy.uix.label import Label
from kivy.utils import platform
from textwrap import fill
from swipescreen import SwipeScreen

class HomeScreen0(SwipeScreen):
    
    def __init__(self, **args):
        super().__init__(**args)
        self.label = Label()
        self.add_widget(self.label)

    def on_size(self, *args):

        if platform == 'android': # Android
            text='Aplicación detección de matriculas.\n\n' +\
                fill('Deslizar a la derecha para usar la cámara')        
            
        self.label.text = text
