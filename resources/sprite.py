from pygame.sprite import Sprite as BaseSprite
from pygame.image import load


class Sprite(BaseSprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        # Will be implemented in the inheritors
        pass

    def draw(self,center, screen):
        self.rect.center = center
        screen.blit(self.image, self.rect)
