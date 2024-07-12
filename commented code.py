commented code 

SKELETON
for s in game.current_level.skeletons:
        while True:
            dir = random.choice(["up", "down", "left", "right"])
            x, y = get_next_position(s.x, s.y, dir)
            if game.current_level.level[y][x] in ".€k":
                s.x, s.y = x, y
                break
other stuff to add and do :
music 
screens
animations
reorganize and rearrange 

to add in level 2:
eye 
undead gaurding the door 
knight able to move through undead 
remove dead undead 

to add in level 3 :
sheild feature 
bullets 
undead (only knight )
rat gaurding the sheild 
snake is caged
use key to let snake out and it eats rat
skeletons
fireballs
traps around coins


snake 
OLD Code 
"""
the Dungeon Explorer game logic
"""
'''from logging import _Level
import random
from pydantic import BaseModel

class Teleporter(BaseModel):
    x: int
    y: int
    target_x: int
    target_y: int

class Fireball(BaseModel):
    x:int 
    y:int
    dir:str

class Skeleton(BaseModel) :
    x:int
    y:int
    dir:str

class DungeonGame(BaseModel):
    status: str = "running"
    x: int
    y: int
    coins: int = 0
    health: int= 200
    items: list[str] = []
    current_level: _Level
    
class Level(BaseModel):
    level: list[list[str]]
    teleporters: list[Teleporter] = []
    fireballs: list[Fireball] = []
    skeletons: list[Skeleton] = []


def move_player(game, direction: str) -> None:
    """Things that happen when the player walks on stuff"""
    x = game.x
    y = game.y
    flag=False # to identify teleporters when encountered

    #basic moves
    if direction == "right" and x<20 :
        x += 1
    elif direction == "left" and  x>0 :
        x -= 1
    elif direction== "up" and y>0 :
        y-=1
    elif direction == "down" and  y< 20 :
        y+=1

    #collect keys
    if game.level[y][x]=="K" :
        game.items.append("key")
        game.level[y][x]="."

    #open doors with keys 
    if "key" in game.items and game.level[y][x]=="d":  # check whether there is a door
        game.items.remove("key")     # key can be used once
        game.level[y][x]="D"  # replace the closed door by an open one

    #collect coins 
    if game.level[y][x] == "$":
        game.level[y][x] = "."
        game.coins+=1

    #health refilling potion
    if game.level[y][x]=="P":
        game.level[y][x]="."
        game.health+=12

    #traps
    if game.level[y][x] == "X":
        game.level[y][x] = "."
        game.health-=17

    #basic moves
    if game.level[y][x] == "." or game.level[y][x]=="D" or flag:
        if game.level[y][x]=="D":
            game.level[y][x]="."
        game.x = x
        game.y =y
        flag=False

    #teleporter move
    check_teleporters(game)
     
    for f in game.fireballs:
        if f.x == game.x and f.y==game.y:
            game.health -= 15

    for f in game.skeletons:
        if f.x == game.x and f.y==game.y:
            game.health -= 10

    
    #when stairs are found
    if game.level[y][x] == "S":
        game.status = "finished"

def start_game():
    
    level_one=Level(
        level= parse_level([
                "#####################",
                "#..K...#.$..........#",
                "#F.....#.$..........#",
                "#XX$$$X#............#",
                "#...####.K..........#",
                "#..X#$XXX...........#",
                "#...#...X...........#",
                "#d#.#...............#",
                "#P#.#..$........K..##",
                "##.X$$X.$..........#S",
                ".....................",
                "#####################"
                ]),
        teleporters=[Teleporter(x=3, y=1, target_x=5, target_y=8),],
        fireballs=[Fireball(x=9,y=7,dir="right"),],
        skeletons=[Skeleton(x=1,y=6,dir="up"),],
        )

    return DungeonGame(
        x=8,
        y=1,
        current_level=level_one
    )
# **** TELEPORTER STUFF ****
def check_teleporters(game):
    for t in game.current_level.teleporters:
        if game.x == t.x and game.y==t.y:
            flag=True
            game.x = t.target_x 
            game.y=t.target_y


#   **FIREBALL STUFF**
#get next position of fireball
def get_next_position(x,y,z) :
    if z=="right":
        x+=1
    elif z=="left":
        x-=1
    elif z=="up":
        y+=1
    else :
        y-=1
    return x,y

# move fireballs
def move_fireball(game):
    for f in game.fireballs:
        x, y = get_next_position(f.x, f.y, f.dir)
        if game.level[y][x] in ".€k":  # flies over coins and keys
            f.x, f.y = x,y
        elif f.dir=="right":
            f.dir="left"
            x,y=get_next_position(f.x,f.y,f.dir)
            f.x,f.y=x,y
        elif f.dir=="left":
            f.dir="right"
            x,y=get_next_position(f.x,f.y,f.dir)  
            f.x,f.y=x,y

# make fireball do damage 
def check_collision(game):
    for f in game.fireballs:
        if f.x == game.x and f.y==game.y:
            game.health -= 15

# ***** END OF FIREBALL STUFF *****

# ***** SKELETON STUFF ******
def move_skeleton(game):
    for s in game.skeletons:
        dir = random.choice(["up", "down", "left", "right"])
        x,y=get_next_position(s.x,s.y,dir)
        if game.level[y][x] in ".€k":  # flies over coins and keys
                s.x, s.y = x,y
        elif s.dir=="right":
                s.dir="left"
                x,y=get_next_position(s.x,s.y,s.dir)
                s.x,s.y=x,y
        elif s.dir=="left":
            s.dir="right"
            x,y=get_next_position(s.x,s.y,s.dir)  
            s.x,s.y=x,y

# make skeleton hurt the player
def check_collision_skeleton(game):
    for f in game.skeletons:
        if f.x == game.x and f.y==game.y:
            game.health -= 10

# *****END OF SKELETON STUFF *****



def parse_level(level):
    return [list(row) for row in level]
def update(game):
     # health check
    if game.health <= 0:
        game.status = "game over"
    # move fireball
    move_fireball(game)
    check_collision(game)
    move_skeleton(game)
    check_collision_skeleton(game) # type: ignore
'''

.............
..E..........
.............


eye :
add an eye_counter 
if counter> 4 and next to eye but no scroll  
make another counter
transport to fireball area 
move the player there 
start counter 
till counter=3
make player stand there 

if scroll no curse and eye dissapears

LEVEL_TWO = Level(
    level=parse_level([
           "#####################",
           "#..K...#..$....Xddd.#",
           "#.......#.$$......###",
           "#..$$$..#....$$.....#",
           "#....####..XX.......#",
           "#.X..#####......X...#",
           "#E..#d...X..XX......#",
           "#P#.#..X...$$$..X...#",
           "##....XX...#####.X..#",
           "##.X$$XX$..%.A.#.X..#",
           "#K.X.X.....#####...S#",
           "#####################"
    ]),
    switches=[Switch(x=19,y=1)],
    teleporters=[Teleporter(x=4, y=2, target_x=13, target_y=8), Teleporter(x=9, y=7, target_x=2, target_y=1)],
    fireballs=[Fireball(x=11, y=7, dir="left"), Fireball(x=6, y=5, dir="down")],
    skeletons=[Skeleton(x=2, y=5, dir="down"), Skeleton(x=8, y=4, dir="up"), Skeleton(x=11, y=8, dir="left")],
    undead=[Undead(x=9,y=9,dir="right")],
    eyes=[Eye(x=1,y=6,time_spent=0)]







    armor how to change 
    teleporters 
    how to check if wearing armor
    undead stick to a background



    '''import random 
import os
import numpy as np
import cv2
from game import start_game, move_player, update


# title of the game window
GAME_TITLE = "Dungeon Explorer"

# map keyboard keys to move commands
MOVES = {
    "a": "left",
    "d": "right",
    "w": "up",
    "s": "down",
}

#
# constants measured in pixels
#
SCREEN_SIZE_X, SCREEN_SIZE_Y = 1470,831
TILE_SIZE = 64


def read_image(filename: str) -> np.ndarray:
    """
    Reads an image from the given filename and doubles its size.
    If the image file does not exist, an error is created.
    """
    img = cv2.imread(filename)  # sometimes returns None
    if img is None:
        raise IOError(f"Image not found: '{filename}'")
    img = np.kron(img, np.ones((2, 2, 1), dtype=img.dtype))  # double image size
    return img


def read_images():
    return {
        filename[:-4]: read_image(os.path.join("tiles", filename))
        for filename in os.listdir("tiles")
        if filename.endswith(".png")
    }


def draw_tile(frame, x, y, image, xbase=0, ybase=0):
    # calculate screen position in pixels
    xpos = xbase + x * TILE_SIZE
    ypos = ybase + y * TILE_SIZE

    # Ensure the frame slice can hold the image
    if ypos + TILE_SIZE > frame.shape[0] or xpos + TILE_SIZE > frame.shape[1]:
        raise ValueError("Tile position is out of frame bounds")

    # copy the image to the screen
    frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = image


def draw(game, images):
    # Initialize screen with the correct dimensions
    num_rows = len(game.current_level.level)
    num_cols = len(game.current_level.level[0])
    frame_height = num_rows * TILE_SIZE
    frame_width = num_cols * TILE_SIZE
    frame = np.zeros((frame_height, frame_width, 3), np.uint8)

    cv2.putText(
        frame,
        str(game.coins),
        org=(1350, 120),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1.5,
        color=(95, 200, 150),
        thickness=3,
    )
    SYMBOLS = {
        ".": "floor",
        "#": "wall",
        "F": "fountain",
        "&": "dragon",
        "S": "stairs_up",
        "$": "coin",
        "X": "trap",
        "K": "key",
        "D": "open_door",
        "d": "closed_door",
        "P": "potion",
    }
    # draw dungeon tiles,wall,fountain,dragon,stairs_up,coin
    for y, row in enumerate(game.current_level.level):
        for x, tile in enumerate(row):
            draw_tile(frame, x=x, y=y, image=images[SYMBOLS[tile]])
    # draw teleporters
    for t in game.current_level.teleporters:
        draw_tile(frame, x=t.x, y=t.y, image=images["teleporter"])
    # draw fireballs 
    for t in game.current_level.fireballs:
        draw_tile(frame,x=t.x,y=t.y,image=images["fireball"])
    # draw skeleton
    for t in game.current_level.skeletons:
        draw_tile(frame,x=t.x,y=t.y,image=images["skeleton"])
    # draw coin icon
    draw_tile(frame, x=10, y=0, image=images["coin"], xbase=750, ybase=65)
    # draw player
    draw_tile(frame, x=game.x, y=game.y, image=images["player"])
    # draw the health bar
    frame[240 : 240 + game.health, 1375:1435] = (70, 50, 255)
    # put a heart symbol next to health
    draw_tile(frame, x=10, y=1, image=images["heart"], xbase=730, ybase=100)
    # display the inventory
    for i, item in enumerate(game.items):
        y = i // 2  # floor division: rounded down
        x = i % 2  # modulo: remainder of an integer division
        draw_tile(frame, xbase=1340, ybase=500, x=x, y=y, image=images[item])
    for dmg in game.damages :
        if dmg.counter>0:
            #draw tile(frame, x=dmg.x, y=dmg.y, image=images[dmg.image-name])
            cv2.putText(frame,
                        dmg.text,
                        org=(TILE_SIZE*dmg.x, TILE_SIZE*dmg.y),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1.5,
                        color=(128,128,255),
                        thickness=4,
            )
            dmg.counter-=1
    # display complete image
    cv2.imshow(GAME_TITLE, frame)


def handle_keyboard(game):
    """keys are mapped to move commands"""
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        game.status = "exited"
    if key in MOVES:
        move_player(game, MOVES[key])


# game starts
images = read_images()
game = start_game()
counter=0
while game.status == "running":
    counter+=1
    draw(game, images)
    # health check
    if counter%10==0 :
        update(game)
    handle_keyboard(game)

cv2.destroyAllWindows()'''

8



final level 
dragon- chases player but not that fast. spits fireballs.  D
fireballs dissapear when hit walls. doesnt affect any other components of game and can fly over evrything.moves in one direction only.
dragon can only be killed with longsword
bullets to reduce health and after health reduces no dragon doesnt chase for about 5 seconds
armour- locked behind door. can be collected and when A key is pressed becomes active. armor has a health. protects aginst fireballs
sheild 
slime reduces speed 
long sword gaurded with spells - scroll-eye , doors , and fountain-coins. should be positioned at an end.
bats spawn suddenly in the next tile but does not move. sometimes bats block way. can choose to kill or not and reduce health - short sword kills, if no shortsword then health reduce. armor has no effect.
cursor control



def collect_bullets(game) :
     for b in game.current_level.bullets:
            if b.x == game.x and b.y == game.y:
                game.bullets+=1

def fire_bullet(game, target_x, target_y):
    direction = calculate_direction_towards_target(game.x, game.y, target_x, target_y)
    bullet = Bullet(x=game.x, y=game.y, dir=direction, range=5)  # Adjust range as needed
    game.current_level.fireballs.append(bullet)

def move_bullets(game):
    new_fireballs = []
    for b in game.current_level.bullets:
        if b.distance_travelled < b.range:
            new_x, new_y = get_next_position(b.x, b.y, b.dir)
            if game.current_level.level[new_y][new_x] in ".D":
                b.x, b.y = new_x, new_y
                b.distance_travelled += 1
                new_fireballs.append(b)
            # Check for collision with dragon
            for d in game.current_level.dragon:
                if b.x == d.x and b.y == d.y:
                    d.chase_cooldown = 4 * 60  # Freeze for 4 seconds 
        else:
            # Fireball has reached its range limit
            pass
    game.current_level.fireballs = new_fireballs

def check_bullet_collision(game):
    for b in game.current_level.bullets:
        for d in game.current_level.dragon:
            if b.x == d.x and b.y == d.y:
                d.chase_cooldown = 4 * 60  # Freeze for 4 seconds 
                game.current_level.fireballs.remove(b)

# Firing bullets with cursor click
def handle_cursor_click(game, cursor_x, cursor_y):
    fire_bullet(game, cursor_x, cursor_x)



     "#S###################",
           "#..K....#.$...#.ddd.#",
           "#.......#.$$..#.#####",
           "#..$$...#....$#.....#",
           "#.......#..XX.#.....#",
           "#.X.#####.....#.X...#",
           "#...#d...X..XX#.....#",
           "#P#.#..X...$$$..X...#",
           "##..#.XX...#####XXX.#",
           "##.X$$XX$..#...#....#",
           "#K.X.X..../#####...s#",
           "#####################"


           def move_fireball(game):
    for f in game.current_level.fireballs:
        x, y = get_next_position(f.x, f.y, f.dir)
        if game.current_level!= "LEVEL_FOUR" :
            if game.current_level.level[y][x] in ".$k":
                f.x, f.y = x, y
            else:
                if f.dir == "right":
                    f.dir = "left"
                elif f.dir == "left":
                    f.dir = "right"
                elif f.dir=="up" :
                    f.dir="down"
                else :
                    f.dir="up"
                x, y = get_next_position(f.x, f.y, f.dir)
                f.x, f.y = x, y