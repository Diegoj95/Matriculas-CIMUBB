from kivy.app import App
from kivy.uix.screenmanager import Screen
from gestures4kivy import CommonGestures

### Para deslizar desde home a la cámara
class SwipeScreen(Screen, CommonGestures):

    def cgb_horizontal_page(self, touch, right):
        App.get_running_app().swipe_screen(right)

