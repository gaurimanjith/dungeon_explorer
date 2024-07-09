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