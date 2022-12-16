from resources.sprite import Sprite
from constants import STEP_DISTANCE


class Box(Sprite):
    def __init__(self, image, startx, starty):
        super().__init__(image, startx, starty)


class Player(Sprite):
    def __init__(self, image, startx, starty):
        super().__init__(image, startx, starty)

        self.x_coord = startx
        self.y_coord = starty
        self.score = 0

    def change_coords(self, horizontal: int, vertical: int):
        self.x_coord = horizontal
        self.y_coord = vertical


class PlayerGroup(Sprite):
    def __init__(self, has_human_player: bool, player_image: str, startx, starty):
        super().__init__(image='./assets/empty.jpg',startx=startx, starty=starty)

        self.has_human_player = has_human_player
        self.players = [
            Player(image=player_image, startx=startx, starty=starty)]
        self.x_coord = startx
        self.y_coord = starty
        self.score = 0

    def moveLeft(self):
        self.x_coord -= STEP_DISTANCE

    def moveRight(self):
        self.x_coord += STEP_DISTANCE

    def moveUp(self):
        self.y_coord -= STEP_DISTANCE

    def moveDown(self):
        self.y_coord += STEP_DISTANCE

    def move_players(self,is_human_group):
        for player in self.players:
            player.change_coords(self.x_coord,self.y_coord)
            if is_human_group:
                player.score +=1

    def move(self, direction, is_human_group):
        if direction == 'right':
            self.moveRight()
        if direction == 'left':
            self.moveLeft()
        if direction == 'up':
            self.moveUp()
        if direction == 'down':
            self.moveDown()
        self.move_players(is_human_group)

    def add_player(self, player: Player):
        player.change_coords(self.x_coord,self.y_coord)
        self.players.append(player)
        

    def paint(self,screen):

        if len(self.players) == 1:
            self.players[0].change_coords(self.x_coord,self.y_coord)
            self.players[0].draw([self.x_coord,self.y_coord],screen)
        else:
            for index, player in enumerate(self.players):
                x_change = self.x_coord - ((index+1) * 8)
                y_change = self.y_coord - ((index+1) * 8)
                player.draw([x_change, y_change],screen)
