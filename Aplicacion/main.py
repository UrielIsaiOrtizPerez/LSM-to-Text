from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemLabel,
    MDNavigationItemIcon,
)
from kivymd.app import MDApp
from audio import CustomVoz
from detector import CustomCamera
import cv2

class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))

class BaseScreen(MDScreen):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(content)

class Comunicador(MDApp):
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        self.root.get_ids().screen_manager.current = item_text
        
    def build(self):
        custom_voz = CustomVoz()
        custom_camara = CustomCamera()

        return MDBoxLayout(
            MDScreenManager(
                BaseScreen(
                    content=custom_camara,
                    name="Camera",
                ),
                BaseScreen(
                    content=custom_voz,
                    name="Voice",
                ),
                id="screen_manager",
            ),
            MDNavigationBar(
                BaseMDNavigationItem(
                    icon="camera",
                    text="Camera",
                    active=True,
                ),
                BaseMDNavigationItem(
                    icon="microphone",
                    text="Voice",
                ),
                on_switch_tabs=self.on_switch_tabs,
            ),
            orientation="vertical",
            md_bg_color=self.theme_cls.backgroundColor,
        )
    
    def on_stop(self):
        cerrar = CustomCamera()
        cerrar.stop(self)

Comunicador().run()
