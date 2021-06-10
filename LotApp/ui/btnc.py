from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button

Builder.load_string(
    """
<BtnC>:
    on_press:
        self.add_name(self.text)
    """
)


class BtnC(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def add_name(name):
        App.get_running_app().cur_collection = name
        App.get_running_app().root.current = "collection"


Builder.load_string(
    """
<BtnL>:
    on_press:
        self.add_name(self.text)
    """
)


class BtnL(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def add_name(name):
        App.get_running_app().cur_lot = name
        App.get_running_app().root.current = "lotScreen"
