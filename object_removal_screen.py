# Programmed by "Huzefa Ali Asgar"

from pydoc import TextRepr
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import cv2
import numpy as np
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooserListView

class ObjectRemovalScreen(Screen):
    def __init__(self, **kwargs):
        super(ObjectRemovalScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        heading = Label(text="Object Removal Page", font_size=24)
        back_button = Button(text='Back to Main Page', on_press=self.go_back_to_main_page)
        self.filechooser = FileChooserListView(on_selection=self.selected)
        process_button = Button(text="Process Image", on_press=self.process_image)

        layout.add_widget(heading)
        layout.add_widget(self.filechooser)
        layout.add_widget(process_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def selected(self, selection):
        # Handle the file selection here
        if selection:
            self.selected_image = selection[0]

    def detect_objects(self, image):
        (h, w) = image.shape[:2]
        # Convert the image to a blob for the neural network
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

        # Pass the blob through the network and obtain the detections and predictions
        self.net.setInput(blob)
        detections = self.net.forward()

        # We'll assume the first detected object is the one we want to remove
        # This is a simplification and in a real application you would use additional logic
        # to decide which objects to remove
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:  # Confidence threshold
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # We create a mask for the detected object
                mask = np.zeros(image.shape[:2], dtype=np.uint8)
                mask[startY:endY, startX:endX] = 255
                return mask

        # If no objects were detected, return an empty mask
        return np.zeros(image.shape[:2], dtype=np.uint8)

    def process_image(self, instance):
        # Check if an image is selected
        if not hasattr(self, 'selected_image'):
            popup = Popup(title='Error', content=Label(text='No image selected!'),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return
        
        # Read the image
        image = cv2.imread(self.selected_image)
        
        # Check if the image is loaded properly
        if image is None:
            popup = Popup(title='Error', content=Label(text='Failed to load image!'),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return
        
        # Detect objects in the image
        mask = self.detect_objects(image)
        
        # Perform inpainting
        inpainted_image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
        
        # Save the inpainted image to a file or update the UI with the new image
        cv2.imwrite('/Users/huz/Desktop/Computer_Photography_Group_Project/elephant_balloon_removed.jpg', inpainted_image)
        
        # Update the UI to display the new image
        # Assuming you have an Image widget to display the result
        self.display_result(inpainted_image)

    def display_result(self, inpainted_image):
        # Convert the image to texture
        buffer = cv2.flip(inpainted_image, 0).tostring()
        texture = TextRepr.create(size=(inpainted_image.shape[1], inpainted_image.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        
        # Create an image widget to display the texture
        image_widget = Image()
        image_widget.texture = texture
        
        # Display the image in a popup
        popup = Popup(title="Inpainted Image", content=image_widget,
                      size_hint=(None, None), size=(Window.width, Window.height))
        popup.open()
    

    def go_back_to_main_page(self, instance):
        self.manager.current = 'home'


