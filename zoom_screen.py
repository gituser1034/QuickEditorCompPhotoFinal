# Olly Love 
# Allows user to zoom into a portion of an image
# Image buttons and zoomed portion should change in program but they don't
# even though the png files are changing

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from PIL import Image as PILImage 
from kivy.uix.label import Label
import cv2
import numpy as np
from load_image_zoom import create_image_buttons
from functools import partial

class ZoomScreen(Screen):
    def __init__(self, **kwargs):
        super(ZoomScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=2)
        self.default_image = Image(source='elephant_balloon.jpg', size_hint=(None, None), 
                                   height = 300, width = 700, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.default_image)

        load_label = Label(text='Choose a quadrant below to Zoom in', size_hint=(None, None), height = 20, width = 400)
        layout.add_widget(load_label)

        layout2 = GridLayout(cols=2, rows=3, padding=10, spacing=1, cols_minimum={0: 90, 1: 90}, 
                             rows_minimum={0: 100, 1: 100})

        top_left, top_right, bottom_left, bottom_right, new_dimensions = self.get_image_buttons(layout)
        
        # These made up of image quadrants, pressing this allows a portion of an image to be zoomed into
        self.image_button_top_left = Button(background_normal='top_left.png', 
                                            on_press=partial(self.nearest_neighbor_zoom, 
                                                             small_image = top_left, 
                                                             new_dimensions=new_dimensions))
        self.image_button_top_right = Button(background_normal='top_right.png', 
                                             on_press=partial(self.nearest_neighbor_zoom, 
                                                              small_image = top_right, 
                                                              new_dimensions=new_dimensions))
        self.image_button_bottom_left = Button(background_normal='bottom_left.png', 
                                               on_press=partial(self.nearest_neighbor_zoom, 
                                                                small_image = bottom_left, 
                                                                new_dimensions=new_dimensions))
        self.image_button_bottom_right = Button(background_normal='bottom_right.png', 
                                                on_press=partial(self.nearest_neighbor_zoom, 
                                                                 small_image = bottom_right, 
                                                                 new_dimensions=new_dimensions))
        
        # Add buttons to grid
        layout2.add_widget(self.image_button_top_left)
        layout2.add_widget(self.image_button_top_right)
        layout2.add_widget(self.image_button_bottom_left)
        layout2.add_widget(self.image_button_bottom_right)
        layout.add_widget(layout2)

        # Enter image path, load image, back to main widgets
        self.load_textfield = TextInput(multiline=False, size_hint=(None, None), height = 30, width = 300, 
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.load_textfield)

        load_button = Button(text='Load Images', on_press=partial(self.load_images, layout=layout), 
                             size_hint=(None, None), height = 30, width = 300, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(load_button)
        
        back_button = Button(text='Back to Main Page', on_press=self.go_back_to_main_page, 
                             size_hint=(None, None), height = 30, width = 300, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(back_button)

        self.add_widget(layout)

    # Load image buttons with code from load_image_zoom.py
    def get_image_buttons(self, layout):
        return create_image_buttons(self, layout)
    
    # Loads image and should refresh buttons
    def load_images(self, instance, layout):
        image_path = self.load_textfield.text
        self.default_image.source = image_path
        print(image_path)
        self.get_image_buttons(layout)

    # Takes image portion and new dimensions of the original image size
    # through interpolation make portion that image size
    def nearest_neighbor_zoom(self, instance, small_image, new_dimensions):
        old_h, old_w, _ = small_image.shape
        new_h, new_w, _ = new_dimensions
        zoomed_in = np.ones((new_h,new_w,3))
        # step size between rows and columns, can be decimal
        row_step = (old_h - 1) / (new_h - 1)
        col_step = (old_w - 1) / (new_w - 1)
        # increments to track rows and columns
        r_incr = 0
        c_incr = 0
        # indices for new array
        i = 0
        j = 0

        # While within height of the new image, iterate over indices in image to be resized, rounding to
        # nearest pixel, increment steps based on nn logic
        # increment row and repeat when on last column
        while i < new_h: 
            zoomed_in[i,j,:] = small_image[self.correct_round(r_incr), self.correct_round(c_incr), :]
            c_incr = c_incr + col_step
            j+=1
            if (j == new_w):
                r_incr = r_incr + row_step
                i+=1
                j=0
                c_incr = 0

        cv2.imwrite('zoomed.png', zoomed_in)
        self.default_image.source = 'zoomed.png'
    
    # Accounting for pythons rounding down to 0 when something is 0.5
    # values with .5 should round up
    def correct_round(self, value):
        if value % 1 == 0.5:
            return int(value + 0.5)
        else:
            return int(round(value))

    def go_back_to_main_page(self, instance):
        self.manager.current = 'home'
