from typing import List

import pygame

RESET_SHOT_BUTTON = 8
DPAD_UP = 11
DPAD_DOWN = 12
DPAD_LEFT = 13
DPAD_RIGHT = 14


class Controller:
    def __init__(self):

        # Use pygame to monitor (and later log) player input
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self._events: List[int] = []


    def get_events(self) -> List[int]:
        # Monitor controller input to reset shot
        self._events.clear()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == RESET_SHOT_BUTTON: # R3 for reset
                    self._events.append(RESET_SHOT_BUTTON)

        return self._events