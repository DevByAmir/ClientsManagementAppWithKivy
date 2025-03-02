from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# Import panels
from panels.home_panel import HomePanel


class PatientSchedulerApp(App):
    def build(self):
        # Set app title
        self.title = 'Patient Scheduler'

        # Create screen manager
        sm = ScreenManager()

        # Add panels to the screen manager
        sm.add_widget(HomePanel())

        return sm


if __name__ == '__main__':
    PatientSchedulerApp().run()