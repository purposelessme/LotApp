import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from logics.db import Db
from logics.fileops import FileOps
from ui.btnc import BtnC, BtnL
from ui.lotpaper import LotPaper
from ui.popbutton import PopButton


class AppManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Home(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        Clock.schedule_once(lambda x: self.add_collections(FileOps.list_files()))

    def add_collections(self, names):
        for j in self.ids["collectionGrid"].children[:]:
            if j.text != "new collection":
                self.ids["collectionGrid"].remove_widget(j)
        for i in names:
            btn = BtnC(text=i)
            self.ids["collectionGrid"].add_widget(btn)


class Collection(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        Clock.schedule_once(lambda x: self.add_collections(Db.list_files(App.get_running_app().cur_collection)))

    def add_collections(self, names):
        for j in self.ids["lotsGrid"].children[:]:
            if j.text != "new lot":
                self.ids["lotsGrid"].remove_widget(j)
        for i in names:
            btn = BtnL(text=i)
            self.ids["lotsGrid"].add_widget(btn)


class LotSpace(Screen):
    participants_list = ListProperty()
    shuffled_list = ListProperty()
    selected_numbers = ListProperty()
    privacy = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        Clock.schedule_once(self.initialize)

    def initialize(self, dt):
        app = App.get_running_app()
        self.ids["lotName"].text = app.cur_lot
        self.initialize_grid()
        self.participant_list()
        app.selected_numbers = Db.get_selected(app.cur_lot, app.cur_collection)
        self.selected_numbers = app.selected_numbers
        app.results_list = Db.get_result(app.cur_lot, app.cur_collection)
        self.ids["condition"].state = Db.get_condition(app.cur_lot, app.cur_collection)
        self.result_grid()
        self.selected_grid()

    def result_grid(self):
        self.ids["resultsGrid"].clear_widgets()
        for i in App.get_running_app().results_list:
            self.ids["resultsGrid"].add_widget(
                PopButton(str(self.shuffled_list.index(i) + 1), i, i))

    def selected_grid(self):
        self.ids["selected_numbers"].clear_widgets()
        for i in App.get_running_app().selected_numbers:
            self.ids["selected_numbers"].add_widget(PopButton(i, self.shuffled_list[int(i) - 1], i))
        App.get_running_app().lot_paper_status()

    def initialize_grid(self):
        app = App.get_running_app()
        sl = Db.get_shuffled(app.cur_lot, app.cur_collection)
        self.participants_list = Db.get_participants(app.cur_lot, app.cur_collection)
        if len(sl) != 0:
            self.shuffled_list = sl
        else:
            self.shuffled_list = self.participants_list
            random.shuffle(self.shuffled_list)
        app.shuffled_list = self.shuffled_list
        self.ids["privacy"].state = "normal"
        self.ids["lotGrid"].clear_widgets()
        for i, v in enumerate(self.shuffled_list):
            self.ids["lotGrid"].add_widget(LotPaper(str(i + 1), str(i + 1)))

    def participant_grid(self):
        app = App.get_running_app()
        self.participants_list = Db.get_participants(app.cur_lot, app.cur_collection)
        self.shuffled_list = self.participants_list
        random.shuffle(self.shuffled_list)
        Db.add_shuffled(self.shuffled_list, app.cur_lot, app.cur_collection)
        app.shuffled_list = self.shuffled_list
        self.ids["privacy"].state = "normal"
        self.ids["lotGrid"].clear_widgets()
        for i, v in enumerate(self.shuffled_list):
            self.ids["lotGrid"].add_widget(LotPaper(str(i + 1), str(i + 1)))

    def participant_list(self):
        data = ""
        for i in self.participants_list:
            data += f"{i}\n"
        self.ids["participants"].text = data

    def on_privacy(self, i, v):
        if self.privacy == "down":
            for i in self.ids["lotGrid"].children:
                i.name = self.shuffled_list[int(i.name) - 1]
        else:
            for i in self.ids["lotGrid"].children:
                i.name = str(self.shuffled_list.index(i.name) + 1)

    def on_shuffled_list(self, i, v):
        if self.privacy == "down":
            for i, v in enumerate(self.ids["lotGrid"].children):
                v.name = self.shuffled_list[len(self.shuffled_list) - i - 1]

    def shuffle(self):
        dic = {}
        app = App.get_running_app()
        for i in app.selected_numbers:
            dic[i] = self.shuffled_list[int(i) - 1]
        random.shuffle(self.shuffled_list)
        for k, v in dic.items():
            self.shuffled_list[self.shuffled_list.index(v)] = self.shuffled_list[int(k) - 1]
            self.shuffled_list[int(k) - 1] = v
        App.get_running_app().shuffled_list = self.shuffled_list
        Db.add_shuffled(self.shuffled_list, app.cur_lot, app.cur_collection)


Builder.load_file("designs/appBase.kv")


class LotApp(App):
    cur_collection = StringProperty()
    cur_lot = StringProperty()
    selected_numbers = ListProperty()
    results_list = ListProperty()
    shuffled_list = ListProperty()

    def build(self):
        Window.bind(on_key_down=self.on_back_btn)
        return AppManager()

    def back(self):
        screen_list = ["home", "collection", "lotScreen"]
        cur_screen = self.root.current
        if cur_screen == "home":
            self.stop()
        self.root.current = screen_list[screen_list.index(cur_screen) - 1]

    def on_selected_numbers(self, i, v):
        self.root.current_screen.ids["selected_numbers"].clear_widgets()
        for i in self.selected_numbers:
            self.root.current_screen.ids["selected_numbers"].add_widget(PopButton(i, self.shuffled_list[int(i) - 1], i))
        self.lot_paper_status()

    def lot_paper_status(self):
        for i in self.root.current_screen.ids["lotGrid"].children:
            if i.index not in self.selected_numbers:
                i.disabled = False
            else:
                i.disabled = True

    def on_results_list(self, i, v):
        self.root.current_screen.ids["resultsGrid"].clear_widgets()
        for i in self.results_list:
            self.root.current_screen.ids["resultsGrid"].add_widget(
                PopButton(str(self.shuffled_list.index(i) + 1), i, i))

    def on_back_btn(self, window, keycode, text, modifiers, *args):
        if keycode == 27:
            return self.back()
        elif keycode == 102:
            if not Window.fullscreen:
                Window.fullscreen = "auto"
                return
            Window.fullscreen = False

    @staticmethod
    def change_full_screen(state):
        if state == "down":
            Window.fullscreen = "auto"
            return
        Window.fullscreen = False
