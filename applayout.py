from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform
from edgedetect import EdgeDetect
from kivy.uix.button import Button
from swipescreen import SwipeScreen

class AppLayout(SwipeScreen):
    edge_detect = ObjectProperty()

    def connect_camera(self, analyze_pixels_resolution, enable_analyze_pixels, enable_video):
        self.edge_detect.connect_camera(analyze_pixels_resolution=analyze_pixels_resolution,
                                            enable_analyze_pixels=enable_analyze_pixels,
                                            enable_video=enable_video)


class ButtonsLayout(RelativeLayout):
    normal_screenshot = StringProperty()
    down_screenshot = StringProperty()
    normal_camera = StringProperty()
    down_camera = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'android':
            self.normal_screenshot = 'icons/cellphone-screenshot_white.png'
            self.down_screenshot = 'icons/cellphone-screenshot_red.png'
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
            self.ids.other.pos_hint = {'center_x': .2, 'center_y': .5}
            self.ids.other.size_hint = (.2, None)
            self.ids.camara.pos_hint = {'center_x': .4, 'center_y': .5}
            self.ids.camara.size_hint = (.2, None)
            self.ids.screen.pos_hint = {'center_x': .6, 'center_y': .5}
            self.ids.screen.size_hint = (.2, None)
        else:
            self.pos = (Window.width * 0.8, 0)
            self.size_hint = (0.2, 1)
            self.ids.other.pos_hint = {'center_x': .5, 'center_y': .7}
            self.ids.other.size_hint = (None, .2)
            self.ids.camara.pos_hint = {'center_x': .5, 'center_y': .5}
            self.ids.camara.size_hint = (None, .2)
            self.ids.screen.pos_hint = {'center_x': .5, 'center_y': .3}
            self.ids.screen.size_hint = (None, .2)

    def screenshot(self):
        self.parent.edge_detect.capture_screenshot()

    def select_camera(self, facing):
        self.parent.edge_detect.select_camera(facing)

        
    def toggle_button_image(self):
        if self.camera_preview_enabled:
            self.camera_preview_enabled = False
            self.edge_detect.disconnect_camera()
        else:
            self.camera_preview_enabled = True
            self.edge_detect.connect_camera(analyze_pixels_resolution=720,
                                        enable_analyze_pixels=True,
                                        enable_video=False)



        


Builder.load_string("""
<AppLayout>:
    edge_detect: self.ids.preview
    EdgeDetect:
        aspect_ratio: '16:9'
        id:preview
    ButtonsLayout:
        id:buttons

<ButtonsLayout>:
    normal_screenshot:
    down_screenshot:
    normal_camera:
    down_camera:
    Button:
        id:other
        on_press: root.select_camera('toggle')
        height: self.width
        width: self.height
        background_normal: 'icons/camera-flip-outline.png'
        background_down: 'icons/camera-flip-outline.png'
    Button:
        id:camara
        on_press: root.toggle_button_image()
        height: self.width
        width: self.height
        background_normal: root.normal_camera
        background_down: root.down_camera
    Button:
        id:screen
        on_press: root.screenshot()
        height: self.width
        width: self.height
        background_normal: root.normal_screenshot
        background_down: root.down_screenshot
""")

