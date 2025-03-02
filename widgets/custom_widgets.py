from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp


# Custom button with modern styling
class ModernButton(Button):
    def __init__(self, bg_color="#4A90E2", **kwargs):
        super(ModernButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = [0, 0, 0, 0]  # Transparent
        self.bg_color = bg_color

        with self.canvas.before:
            Color(*get_color_from_hex(self.bg_color))
            self.background_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])

        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.background_rect.pos = self.pos
        self.background_rect.size = self.size
