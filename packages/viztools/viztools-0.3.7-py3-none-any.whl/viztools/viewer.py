from abc import abstractmethod, ABC
from typing import Tuple, Optional, List

import numpy as np
import pygame as pg

from viztools.coordinate_system import CoordinateSystem, draw_coordinate_system
from viztools.drawable import Drawable


class Viewer(ABC):
    def __init__(self, screen_size: Optional[Tuple[int, int]] = None, framerate: int = 60, font_size: int = 16):
        pg.init()
        pg.key.set_repeat(130, 25)

        self.running = True
        self.render_needed = True
        self.clock = pg.time.Clock()
        self.framerate = framerate
        self.mouse_pos = np.array(pg.mouse.get_pos(), dtype=np.int32)

        mode = pg.RESIZABLE
        if screen_size is None:
            screen_size = (0, 0)
        if screen_size == (0, 0):
            mode = mode | pg.FULLSCREEN
        self.screen = pg.display.set_mode(screen_size, mode)

        self.coordinate_system = CoordinateSystem(screen_size)

        self.render_font = pg.font.Font(pg.font.get_default_font(), font_size)

    def run(self):
        delta_time = 0
        while self.running:
            self._handle_events()
            self.tick(delta_time)
            if self.render_needed:
                self._render()
                self.render_needed = False
            delta_time = self.clock.tick(self.framerate)
        pg.quit()

    def tick(self, delta_time: float):
        pass

    @abstractmethod
    def render(self):
        pass

    def render_drawables(self, drawables: List[Drawable]):
        for drawable in drawables:
            drawable.draw(self.screen, self.coordinate_system)

    def render_coordinate_system(self, draw_numbers=True):
        draw_coordinate_system(self.screen, self.coordinate_system, self.render_font, draw_numbers=draw_numbers)

    def _render(self):
        self.render()
        pg.display.flip()

    def _handle_events(self):
        events = pg.event.get()
        for event in events:
            self.handle_event(event)

    @abstractmethod
    def handle_event(self, event: pg.event.Event):
        if self.coordinate_system.handle_event(event):
            self.render_needed = True
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = np.array(event.pos)
        if event.type == pg.QUIT:
            self.running = False
        if event.type in (pg.WINDOWENTER, pg.WINDOWFOCUSGAINED, pg.WINDOWRESIZED):
            self.render_needed = True
