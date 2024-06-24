from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
import speech_recognition as sr

class CustomVoz(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding=(0,0,0,20)
        self.pos_hint = {'center_x':0.5}
        self.lbPresiona = MDLabel(text="Presiona el botón para hablar", halign='center')
        self.btnActivate = MDIconButton(
            icon='microphone',
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.iniciar_escucha
        )
        self.recognizer = sr.Recognizer()
        self.add_widget(self.lbPresiona)
        self.add_widget(self.btnActivate)

    def iniciar_escucha(self, instance):
        try:
            self.lbPresiona.text = "Escuchando..."
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source)
            texto = self.recognizer.recognize_google(audio, language="es-ES")
            self.lbPresiona.text = texto
        except sr.UnknownValueError:
            self.lbPresiona.text = "No se pudo entender la voz"
        except sr.RequestError:
            self.lbPresiona.text = "Error en la solicitud"
