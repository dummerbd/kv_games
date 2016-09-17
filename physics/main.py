from random import randint
from math import radians
from functools import partial

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.widget import Widget

import kivent_core
import kivent_cymunk
from kivent_core.managers.resource_managers import texture_manager
from kivent_core.systems.gamesystem import GameSystem


texture_manager.load_atlas('../assets/background_objects.atlas')


class VelocitySystem2D(GameSystem):
    def update(self, dt):
        for component in self.components:
            if component is not None:
                entity = self.gameworld.entities[component.entity_id]
                pos_comp = entity.position
                pos_comp.x += component.vx * dt
                pos_comp.y += component.vy * dt
                if pos_comp.x <= 0:
                    pos_comp.x = Window.width
                elif pos_comp.x >= Window.width:
                    pos_comp.x = 0
                if pos_comp.y <= 0:
                    pos_comp.y = Window.height
                elif pos_comp.y >= Window.height:
                    pos_comp.y = 0

Factory.register('VelocitySystem2D', cls=VelocitySystem2D)


class DemoGame(Widget):
    def __init__(self, **kwargs):
        super(DemoGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld([
            'cymunk_physics', 'rotate_renderer', 'rotate', 'position'
        ], callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.set_state()

    def destroy_created_entity(self, ent_id, dt):
        self.gameworld.remove_entity(ent_id)
        self.app.count -= 1

    def setup_states(self):
        self.gameworld.add_state(
            state_name='main',
            systems_added=['rotate_renderer'],
            systems_removed=[],
            systems_paused=[],
            systems_unpaused=['rotate_renderer'],
            screenmanager_screen='main')

    def set_state(self):
        self.gameworld.state = 'main'

    def update(self, dt):
        self.gameworld.update(dt)

    def create_asteroid(self, pos):
        x_vel = randint(-500, 500)
        y_vel = randint(-500, 500)
        angle = radians(randint(-360, 360))
        angular_velocity = radians(randint(-150, -150))
        shape_dict = {
            'inner_radius': 0,
            'outer_radius': 20,
            'mass': 50,
            'offset': (0, 0)
        }
        col_shape = {
            'shape_type': 'circle',
            'elasticity': .5,
            'collision_type': 1,
            'shape_info': shape_dict,
            'friction': 1.0
        }
        col_shapes = [col_shape]
        physics_component = {
            'main_shape': 'circle',
            'velocity': (x_vel, y_vel),
            'position': pos,
            'angle': angle,
            'angular_velocity': angular_velocity,
            'vel_limit': 250,
            'ang_vel_limit': radians(200),
            'mass': 50,
            'col_shapes': col_shapes
        }
        component = {
            'cymunk_physics': physics_component,
            'rotate_renderer': {
                'texture': 'asteroid1',
                'size': (45, 45),
                'render': True
            },
            'position': pos,
            'rotate': 0
        }
        component_order = ['position', 'rotate', 'rotate_renderer', 'cymunk_physics']
        return self.gameworld.init_entity(component, component_order)

    def draw_asteroids(self):
        size = Window.size
        w, h = size[0], size[1]
        delete_time = 2.5
        create_asteroid = self.create_asteroid
        destroy_ent = self.destroy_created_entity
        for x in range(100):
            pos = (randint(0, w), randint(0, h))
            ent_id = create_asteroid(pos)
            Clock.schedule_once(partial(destroy_ent, ent_id), delete_time)
        self.app.count += 100


class DebugPanel(Widget):
    fps = StringProperty(None)

    def __init__(self, **kwargs):
        super(DebugPanel, self).__init__(**kwargs)
        Clock.schedule_once(self.update_fps)

    def update_fps(self, dt):
        self.fps = str(int(Clock.get_fps()))
        Clock.schedule_once(self.update_fps, .05)


class DemoApp(App):
    count = NumericProperty(0)


if __name__ == '__main__':
    DemoApp().run()
