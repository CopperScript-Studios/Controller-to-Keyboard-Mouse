import pygame
import pydirectinput
import pyautogui
import keyboard
import os
import ctypes

import os
import ctypes

try:
    # Per-Monitor DPI Aware V2
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        # Fallback for older Windows builds
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

pyautogui.PAUSE = 0
pydirectinput.PAUSE = 0
pydirectinput.FAILSAFE = False
pyautogui.FAILSAFE = False

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    clock = pygame.time.Clock()
    running = True

    media_button_index = 5
    media_tap_count = 0
    last_media_tap_time = 0
    media_tap_timeout = 300

    pressed_buttons = [None,None,False,None,None,None,None,False]
    pressed_axis = [[False,False],[False,False]]
    pressed_mouse = [False,False,None,False]
    pressed_mouse_button_time = [0,0,None,0]
    media_button_pressed = False

    while running:
        clock.tick(60)
        pygame.event.pump()

        ms = pygame.time.get_ticks()
        hold_delay = 0.5

        mouse_buttons = ['left', 'right', None, 'middle']
        for i in range(len(mouse_buttons)):
            if mouse_buttons[i] is None:
                continue

            if joystick.get_button(i) and not pressed_buttons[i]:
                pressed_buttons[i] = True
                pressed_mouse_button_time[i] = ms
                
            elif joystick.get_button(i) and pressed_buttons[i]:
                if ms - pressed_mouse_button_time[i] >= hold_delay * 1000 and not pressed_mouse[i]:
                    pydirectinput.mouseDown(button=mouse_buttons[i])
                    pressed_mouse[i] = True
                    
            elif not joystick.get_button(i) and pressed_buttons[i]:
                pressed_buttons[i] = False
                
                if pressed_mouse[i]:
                    pydirectinput.mouseUp(button=mouse_buttons[i])
                    pressed_mouse[i] = False
                else:
                    pydirectinput.click(button=mouse_buttons[i])

        def on_screen_keyboard():
            pydirectinput.keyDown('win')
            pydirectinput.keyDown('ctrl')
            pydirectinput.press('o')
            pydirectinput.keyUp('ctrl')
            pydirectinput.keyUp('win')

        buttons = [None,None,None,None,'delete',None,None,None,None,None,None,'up','down','left','right','escape']
        for i in range(len(buttons)):
            if buttons[i] == None:
                continue
            if joystick.get_button(i):
                if buttons[i] == 'on screen keyboard':
                    on_screen_keyboard()
                else:
                    pydirectinput.click(buttons[i])

        holdable_buttons = [None,None,'space',None,None,None,None,'shift']
        for i in range(len(holdable_buttons)):
            if holdable_buttons[i] == None:
                continue
            if joystick.get_button(i) and not pressed_buttons[i]:
                pydirectinput.keyDown(holdable_buttons[i])
                pressed_buttons[i] = True
            elif pressed_buttons[i]:
                pydirectinput.keyUp(holdable_buttons[i])
                pressed_buttons[i] = False

        if joystick.get_button(5) and not media_button_pressed:
            media_button_pressed = True
            media_tap_count += 1
            last_media_tap_time = ms
        elif not joystick.get_button(5) and media_button_pressed:
            media_button_pressed = False

        if media_tap_count > 0 and (ms - last_media_tap_time) > media_tap_timeout:
            if media_tap_count == 1:
                keyboard.send('play/pause media')
            elif media_tap_count == 2:
                keyboard.send('next track')
            elif media_tap_count >= 3:
                keyboard.send('previous track')
            
            media_tap_count = 0  # Reset tap counter

        movement_deadzone = 0.5
        axis_index = [['a','d'],['w','s']]

        def axis_cauculation(axis: int):
            if joystick.get_axis(axis) < -movement_deadzone:
                if not pressed_axis[axis][0]:
                    pressed_axis[axis][0] = True
                    if pressed_axis[axis][1]:
                        pydirectinput.keyUp(axis_index[axis][1])
                    pressed_axis[axis][1] = False
                    pydirectinput.keyDown(axis_index[axis][0])
            elif joystick.get_axis(axis) > movement_deadzone:
                if not pressed_axis[axis][1]:
                    pressed_axis[axis][1] = True
                    if pressed_axis[axis][0]:
                        pydirectinput.keyUp(axis_index[axis][0])
                    pressed_axis[axis][0] = False
                    pydirectinput.keyDown(axis_index[axis][1])
            else:
                if pressed_axis[axis][0]:
                    pressed_axis[axis][0] = False
                    pydirectinput.keyUp(axis_index[axis][0])
                if pressed_axis[axis][1]:
                    pressed_axis[axis][1] = False
                    pydirectinput.keyUp(axis_index[axis][1])

        axis_cauculation(0)            
        axis_cauculation(1)

        cam_x = joystick.get_axis(2)
        cam_y = joystick.get_axis(3)

        deadzone = 0.2
        speed_multiplier = 12

        cam_x = int(cam_x * speed_multiplier) if abs(cam_x) > deadzone else 0
        cam_y = int(cam_y * speed_multiplier) if abs(cam_y) > deadzone else 0

        if cam_x != 0 or cam_y != 0:
            if joystick.get_button(8):
                pyautogui.scroll(-cam_y)
            else:
                pydirectinput.move(cam_x, cam_y)

        if keyboard.is_pressed('delete'):
            running = False
