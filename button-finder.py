import pygame

pygame.init()
pygame.joystick.init()

deadzone = 0.2
clock = pygame.time.Clock()

if pygame.joystick.get_count() == 0:
    print("ERROR: No controller detected! Plug one in and restart.")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Connected to: {joystick.get_name()}")
    print('Press "Delete" to exit.')
    print('Now listening for inputs...')
    
    running = True
    while running:
        clock.tick(60)  # Prevents 100% CPU usage loop
        
        for event in pygame.event.get():
            # Catch window close button (X)
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button: {event.button}")

            elif event.type == pygame.JOYAXISMOTION:
                if abs(event.value) > deadzone:
                    print(f"Axis {event.axis} moved to: {event.value:.2f}")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    print('Stopped listening for inputs.')
                    running = False

pygame.quit()