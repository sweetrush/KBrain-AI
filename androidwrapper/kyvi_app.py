from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.graphics import Color, Rectangle
Window.clearcolor = (1, 1, 1, 1)

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET])

from webview import WebView

# Define the layout of the app
KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        MDTextField:
            id: url_input
            hint_text: 'Enter URL'
            size_hint_y: None
            height: '48dp'

        Button:
            text: 'Load URL'
            on_release: app.load_url(url_input.text)
            size_hint_y: None
            height: '48dp'

        WebView:
            id: webview
'''

class MainScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        # Load the KV string
        return Builder.load_string(KV)

    def load_url(self, url):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        webview = self.root.get_screen('main').ids.webview
        webview.load_url(url)

if __name__ == '__main__':
    MyApp().run()