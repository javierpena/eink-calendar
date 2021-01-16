from datetime import datetime
import pygame
import sys

class PygameDriver():
    def __init__(self, xres, yres):
        pygame.init()
        self.screen = pygame.display.set_mode((xres, yres))
        self.xres = xres
        self.yres = yres

    # image1: black/white image
    # image2: black/yellow image
    def display(self, image1=None, image2=None):
        if image1:
            raw_str1 = image1.convert('RGBA').tobytes("raw", 'RGBA')
            pygame_surface1 = pygame.image.fromstring(raw_str1, (self.xres, self.yres), 'RGBA')
            self.screen.blit(pygame_surface1, (0, 0))

        if image2:
            raw_str2 = image2.convert('RGB').tobytes("raw", 'RGB')
            pygame_surface2 = pygame.image.fromstring(raw_str2, (self.xres, self.yres), 'RGB')
            pygame_surface2.set_colorkey((255, 255, 255))

            image_pixel_array = pygame.PixelArray(pygame_surface2)
            image_pixel_array.replace((0, 0, 0), (127, 100, 0))
            del image_pixel_array

            self.screen.blit(pygame_surface2, (0, 0))

        pygame.display.flip()

    def end(self):
        pygame.quit()

class PygameKBDriver():
    def __init__(self):
        pass

    def wait_for_keypress(self, timeout=60):
        start_time = datetime.now()
        while True:
            current_time = datetime.now()
            delta = current_time - start_time
            if delta.seconds > timeout:
                return None
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    elif event.key == pygame.K_2:
                        return 2
                    elif event.key == pygame.K_3:
                        return 3
                    elif event.key == pygame.K_4:
                        return 4
            pygame.time.wait(1000)
