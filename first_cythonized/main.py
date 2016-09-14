from random import randint, choice

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.widget import Widget

from kivent_core.managers.resource_managers import texture_manager

from velocity_module.velocity import VelocitySystem2D


texture_manager.load_atlas('../assets/background_objects.atlas')


class TestGame(Widget):
    def __init__(self, **kwargs):
        super(TestGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld([
            'renderer', 'position', 'velocity'
        ], callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.load_models()
        self.draw_stuff()

    def setup_states(self):
        self.gameworld.add_state(
            state_name='main',
            systems_added=['renderer'],
            systems_removed=[],
            systems_paused=[],
            systems_unpaused=['renderer', 'velocity'],
            screenmanager_screen='main')

    def set_state(self):
        self.gameworld.state = 'main'

    def load_models(self):
        model_manager = self.gameworld.model_manager
        model_manager.load_textured_rectangle(
            'vertex_format_4f', 5, 5, 'star1', 'star1-4f-1')
        model_manager.load_textured_rectangle(
            'vertex_format_4f', 10, 10, 'star1', 'star1-4f-2')

    def draw_stuff(self):
        for x in range(5000):
            pos = randint(0, Window.width), randint(0, Window.height)
            vel = randint(-50, 50), randint(-50, 50)
            bounds = 0, 0, Window.width, Window.height
            model_key = choice(['star1-4f-1', 'star1-4f-2'])
            self.gameworld.init_entity({
                'position': pos,
                'velocity': (vel, bounds),
                'renderer': {
                    'texture': 'star1',
                    'model_key': model_key
                }
            }, ['position', 'velocity', 'renderer'])


class DebugPanel(Widget):
    fps = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.update_fps)

    def update_fps(self, dt):
        self.fps = str(int(Clock.get_fps()))
        Clock.schedule_once(self.update_fps, .05)


class FirstApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)

if __name__ == '__main__':
    FirstApp().run()
