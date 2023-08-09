from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager
from android_permissions import AndroidPermissions

from homelayout import HomeScreen0
from applayout import AppLayout


if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity
    View = autoclass('android.view.View')

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread 
        # so use Window.width and Window.height
        if Window.width > Window.height:
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar 
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
elif platform != 'ios':
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config 
    Config.set('input', 'mouse', 'mouse, disable_multitouch')


class MyApp(App):
    
    def build(self):
        self.enable_swipe = False
        self.sm = ScreenManager()
        self.screens = [
            HomeScreen0(name='home'),
            AppLayout(name='applayout')]
        
        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)

        for screen in self.screens:
            self.sm.add_widget(screen)
            
        self.sm.current = 'home'  # Set the initial screen to 'home'
        
        return self.sm

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None
        self.enable_swipe = True
        # Can't connect camera till after on_start()
        Clock.schedule_once(self.connect_camera)

    def swipe_screen(self, right):
        if self.enable_swipe:
            if right:
                self.sm.transition.direction = 'right'
                self.sm.current = 'home'
            else:
                self.sm.transition.direction = 'left'
                self.sm.current = 'applayout'

    def connect_camera(self, dt):
        opencv_screen = self.sm.get_screen('applayout')
        opencv_screen.connect_camera(analyze_pixels_resolution=720,
                                      enable_analyze_pixels=True,
                                      enable_video=False)

    def on_stop(self):
        opencv_screen = self.sm.get_screen('applayout')
        opencv_screen.disconnect_camera()


MyApp().run()
