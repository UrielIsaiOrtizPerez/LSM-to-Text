from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
import cv2
import mediapipe as mp
import numpy as np
import pickle

class CustomCamera(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.video_captura = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.mp_manos = mp.solutions.hands
        self.manos = self.mp_manos.Hands()
        diccionario = pickle.load(open('model.p', 'rb'))
        self.modelo = diccionario['model']
        self.etiquetas = {0:'Hola',1:'Bien',2:'Tu',3:'Mi',4:'Nombre',5:'A',6:'E',7:'I',8:'O',9:'U',10:'L',11:'R',12:'Yo',13:'20'}
        self.detectar = ''
        self.video_image = Image()
        self.video_image.allow_stretch = True
        self.lbtitulo = MDLabel(text='LSM',halign='center',size_hint_y=None,height=100)
        self.lbletra = MDLabel(text='',halign='center',size_hint_y=None,height=100)
        self.add_widget(self.lbtitulo)
        self.add_widget(self.video_image)
        self.add_widget(self.lbletra)
        Clock.schedule_interval(self.update, 1.0 / 40.0)

    def update(self, dt):
        ret, frame = self.video_captura.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = self.manos.process(frame_rgb)

            if res.multi_hand_landmarks:
                for hand_landmarks in res.multi_hand_landmarks:
                    for landmark in hand_landmarks.landmark:
                        height, width, _ = frame.shape
                        cx, cy = int(landmark.x * width), int(landmark.y * height)
                        cv2.circle(frame, (cx, cy), 4, (255, 0, 0), cv2.FILLED)
                        
            if res.multi_hand_landmarks:
                prediccion = self.modelo.predict([np.asarray(self.extract_caracteristicas(res.multi_hand_landmarks[0]))])
                prediccion_letra = self.etiquetas[float(prediccion[0])]
                self.detectar = prediccion_letra
            else:
                self.detectar = ''

            frame = cv2.rotate(frame, cv2.ROTATE_180)
            textura = self.convert_frame(frame)
            self.video_image.texture = textura
            self.lbletra.text = f'{self.detectar}'

    def extract_caracteristicas(self, hand_landmarks):
        datos = []
        for landmark in hand_landmarks.landmark:
            x = landmark.x
            y = landmark.y
            datos.append(x)
            datos.append(y)
        return datos

    def convert_frame(self, frame):
        textura = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        textura.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        return textura
    
    def stop(self, instance):
        self.video_captura.release()
        cv2.destroyAllWindows()