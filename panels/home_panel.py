from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex


class HomePanel(Screen):
    def __init__(self, **kwargs):
        super(HomePanel, self).__init__(**kwargs)

        # Main layout
        self.layout = BoxLayout(orientation='vertical')

        # Top ribbon with panel name, hamburger menu, and notification icon
        self.top_ribbon = BoxLayout(
            size_hint=(1, None),
            height=dp(60),
            padding=[dp(15), dp(10)],
            spacing=dp(10)
        )

        # Add background color to top ribbon
        with self.top_ribbon.canvas.before:
            Color(*get_color_from_hex("#F6F6F6"))  # Light gray color
            self.top_bg = Rectangle(pos=self.top_ribbon.pos, size=self.top_ribbon.size)

        # Update rectangle position and size when layout changes
        self.top_ribbon.bind(pos=self._update_rect, size=self._update_rect)

        # Hamburger menu icon
        self.hamburger_menu = Image(
            source='./icons/hamburgerMenu.png',  # Path to the hamburger menu icon
            size_hint=(None, None),
            size=(dp(33), dp(33))
        )

        # Panel name label
        self.panel_label = Label(
            text="Home Panel",
            font_size=dp(20),
            bold=True,
            color=get_color_from_hex("#19081c")
        )

        # Notification icon
        self.notification_icon = Image(
            source='./icons/notification.png',  # Path to the notification icon
            size_hint=(None, None),
            size=(dp(33), dp(33))
        )

        # Add hamburger menu, label, and notification icon to top ribbon
        self.top_ribbon.add_widget(self.hamburger_menu)
        self.top_ribbon.add_widget(self.panel_label)
        self.top_ribbon.add_widget(self.notification_icon)

        # Add top ribbon to main layout
        self.layout.add_widget(self.top_ribbon)

        # Content area (placeholder)
        self.content_area = BoxLayout(orientation='vertical', padding=[dp(10), dp(10)])

        # Add background color to content area
        with self.content_area.canvas.before:
            Color(*get_color_from_hex("#FFFFFF"))  # White color
            self.content_bg = Rectangle(pos=self.content_area.pos, size=self.content_area.size)

        # Update content rectangle position and size when layout changes
        self.content_area.bind(pos=self._update_content_rect, size=self._update_content_rect)

        # Add content area to main layout
        self.layout.add_widget(self.content_area)

        # Add main layout to screen
        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        """Update the rectangle position and size."""
        self.top_bg.pos = instance.pos
        self.top_bg.size = instance.size

    def _update_content_rect(self, instance, value):
        """Update the content rectangle position and size."""
        self.content_bg.pos = instance.pos
        self.content_bg.size = instance.size