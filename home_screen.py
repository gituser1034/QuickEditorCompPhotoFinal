# Programmed by "Dewan Mohammad Tasinuzzaman". Navigating to all other pages of the application.

# home_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        heading = Label(text="Computer Photography - Group Project - Fall 2023", font_size=24)
        zoom_button = Button(text="Image Zooming", on_press=self.go_to_zoom_screen)
        panorama_button = Button(text="Panorama Image Maker", on_press=self.go_to_panorama_screen)
        depth_estimation_button = Button(text="Depth Estimation", on_press=self.go_to_depth_estimation_screen)
        object_removal_button = Button(text="Object Removal", on_press=self.go_to_object_removal_screen)

        layout.add_widget(heading)
        layout.add_widget(zoom_button)
        layout.add_widget(panorama_button)
        layout.add_widget(depth_estimation_button)
        layout.add_widget(object_removal_button)

        self.add_widget(layout)

    def go_to_zoom_screen(self, instance):
        self.manager.current = 'zoom'

    def go_to_panorama_screen(self, instance):
        self.manager.current = 'panorama'

    def go_to_depth_estimation_screen(self, instance):
        self.manager.current = 'depth_estimation'

    def go_to_object_removal_screen(self, instance):
        self.manager.current = 'object_removal'
