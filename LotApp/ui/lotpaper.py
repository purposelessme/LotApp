from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button

Builder.load_string(
    """
#:import Db logics.db.Db
<LotPaper>:
    text:self.name
    bold:True
    font_size:"30sp"
    size_hint:0.5,0.5
    on_press:
        app.selected_numbers.append(self.index)
        Db.add_selected(self.index,app.cur_lot,app.cur_collection)
    """
)


class LotPaper(Button):
    index = StringProperty()
    name = StringProperty()

    def __init__(self, index, name, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.name = name
