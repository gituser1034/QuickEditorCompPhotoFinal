# Programmed by "Huzefa Ali Asgar"
import cv2
import numpy as np
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture

class DepthEstimationScreen(Screen):
    def __init__(self, **kwargs):
        super(DepthEstimationScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.heading = Label(text="Depth Estimation Page", font_size=24)
        self.back_button = Button(text="Back to Home", on_press=self.go_back_to_home)
        self.filechooser = FileChooserListView(on_selection=self.selected)
        self.process_button = Button(text="Estimate Depth", on_press=self.estimate_depth)
        self.layout.add_widget(self.heading)
        self.layout.add_widget(self.filechooser)
        self.layout.add_widget(self.process_button)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

    def go_back_to_home(self, instance):
        self.manager.current = 'home'

    def selected(self, filechooser):
        if filechooser.selection:
            self.selected_image = filechooser.selection[0]

    def estimate_depth(self, instance):
        if hasattr(self, 'selected_image'):
            depth_map = self.mock_depth_estimation(self.selected_image)
            self.display_depth_map(depth_map)
        else:
            popup = Popup(title='Error',
                          content=Label(text='No image selected!'),
                          size_hint=(None, None), size=(400, 400))
            popup.open()

    def mock_depth_estimation(self, image_path):
        # Assuming the depth map is a single-channel image with the same width and height as the input
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        depth_map = np.random.rand(image.shape[0], image.shape[1]).astype(np.float32)
        return depth_map

    def display_depth_map(self, depth_map):
        # Normalize the depth map for display
        depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
        depth_map_normalized = np.uint8(depth_map_normalized)
        depth_map_colorized = cv2.applyColorMap(depth_map_normalized, cv2.COLORMAP_JET)
        # Convert to texture
        buffer = cv2.flip(depth_map_colorized, 0).tobytes()
        texture = Texture.create(size=(depth_map_colorized.shape[1], depth_map_colorized.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        # Create an image widget to display the texture
        image_widget = KivyImage()
        image_widget.texture = texture
        # Display the image in a popup
        popup = Popup(title="Estimated Depth Map", content=image_widget,
                      size_hint=(None, None), size=(400, 400))
        popup.open()

