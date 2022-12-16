from dataclasses import dataclass, field
from random import randrange
from time import sleep
from typing import Any, List

# from pygame import init as pg_init, display as pg_display, image as pg_image, Surface as PG_Surface, font
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from levels import Level
from resources.dimension import Dimensions



DIFFICULTY = ['EASY']
DIMS=[3]
ROWS=[3]
COLUMNS=[3]
PLAYERS=[2]
FPS = 60


@dataclass
class Stats:
    
    difficulty: str = ""
    attempt: int = 0
    min: int = 0
    max: int = 0


@dataclass
class Game:

    menu_states: List[str] = field(init=False)
    screen: pygame.Surface = field(init=False)
    play_menu: Any = field(init=False)
    stats: List[Stats] =  field(init=False)
    is_running: bool = True
    is_paused: bool = True
    display_caption_prefix: str = "Lost in the Woods"

    selected_menu_state: str = 'main'

    auto_play: bool = False
    selected_level: str = 'EASY'



    def background(self):
        global surface
        surface.fill((0,0,0))


    def update_stats(self,index,score):
            self.stats[index].attempt +=1
            self.stats[index].min = min(score, self.stats[index].min) if self.stats[index].min !=0 else score
            self.stats[index].max = max(score, self.stats[index].max) if self.stats[index].max !=0 else score

            try:
                with open(f'scores{index}.txt','w') as file:
                    file.write(f"{self.stats[index].attempt}\n")
                    file.write(f"{self.stats[index].min}\n")
                    file.write(f"{self.stats[index].max}\n")
            except: 
                print("File not found!")

    def play_function(self,difficulty: List, test: bool = False) -> None:
        """
        Main game function.
        :param difficulty: Difficulty of the game
        :param font: Pygame font
        :param test: Test method, if ``True`` only one loop is allowed
        """
        assert isinstance(difficulty, list)
        difficulty = difficulty[0]
        assert isinstance(difficulty, str)

        # Define globals
        global main_menu
        global clock


        if difficulty == 'EASY':
            level = Level(autoplay=False,dimensions= Dimensions(COLUMNS[0],ROWS[0]),number_of_players= PLAYERS[0])
            score = level.start(clock)
        elif difficulty == 'MEDIUM':
            level = Level(autoplay=False,dimensions= Dimensions(COLUMNS[0],ROWS[0]),number_of_players= PLAYERS[0])
            score = level.start(clock)
        elif difficulty == 'HARD':
            level = Level(autoplay=False,dimensions= Dimensions(COLUMNS[0],ROWS[0]),number_of_players= PLAYERS[0])
            score = level.start(clock)
        else:
            raise ValueError(f'unknown difficulty {difficulty}')
        font = pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30)
        f_esc = font.render('Game Ended', True, (255, 255, 255))

        if self.selected_level == "EASY":
            self.update_stats(0,score)
        if self.selected_level == "MEDIUM":
            self.update_stats(1,score)
        if self.selected_level == "HARD":
            self.update_stats(2,score)

        bg_color = (0,0,0)
        self.prep_play_menu()
        # Reset main menu and disable
        # You also can set another menu, like a 'pause menu', or just use the same
        # main_menu as the menu that will check all your input.

        main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        main_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT,
            theme=main_theme,
            title='Main Menu',
            width=WINDOW_WIDTH
        )
        main_menu.add.button('Play', self.play_menu)

        main_menu.add.selector('Difficulty ',
                            [('Easy', 'EASY'),
                            ('Medium', 'MEDIUM'),
                            ('Hard', 'HARD')],
                            onchange=self.change_difficulty,)
        main_menu.add.button('Quit', pygame_menu.events.EXIT)

        main_menu.enable()

        while True:
            clock.tick(60)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        main_menu.enable()
                        return
                        
            if main_menu.is_enabled():
                main_menu.update(events)

            surface.fill(bg_color)

            surface.blit(f_esc, (int((WINDOW_WIDTH - f_esc.get_width()) / 2),
                                int(WINDOW_HEIGHT / 2 + f_esc.get_height())))
            pygame.display.flip()


    def change_difficulty(self,value, difficulty) -> None:
        self.selected_level=difficulty
        DIFFICULTY[0] = difficulty


    def change_rows(self,value, row) -> None:
        ROWS[0] = row


    def change_columns(self,value, col) -> None:
        COLUMNS[0] = col

    def change_dims(self,value, col) -> None:
        DIMS[0] = col
        
    def change_players(self,value, players) -> None:
        PLAYERS[0] = players
        
    def prep_play_menu(self):

        submenu_theme = pygame_menu.Theme(background_color=(12, 0, 0, 0),
                            title_background_color=(4, 47, 126),
                            title_font_shadow=True,
                            widget_padding=10,
                            #widget_font = pygame_menu.font.FONT_DIGITAL,
                            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE)
        self.play_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT,
            title='Play Menu',
            width=WINDOW_WIDTH,
            theme= submenu_theme,
        )
        #self.play_menu.add.button('Exit', pygame_menu.events.EXIT,       # Link to exit action
        #                    align=pygame_menu.locals.ALIGN_RIGHT)
        play_submenu = pygame_menu.Menu(
            height=WINDOW_HEIGHT,
            theme=submenu_theme,
            title='Scores',
            width=WINDOW_WIDTH
        )

        attempt = 0
        mini = 0
        maxi = 0
        for stat in self.stats:
            if stat.difficulty == self.selected_level:
                attempt = stat.attempt
                mini = stat.min
                maxi = stat.max
                break

        score_select = play_submenu.add.dropselect('Difficulty Level',
                            [('Easy', 'EASY'),
                            ('Medium', 'MEDIUM'),
                            ('Hard', 'HARD')],
                        dropselect_id='select_difficulty',
                        default=(0),
                        onchange=self.change_difficulty,
                        placeholder_add_to_selection_box=False,
                        selection_box_bgcolor=(173,38,226,200),
                        selection_option_selected_bgcolor=(188, 227, 244),
                        selection_option_selected_font_color=(0,45,46),
                        )

        play_submenu.add.label(f'Score for fifficulty: {stat.difficulty.lower()}')
        play_submenu.add.label(f'Total Played {attempt}')
        play_submenu.add.label(f'Fastest {mini} ')
        play_submenu.add.label(f'Slowest {maxi} ')    
        play_submenu.add.button('Back',
                        pygame_menu.events.RESET,
                        font_size=20, font_color='black',
                        background_color='green',
                        #align=pygame_menu.locals.ALIGN_RIGHT,
                        margin=(200,20),
                        selection_color='purple'
                        )

        self.play_menu.add.dropselect('Players ',
                        [('2',2),('3',3),('4',4)],
                        dropselect_id='select_players',
                        default=(0),
                        onchange=self.change_players,
                        placeholder_add_to_selection_box=False,
                        selection_box_bgcolor=(173,38,226,200),
                        selection_option_selected_bgcolor=(188, 227, 244),
                        selection_option_selected_font_color=(0,45,46),
                        )

        self.play_menu.add.dropselect('Rows    ',
                        [('2',2),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9)],
                        default=(0),   
                        onchange=self.change_rows,
                        dropselect_id='select_row',
                        placeholder_add_to_selection_box=False,
                        selection_box_bgcolor=(173,38,226,200),
                        selection_option_selected_bgcolor=(188, 227, 244),
                        selection_option_selected_font_color=(0,45,46),
                        )

        self.play_menu.add.dropselect('Columns ',
                        [('2',2),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9)],
                        default=(0),                     
                        onchange=self.change_columns,
                        dropselect_id='select_cols',
                        placeholder_add_to_selection_box=False,
                        selection_box_bgcolor=(173,38,226,200),
                        selection_option_selected_bgcolor=(188, 227, 244),
                        selection_option_selected_font_color=(0,45,46),
                        )

        self.play_menu.add.button('Begin',  # When pressing return -> play(DIFFICULTY[0], font)
                        self.play_function,
                        DIFFICULTY,
                        font_size=20,
                        font_color='black',
                        background_color='green',
                        #align=pygame_menu.locals.ALIGN_RIGHT,
                        margin=(200,20),
                        selection_color='purple'
                        )

        self.play_menu.add.button('Score', play_submenu,
                        font_size=20, font_color='black',
                        background_color='red',
                        float=True, margin=(80,20),
                        selection_color='purple'
                        )

        self.play_menu.add.button('Back', pygame_menu.events.BACK,
                        font_size=20, font_color='black',
                        background_color='red',
                        float=True, margin=(-40,20),
                        selection_color='purple'
                        )
        self.play_menu.add.button('Exit', pygame_menu.events.EXIT,
                        #align=pygame_menu.locals.ALIGN_LEFT,
                        font_size=20, font_color='black',
                        background_color='red',
                        float=True, margin=(-150,20),
                        selection_color='purple'
                        )

    def prep_menu(self):

        global clock
        global main_menu
        global surface

        surface = create_example_window('Lost in woods', (WINDOW_WIDTH,WINDOW_HEIGHT))
        clock = pygame.time.Clock()


        self.prep_play_menu()

        main_theme = pygame_menu.Theme(background_color=(12, 0, 0, 0),
                            title_background_color=(4, 47, 126),
                            title_font_shadow=True,
                            widget_padding=10,
                            #widget_font = pygame_menu.font.FONT_DIGITAL,
                            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE)

        main_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT,
            theme=main_theme,
            title='Main Menu',
            width=WINDOW_WIDTH,
            column_max_width=WINDOW_WIDTH,
            column_min_width=1,
        )

        main_menu.add.label("WELCOME TO THE GAME", max_char=-1, font_size=40)
        main_menu.add.image("./assets/ninja1.png", angle=10, scale=(2,2))
                 
        main_theme.widget_font_size = 19

        main_menu.add.dropselect('Difficulty Level',
                            [('Easy', 'EASY'),
                            ('Medium', 'MEDIUM'),
                            ('Hard', 'HARD')],
                        default=(0),
                        onchange=self.change_difficulty,
                        dropselect_id='select_difficulty',
                        placeholder_add_to_selection_box=False,
                        selection_box_bgcolor=(173,38,226,200),
                        selection_option_selected_bgcolor=(188, 227, 244),
                        selection_option_selected_font_color=(0,45,46),
                        )

        main_menu.add.button('Start', self.play_menu,
                            font_size=20, font_color='black',
                            background_color='green',
                            margin=(50,-200),selection_color='purple',
                            )
        main_menu.add.button('Exit', pygame_menu.events.EXIT,
                            font_size=20, font_color='black',
                            background_color='red',
                            float=True, margin=(-30,20),
                            selection_color='purple')

    def prev_stats(self):
        data0 = [0 for i in range(3)]
        data1 = [0 for i in range(3)]
        data2 = [0 for i in range(3)]
        try:
            with open('./scores0.txt') as f:
                lines = f.readlines()
                for k,v in enumerate(lines):
                    data0[k] = round(float(v.strip()))
            with open('./scores1.txt') as f:
                lines = f.readlines()
                for k,v in enumerate(lines):
                    data1[k] = round(float(v.strip()))
            with open('./scores2.txt') as f:
                lines = f.readlines()
                for k,v in enumerate(lines):
                    data2[k] = round(float(v.strip()))
        except:
            pass
    
        self.stats = [ 
            Stats('EASY',data0[0],data0[1],data0[2]),
            Stats('MEDIUM',data1[0],data1[1],data1[2]),
            Stats('HARD',data2[0],data2[1],data2[2]),
        ]



    def start(self):
        pygame.init()
        pygame.mixer.init()
        self.prev_stats()
        self.prep_menu()
        pygame.mixer.music.load('./assets/playback.mp3')
        pygame.mixer.music.play(loops=0)
      
        while True:

            # Tick
            clock.tick(FPS)

            # Paint background
            self.background()

            # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            # Main menu
            if main_menu.is_enabled():
                main_menu.mainloop(surface, self.background, disable_loop=False, fps_limit=FPS)

            # Flip surface
            pygame.display.flip()