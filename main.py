# Programmed by "Dewan Mohammad Tasinuzzaman". For overall setup for the application's UI.



from home_screen import HomeScreen
from zoom_screen import ZoomScreen
from panorama_screen import PanoramaScreen
from depth_estimation_screen import DepthEstimationScreen
from object_removal_screen import ObjectRemovalScreen
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ZoomScreen(name='zoom'))
        sm.add_widget(PanoramaScreen(name='panorama'))
        sm.add_widget(DepthEstimationScreen(name='depth_estimation'))
        sm.add_widget(ObjectRemovalScreen(name='object_removal'))
        return sm
    
    def on_start(self):
        self.title = 'Quick Editor'

if __name__ == '__main__':
    MyApp().run()
