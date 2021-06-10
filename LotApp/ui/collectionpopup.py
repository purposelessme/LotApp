from kivy.app import App
from kivy.lang import Builder
from kivy.uix.modalview import ModalView

from logics.db import Db

Builder.load_string(
    """
<CollectionPopUp>:
    auto_dismiss:True
    size_hint:0.3,0.2
    BoxLayout:
        orientation:"vertical"
        TextInput:
            id:name
            multiline:False
        Button:
            text:"CREATE"
            on_press:
                root.create(name.text)
                name.text = ""
"""
)


class CollectionPopUp(ModalView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ""

    def create(self, name):
        if App.get_running_app().root.current == "home":
            self.collection(name)
            return
        self.lot(name)

    def collection(self, name):
        Db.create_db(name)
        self.dismiss()
        App.get_running_app().cur_collection = name
        App.get_running_app().root.current = "collection"

    def lot(self, field):
        Db.add_entry(App.get_running_app().cur_collection, field)
        self.dismiss()
        App.get_running_app().cur_lot = field
        App.get_running_app().root.current = "lotScreen"
