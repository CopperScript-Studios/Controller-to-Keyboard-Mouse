import pygame
import pydirectinput
import pyautogui
import keyboard

pyautogui.PAUSE = 0
pydirectinput.PAUSE = 0

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    clock = pygame.time.Clock()
    running = True

    pressed_buttons = [False,False,False,False,False,None,None,False,None,None,None,None,None,None,None,False]
    pressed_axis = [[False,False],[False,False]]
    pressed_mouse_button_time = [0,0,None,0]

    while running:
        clock.tick(60)
        pygame.event.pump()

        ms = pygame.time.get_ticks()
        hold_delay = 1

        mouse_buttons = ['left','right',None,'middle']
        for i in range(len(mouse_buttons)):
            if mouse_buttons[i] == None:
                continue
            if joystick.get_button(i) and not pressed_buttons[i]:
                if abs(ms - pressed_mouse_button_time[i]) >= hold_delay * 1000:
                    pydirectinput.mouseDown(button=mouse_buttons[i])
                    pressed_buttons[i] = True
                else:
                    pydirectinput.click(button=mouse_buttons[i])
                    pressed_mouse_button_time[i] = ms
            elif pressed_buttons[i]:
                pydirectinput.mouseUp(button=mouse_buttons[i])
                pressed_buttons[i] = False
                pressed_mouse_button_time[i] = 0

        buttons = [None,None,'space',None,'delete',None,None,'shift',None,None,None,'up','down','left','right','escape']
        for i in range(len(buttons)):
            if buttons[i] == None:
                continue
            if joystick.get_button(i) and not pressed_buttons[i]:
                pydirectinput.keyDown(buttons[i])
                pressed_buttons[i] = True
            elif pressed_buttons[i]:
                pydirectinput.keyUp(buttons[i])
                pressed_buttons[i] = False

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
                    pydirectinput.keyUp('a')
                if pressed_axis[axis][1]:
                    pressed_axis[axis][1] = False
                    pydirectinput.keyUp('d')

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
