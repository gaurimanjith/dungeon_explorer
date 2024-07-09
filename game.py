
import random
from pydantic import BaseModel

class Switch(BaseModel):
    x:int
    y:int

class Teleporter(BaseModel):
    x: int
    y: int
    target_x: int
    target_y: int

class Fireball(BaseModel):
    x: int
    y: int
    dir: str

class Skeleton(BaseModel):
    x: int
    y: int
    dir: str

class Undead(BaseModel):
    x:int
    y:int
    dir:str

class Eye(BaseModel):
    x:int
    y:int
    time_spent:int

class Level(BaseModel):
    level: list[list[str]]
    teleporters: list[Teleporter] = []
    fireballs: list[Fireball] = []
    skeletons: list[Skeleton] = []
    undead:list[Undead]=[]
    switches: list[Switch]=[]
    eyes:list[Eye]=[]

class DungeonGame(BaseModel):
    status: str = "running"
    x: int
    y: int
    coins: int = 0
    health: int = 150
    items: list[str] = []
    current_level: Level
    level_number: int = 0

def parse_level(level):
    return [list(row) for row in level]

# Define levels as global variables
LEVEL_ONE = Level(
        level=parse_level([
            "#####################",
            "#..K...#.$..........#",
            "#F.....#.$..........#",
            "#XX$$$X#............#",
            "#...####.K..........#",
            "#..X#$XXX...........#",
            "#...#...X...........#",
            "#d#.#...............#",
            "#P#.#..$........K..##",
            "##.X$$X.$...........S",
            "#...................#",
            "#####################"
        ]),
        teleporters=[Teleporter(x=3, y=1, target_x=5, target_y=8)],
        fireballs=[Fireball(x=9, y=7, dir="right")],
        skeletons=[Skeleton(x=1, y=6, dir="up")],
       
        
    )
LEVEL_TWO = Level(
    level=parse_level([
           "#####################",
           "#..K...#..$....Xddd.#",
           "#.......#.$$......###",
           "#..$$$..#....$$.....#",
           "#....####..XX.......#",
           "#.X..#####......X...#",
           "#...#d...X..XX......#",
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

)
LEVEL_THREE = Level(
    level=parse_level([
        "#####################",
        "#...................#",
        "#...................#",
        "#...................#",
        "#...................#",
        "#...................#",
        "#...................#",
        "#...................#",
        "#...................#",
        "#...................#",
        "#...................#",
        "#####################"
    ]),
    teleporters=[],
    fireballs=[],
    skeletons=[],
    eyes=[Eye(x=3,y=1,time_spent=0)]
)
LEVELS = [LEVEL_ONE, LEVEL_TWO, LEVEL_THREE]
def start_game():
    # Create the game with starting player attributes and the first level
    return DungeonGame(
        x=8,  # Starting x position of the player
        y=1,  # Starting y position of the player
        current_level=LEVEL_ONE  # The level the player starts in
    )

# Functions to move player, fireballs, and skeletons, and to check collisions
def get_next_position(x, y, dir):
    if dir == "right":
        x += 1
    elif dir == "left":
        x -= 1
    elif dir == "up":
        y -= 1
    elif dir == "down":
        y += 1
    return x, y

def move_fireball(game):
    for f in game.current_level.fireballs:
        x, y = get_next_position(f.x, f.y, f.dir)
        if game.current_level.level[y][x] in ".€k":
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

def move_skeleton(game):
   for s in game.current_level.skeletons:
        while True:
            dir = random.choice(["up", "down", "left", "right"])
            x, y = get_next_position(s.x, s.y, dir)
            if game.current_level.level[y][x] in ".€k":
                s.x, s.y = x, y
                break
def move_undead(game):
    for u in game.current_level.undead:
        while True:
            dir = random.choice(["up", "down", "left", "right"])
            x, y = get_next_position(u.x, u.y, dir)
            if game.current_level.level[y][x] in ".€k":
                u.x, u.y = x, y
                break
def eye(game):
    for e in game.current_level.eyes:
       if "scroll" in game.items :
            game.items.remove("scroll")
             
       if (e.x==game.x-1) or (e.x==game.x+1) or (e.y==game.y-1) or (e.y==game.y+1) :
           e.time_spent+=1
           if(e.time_spent>30):
            curse_time=0
            while curse_time<40 :
               game.x=6
               game.y=4
               curse_time+=1


def check_collision(game):
    for f in game.current_level.fireballs:
        if f.x == game.x and f.y == game.y:
            game.health -= 15

def check_collision_skeleton(game):
    for s in game.current_level.skeletons:
        if s.x == game.x and s.y == game.y:
            game.health -= 10
def check_collision_undead(game):
    for u in game.current_level.undead:
            if u.x == game.x and u.y == game.y:
                game.health -= 10

def openswitchdoor(game):
    for s in game.current_level.switches:
        if game.x==s.x and game.y==s.y :
                game.current_level.level[11][10]="."


def move_player(game, direction: str) -> None:
    x, y = game.x, game.y

    if direction == "right" and x < len(game.current_level.level[0]) - 1:
        x += 1
    elif direction == "left" and x > 0:
        x -= 1
    elif direction == "up" and y > 0:
        y -= 1
    elif direction == "down" and y < len(game.current_level.level) - 1:
        y += 1

    if game.current_level.level[y][x] == "K":
        game.items.append("key")
        game.current_level.level[y][x] = "."
    elif "key" in game.items and game.current_level.level[y][x] == "d":
        game.items.remove("key")
        game.current_level.level[y][x] = "D"
    elif game.current_level.level[y][x] == "$":
        game.current_level.level[y][x] = "."
        game.coins += 1
    elif game.current_level.level[y][x] == "P":
        game.current_level.level[y][x] = "."
        game.health += 12
    elif game.current_level.level[y][x] == "X":
        game.current_level.level[y][x] = "."
        game.health -= 17
    if game.current_level.level[y][x] == "A":
        game.items.append("armor")
        game.current_level.level[y][x] = "."
    if game.current_level.level[y][x] in ".D":
        game.x, game.y = x, y

    check_teleporters(game)
    check_collision(game)
    check_collision_skeleton(game)
    check_collision_undead(game)

    if game.current_level.level[y][x] == "S":
        game.level_number += 1
    if game.level_number < len(LEVELS):
        # move to next level
        game.current_level = LEVELS[game.level_number]
    else:
        # no more levels left
        game.status = "finished"

def check_teleporters(game):
    for t in game.current_level.teleporters:
        if game.x == t.x and game.y == t.y:
            game.x, game.y = t.target_x, t.target_y


def update(game):
    if game.health <= 0:
        game.status = "game over"
    move_fireball(game)
    check_collision(game)
    move_skeleton(game)
    check_collision_skeleton(game)
    check_collision_undead(game)
    eye(game)

# Example of how to use the start_game function
game = start_game()



    
    