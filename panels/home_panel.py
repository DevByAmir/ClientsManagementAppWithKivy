import json
import os

from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex


class MenuButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)


class NotificationButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(NotificationButton, self).__init__(**kwargs)


class SideMenu(RelativeLayout):
    def __init__(self, **kwargs):
        super(SideMenu, self).__init__(size_hint=(1, 1))
        self.opacity = 0
        self.visible = False

        # Overlay for darkening the background
        self.overlay = BoxLayout(size_hint=(1, 1))
        with self.overlay.canvas.before:
            Color(0, 0, 0, 0.5)  # Semi-transparent black
            self.overlay_rect = Rectangle(pos=self.overlay.pos, size=self.overlay.size)
        self.overlay.bind(pos=self._update_overlay_rect, size=self._update_overlay_rect)

        # Menu panel
        self.menu_panel = BoxLayout(
                orientation='vertical',
                size_hint=(0.5, 1),
                pos_hint={'x': -0.5, 'y': 0}  # Start off-screen to the left
        )

        # Add background color to menu panel
        with self.menu_panel.canvas.before:
            Color(*get_color_from_hex("#333333"))  # Darker background for menu
            self.menu_bg = Rectangle(pos=self.menu_panel.pos, size=self.menu_panel.size)

        # Update rectangle position and size when layout changes
        self.menu_panel.bind(pos=self._update_menu_rect, size=self._update_menu_rect)

        # Menu items container - explicitly at the top with padding
        self.menu_items = BoxLayout(
                orientation='vertical',
                padding=[dp(20), dp(40), dp(20), dp(20)],  # Extra padding at top
                size_hint_y=None,
                height=dp(150)
        )

        # Add menu items
        self.settings_btn = Label(
                text="Settings",
                font_size=dp(18),
                color=get_color_from_hex("#FFFFFF"),
                size_hint_y=None,
                height=dp(50)
        )

        self.about_btn = Label(
                text="About",
                font_size=dp(18),
                color=get_color_from_hex("#FFFFFF"),
                size_hint_y=None,
                height=dp(50)
        )

        # Add menu items to container
        self.menu_items.add_widget(self.settings_btn)
        self.menu_items.add_widget(self.about_btn)

        # Add items container to menu panel
        self.menu_panel.add_widget(self.menu_items)

        # Add filler to push menu items to the top
        self.menu_panel.add_widget(BoxLayout())

        # Add overlay and menu panel to the layout
        self.add_widget(self.overlay)
        self.add_widget(self.menu_panel)

        # Bind overlay touch to close menu
        self.overlay.bind(on_touch_down=self._on_overlay_touch)

    def _update_overlay_rect(self, instance, value):
        """Update the overlay rectangle position and size."""
        self.overlay_rect.pos = instance.pos
        self.overlay_rect.size = instance.size

    def _update_menu_rect(self, instance, value):
        """Update the menu rectangle position and size."""
        self.menu_bg.pos = instance.pos
        self.menu_bg.size = instance.size

    def _on_overlay_touch(self, instance, touch):
        """Close menu when overlay is touched."""
        if self.visible and instance.collide_point(*touch.pos):
            print("Overlay clicked - closing menu")
            self.close()
            return True

    def open(self):
        """Open the side menu with animation."""
        print("Opening menu")
        if not self.visible:
            self.opacity = 1
            self.visible = True
            # Animate the menu panel sliding in from left
            anim = Animation(pos_hint={'x': 0, 'y': 0}, duration=0.3)
            anim.start(self.menu_panel)

    def close(self):
        """Close the side menu with animation."""
        print("Closing menu")
        if self.visible:
            # Animate the menu panel sliding out to left
            anim = Animation(pos_hint={'x': -0.5, 'y': 0}, duration=0.3)
            anim.bind(on_complete=self._after_close)
            anim.start(self.menu_panel)

    def _after_close(self, *args):
        """Called after close animation completes."""
        self.opacity = 0
        self.visible = False


class NotificationItem(BoxLayout):
    def __init__(self, time, title, duration=None, **kwargs):
        super(NotificationItem, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(100)
        self.padding = [dp(15), dp(10)]
        self.spacing = dp(5)

        # Add background with rounded corners and shadow effect
        with self.canvas.before:
            # Shadow effect (slightly larger, darker rectangle behind)
            Color(0.85, 0.85, 0.85, 1)  # Light gray for shadow
            self.shadow = RoundedRectangle(
                    pos=(self.pos[0] + dp(2), self.pos[1] - dp(2)),
                    size=(self.size[0], self.size[1]),
                    radius=[dp(10)]
            )

            # Main background (white rounded rectangle)
            Color(*get_color_from_hex("#FFFFFF"))
            self.bg = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(10)]
            )

        # Update rectangle position and size when layout changes
        self.bind(pos=self._update_rect, size=self._update_rect)

        # Create horizontal layout for time and title
        time_title_layout = BoxLayout(size_hint_y=None, height=dp(40))

        # Time label
        time_label = Label(
                text=time,
                font_size=dp(16),
                color=get_color_from_hex("#666666"),
                size_hint_x=None,
                width=dp(100),
                halign='left',
                valign='middle'
        )
        time_label.bind(texture_size=time_label.setter('text_size'))

        # Title label
        title_label = Label(
                text=title,
                font_size=dp(16),
                bold=True,
                color=get_color_from_hex("#333333"),
                halign='left',
                valign='middle'
        )
        title_label.bind(texture_size=title_label.setter('text_size'))

        # Add time and title to horizontal layout
        time_title_layout.add_widget(time_label)
        time_title_layout.add_widget(title_label)

        # Create duration layout if duration provided
        if duration:
            duration_layout = BoxLayout(size_hint_y=None, height=dp(30))
            duration_label = Label(
                    text=duration,
                    font_size=dp(14),
                    color=get_color_from_hex("#999999"),
                    size_hint_x=None,
                    width=dp(100),
                    halign='left',
                    valign='middle'
            )
            duration_label.bind(texture_size=duration_label.setter('text_size'))

            # Add clock icon
            clock_icon = Image(
                    source='./images/clock.png',  # You might need to add this icon
                    size_hint=(None, None),
                    size=(dp(16), dp(16))
            )

            duration_layout.add_widget(clock_icon)
            duration_layout.add_widget(duration_label)

        # Notification bell
        bell_icon = Image(
                source='./images/notification.png',
                size_hint=(None, None),
                size=(dp(24), dp(24)),
                pos_hint={'right': 1}
        )

        # Add widgets to main layout
        self.add_widget(time_title_layout)
        if duration:
            self.add_widget(duration_layout)

        # Add bell icon
        bell_layout = BoxLayout(size_hint_y=None, height=dp(24))
        bell_layout.add_widget(Label())  # Spacer
        bell_layout.add_widget(bell_icon)
        self.add_widget(bell_layout)

    def _update_rect(self, instance, value):
        """Update the rectangle position and size."""
        self.bg.pos = instance.pos
        self.bg.size = instance.size
        # Update shadow position to create shadow effect
        self.shadow.pos = (instance.pos[0] + dp(2), instance.pos[1] - dp(2))
        self.shadow.size = instance.size


class NotificationsPanel(Screen):
    def __init__(self, **kwargs):
        super(NotificationsPanel, self).__init__(**kwargs)

        # Main layout
        self.layout = BoxLayout(orientation='vertical')

        # Top ribbon with back button and panel name
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

        # Back button with arrow icon
        self.back_button = MenuButton(
                source='./images/leftArrow.png',
                size_hint=(None, None),
                size=(dp(33), dp(33))
        )
        self.back_button.bind(on_release=self.go_back_to_home)

        # Panel name label
        self.panel_label = Label(
                text="Notifications",
                font_size=dp(20),
                bold=True,
                color=get_color_from_hex("#19081c")
        )

        # Add back button and title to top ribbon
        self.top_ribbon.add_widget(self.back_button)
        self.top_ribbon.add_widget(self.panel_label)
        # Add empty widget to balance layout
        empty_widget = BoxLayout(size_hint=(None, None), size=(dp(33), dp(33)))
        self.top_ribbon.add_widget(empty_widget)

        # Add top ribbon to main layout
        self.layout.add_widget(self.top_ribbon)

        # Content area with notifications
        self.content_area = ScrollView(do_scroll_x=False)

        # Container for notification items
        self.notifications_container = BoxLayout(
                orientation='vertical',
                padding=[dp(15), dp(15)],
                spacing=dp(15),
                size_hint_y=None
        )
        # Bind height to children to ensure proper scrolling
        self.notifications_container.bind(minimum_height=self.notifications_container.setter('height'))

        # Add container to scroll view
        self.content_area.add_widget(self.notifications_container)

        # Add background color to content area
        with self.content_area.canvas.before:
            Color(*get_color_from_hex("#F0F0F0"))  # Light gray background
            self.content_bg = Rectangle(pos=self.content_area.pos, size=self.content_area.size)

        # Update content rectangle position and size when layout changes
        self.content_area.bind(pos=self._update_content_rect, size=self._update_content_rect)

        # Add content area to main layout
        self.layout.add_widget(self.content_area)

        # Add main layout to screen
        self.add_widget(self.layout)

        # Load notifications from JSON when panel is shown
        self.bind(on_pre_enter=self.load_notifications)

    def _update_rect(self, instance, value):
        """Update the rectangle position and size."""
        self.top_bg.pos = instance.pos
        self.top_bg.size = instance.size

    def _update_content_rect(self, instance, value):
        """Update the content rectangle position and size."""
        self.content_bg.pos = instance.pos
        self.content_bg.size = instance.size

    def go_back_to_home(self, instance):
        """Go back to home screen."""
        print("Back button clicked - returning to home panel")
        if self.manager:
            # Check if 'home' screen exists in the screen manager
            if 'home' in self.manager.screen_names:
                self.manager.current = 'home'
            else:
                print("Warning: 'home' screen not found in screen manager")
                # Fallback - try to find any available screen
                if len(self.manager.screen_names) > 0 and self.manager.screen_names[0] != self.name:
                    self.manager.current = self.manager.screen_names[0]
                else:
                    print("Error: No alternative screens available")

    def load_notifications(self, *args):
        """Load notifications from JSON file."""
        self.notifications_container.clear_widgets()
        try:
            # Check if notifications.json exists
            if os.path.exists('./data/notifications.json'):
                with open('./data/notifications.json', 'r') as file:
                    notifications = json.load(file)

                # Add notifications to the container
                for notification in notifications:
                    time = notification.get('time', '')
                    title = notification.get('title', '')
                    duration = notification.get('duration', None)

                    self.notifications_container.add_widget(
                            NotificationItem(time=time, title=title, duration=duration)
                    )
            else:
                # Fallback to sample data if JSON doesn't exist
                self.load_sample_notifications()

        except Exception as e:
            print(f"Error loading notifications: {e}")
            # Fallback to sample data
            self.load_sample_notifications()

    def load_sample_notifications(self):
        """Load sample notifications for testing."""
        self.notifications_container.add_widget(
                NotificationItem(time="9:00 am", title="Client Meeting", duration="5h")
        )
        self.notifications_container.add_widget(
                NotificationItem(time="11:00 am", title="Team Standup", duration="5h")
        )
        self.notifications_container.add_widget(
                NotificationItem(time="3:00 pm", title="Design Conference", duration="11h")
        )
        self.notifications_container.add_widget(
                NotificationItem(time="4:30 pm", title="Project Deadline", duration="11h")
        )


class HomePanel(Screen):
    def __init__(self, **kwargs):
        super(HomePanel, self).__init__(**kwargs)

        # Notification status - default to False (no notifications)
        self.has_notifications = False

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

        # Hamburger menu button
        self.hamburger_menu = MenuButton(
                source='./images/hamburgerMenu.png',
                size_hint=(None, None),
                size=(dp(33), dp(33))
        )
        self.hamburger_menu.bind(on_release=self.open_menu)

        # Panel name label
        self.panel_label = Label(
                text="Home Panel",
                font_size=dp(20),
                bold=True,
                color=get_color_from_hex("#19081c")
        )

        # Notification button with regular icon
        self.notification_icon = NotificationButton(
                source='./images/notification.png',
                size_hint=(None, None),
                size=(dp(33), dp(33))
        )
        self.notification_icon.bind(on_release=self.show_notifications)

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

        # Create side menu
        self.side_menu = SideMenu()

        # Add the side menu on top of everything but make it invisible initially
        self.add_widget(self.layout)
        self.add_widget(self.side_menu)

        # Check for notifications when panel is shown
        self.bind(on_pre_enter=self.check_for_notifications)

    def _update_rect(self, instance, value):
        """Update the rectangle position and size."""
        self.top_bg.pos = instance.pos
        self.top_bg.size = instance.size

    def _update_content_rect(self, instance, value):
        """Update the content rectangle position and size."""
        self.content_bg.pos = instance.pos
        self.content_bg.size = instance.size

    def open_menu(self, instance):
        """Open the side menu."""
        print("Hamburger menu clicked")
        self.side_menu.open()

    def show_notifications(self, instance):
        """Switch to notifications panel."""
        print("Notification icon clicked")

        if self.manager:
            print("Switching to notifications panel")
            # Check if notifications screen exists in manager
            if 'notifications' not in self.manager.screen_names:
                # Create and add the notifications screen if it doesn't exist
                notifications_screen = NotificationsPanel(name='notifications')
                self.manager.add_widget(notifications_screen)

            # Switch to notifications screen
            self.manager.current = 'notifications'

            # Reset notification icon after viewing
            self.set_has_notifications(False)

    def check_for_notifications(self, *args):
        """Check if there are any notifications by looking for the JSON file."""
        try:
            # Check if notifications.json exists and has content
            if os.path.exists('./data/notifications.json'):
                with open('./data/notifications.json', 'r') as file:
                    notifications = json.load(file)
                    # Set notification indicator if there are notifications
                    self.set_has_notifications(len(notifications) > 0)
            else:
                # Create directory if it doesn't exist
                os.makedirs('./data', exist_ok=True)

                # Create a sample notifications file for testing
                sample_notifications = [
                        {"time": "9:00 am", "title": "Client Meeting", "duration": "5h"},
                        {"time": "11:00 am", "title": "Team Standup", "duration": "5h"},
                        {"time": "3:00 pm", "title": "Design Conference", "duration": "11h"},
                        {"time": "4:30 pm", "title": "Project Deadline", "duration": "11h"}
                ]

                with open('./data/notifications.json', 'w') as file:
                    json.dump(sample_notifications, file)

                # Set notification indicator to true for the sample data
                self.set_has_notifications(True)

        except Exception as e:
            print(f"Error checking for notifications: {e}")
            # Default to sample data behavior
            self.set_has_notifications(True)

    def set_has_notifications(self, has_notifications):
        """Set whether there are notifications and update the icon."""
        print(f"Setting notification status to: {'Has notifications' if has_notifications else 'No notifications'}")
        self.has_notifications = has_notifications
        if has_notifications:
            self.notification_icon.source = './images/notificationRed.png'
        else:
            self.notification_icon.source = './images/notification.png'


def setup_screen_manager():
    """Setup screen manager with all required screens."""
    sm = ScreenManager()

    # Create screens
    home_screen = HomePanel(name='home')
    notifications_screen = NotificationsPanel(name='notifications')

    # Add screens to manager
    sm.add_widget(home_screen)
    sm.add_widget(notifications_screen)

    # Verify screens are properly registered
    print(f"Available screens: {sm.screen_names}")

    return sm
