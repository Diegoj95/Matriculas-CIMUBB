from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform
from edgedetect import EdgeDetect
from kivy.uix.button import Button
from swipescreen import SwipeScreen
from android.runnable import run_on_ui_thread
from kivymd.app import MDApp
from kivymd.toast import toast




class AppLayout(SwipeScreen):
    edge_detect = ObjectProperty()

    def connect_camera(self, analyze_pixels_resolution, enable_analyze_pixels, enable_video):
        self.edge_detect.connect_camera(analyze_pixels_resolution=analyze_pixels_resolution,
                                            enable_analyze_pixels=enable_analyze_pixels,
                                            enable_video=enable_video)


class ButtonsLayout(RelativeLayout):
    normal_camera = StringProperty()
    down_camera = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'android':
            self.normal_camera = 'icons/camera_white.png'
            self.down_camera = 'icons/camera_red.png'

    def on_size(self, layout, size):
        if platform == 'android':
            self.ids.screen.min_state_time = 0.3
        else:
            self.ids.screen.min_state_time = 1
        if Window.width < Window.height:
            self.pos = (0, 0)
            self.size_hint = (1, 0.2)
            self.ids.screen.pos_hint = {'center_x': .5, 'center_y': .5}
            self.ids.screen.size_hint = (.2, None)
        else:
            self.pos = (Window.width * 0.8, 0)
            self.size_hint = (0.2, 1)
            self.ids.screen.pos_hint = {'center_x': .5, 'center_y': .3}
            self.ids.screen.size_hint = (None, .2)



    def photo(self):
        self.parent.edge_detect.capture_photo()
        toast('Capturando matricula')



Builder.load_string("""
<AppLayout>:
    edge_detect: self.ids.preview
    EdgeDetect:
        aspect_ratio: '16:9'
        id:preview
    ButtonsLayout:
        id:buttons

<ButtonsLayout>:


    Button:
        id:screen
        on_press: root.photo()
        height: self.width
        width: self.height
        background_normal: root.normal_camera
        background_down: root.down_camera
""")

