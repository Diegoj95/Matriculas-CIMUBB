from kivy.clock import mainthread
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
import numpy as np
import cv2
from camera4kivy import Preview

class EdgeDetect(Preview):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzed_texture = None
        self.camera_preview_enabled = True
        self.camera_started = False  # Variable para controlar si la cámara está encendida o apagada

        # Cargar el clasificador haarcascade
        self.plate_cascade = cv2.CascadeClassifier('haarcascade_plate_number.xml')

    ####################################
    # Analyze a Frame - NOT on UI Thread
    ####################################

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
        rgba = np.fromstring(pixels, np.uint8).reshape(image_size[1], image_size[0], 4)

        if self.camera_preview_enabled:
            gray = cv2.cvtColor(rgba, cv2.COLOR_RGBA2GRAY)
            # Detectar placas
            plates = self.detect_plates(gray)
            # Dibujar rectángulos alrededor de las placas detectadas
            annotated_image = self.annotate_plates(rgba, plates)
        else:
            annotated_image = rgba

        pixels = annotated_image.tostring()
        self.make_thread_safe(pixels, image_size)

    def detect_plates(self, gray):
        plates = self.plate_cascade.detectMultiScale(gray, scaleFactor=1.1)
        return plates

    def annotate_plates(self, image, plates):
        annotated_image = image.copy()
        for (x, y, w, h) in plates:
            # Ajustar el grosor y el color del borde del rectángulo
            cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        return annotated_image

    @mainthread
    def make_thread_safe(self, pixels, size):
        if not self.analyzed_texture or self.analyzed_texture.size[0] != size[0] or self.analyzed_texture.size[1] != size[1]:
            self.analyzed_texture = Texture.create(size=size, colorfmt='rgba')
            self.analyzed_texture.flip_vertical()

        if self.camera_connected:
            self.analyzed_texture.blit_buffer(pixels, colorfmt='rgba')
        else:
            self.analyzed_texture = None

    ################################
    # Annotate Screen - on UI Thread
    ################################

    def canvas_instructions_callback(self, texture, tex_size, tex_pos):
        if self.analyzed_texture:
            Color(1, 1, 1, 1)
            Rectangle(texture=self.analyzed_texture, size=tex_size, pos=tex_pos)


    def toggle_camera_preview(self):
        self.camera_preview_enabled = not self.camera_preview_enabled
