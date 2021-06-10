from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView


class PopButton(Button):

    def __init__(self, num, name, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.num = num
        self.name = name
        self.bind(on_press=self.pop_up)

    def pop_up(self, dt):
        Pop(self.num, self.name).open()


Builder.load_string(
    """
#:import Db logics.db.Db
<Pop>:
    size_hint:(0.2,0.1)
    auto_dismiss:False
    BoxLayout:
        orientation:"vertical"
        Button:
            text:f"remove {root.num}"
            on_press:
                Db.remove_selected(root.num,app.cur_lot,app.cur_collection) if root.num in app.selected_numbers else None
                Db.remove_result(root.name,app.cur_lot,app.cur_collection) if root.name in app.results_list else None
                app.selected_numbers.remove(root.num) if root.num in app.selected_numbers else None
                app.results_list.remove(root.name) if root.name in app.results_list else None
                root.dismiss()
        Button:
            text:"cancel"
            on_press:
                root.dismiss()
    """
)


class Pop(ModalView):
    num = StringProperty()

    def __init__(self, num, name, **kwargs):
        super().__init__(**kwargs)
        self.num = num
        self.name = name
