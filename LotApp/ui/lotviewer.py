from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import sp
from kivy.properties import NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView

from logics.db import Db


class LotViewer(ModalView):

    def __init__(self, nums, shuffled, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.overlay_color = [0, 0, 0, 0]
        self.background = ""
        self.background_color = [0.3, 0.9, 0.7, 1]
        self.size_hint = [0.6, 0.4]
        self.pos_hint = {"center_x": 0.35, "center_y": 0.50}
        self.add_widget(Viewer(nums, shuffled))
        self.open()


class Viewer(BoxLayout):
    index = NumericProperty()

    def __init__(self, nums, shuffled, **kwargs):
        super().__init__(**kwargs)
        al = AnchorLayout(anchor_x="left", anchor_y="top")
        self.btn = Button(size_hint=(0.5, 0.5), font_size=sp(50))
        al.add_widget(self.btn)
        self.add_widget(al)
        self.index = 0
        self.nums = nums
        self.shuffled = shuffled
        Clock.schedule_once(self.initialize, 0)

    def initialize(self, dt):
        if self.index == len(self.nums):
            self.parent.dismiss()
            return
        self.btn.text = self.nums[self.index]
        self.btn.size_hint = [0.5, 0.5]
        Clock.schedule_once(self.start_opening, 2)
        Clock.unschedule(self.initialize)

    def start_opening(self, dt):
        Clock.schedule_interval(self.animate, 0.5)
        Clock.unschedule(self.start_opening)

    def animate(self, dt):
        if self.btn.size_hint == [1, 1]:
            Clock.unschedule(self.animate)
            Clock.schedule_once(self.initialize, 2)
            return
        if self.btn.size_hint == [0.5, 0.5]:
            self.btn.size_hint = [1, 0.5]
        else:
            app = App.get_running_app()
            self.btn.size_hint = [1, 1]
            self.btn.text = self.shuffled[int(self.nums[self.index]) - 1]
            app.results_list.append(self.btn.text)
            Db.add_result(app.results_list, app.cur_lot, app.cur_collection)
            self.index += 1
