
import random
import pygame
from pydantic import BaseModel
from datetime import datetime

#Initialize Pygame mixer
pygame.mixer.init()
# Load sound effects
coin_collect_sound = pygame.mixer.Sound("coin.mp3")
fireball_hit_sound = pygame.mixer.Sound("explosion.mp3")
elf_collect_sound = pygame.mixer.Sound("elf.mp3")
trap_fall_sound = pygame.mixer.Sound("stop.mp3")

class Switch(BaseModel):
    x:int
    y:int
    flag:bool=False

class Elf(BaseModel):
    x:int
    y:int
    flag: bool=False
    time : int=6
   
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

class Rat(BaseModel):
    x:int 
    y:int 
    dir:str
    active:bool=True

class Eye(BaseModel):
    x:int
    y:int
    time_spent:int
    dead:bool=False

class Snake(BaseModel):
    x:int
    y:int
    dir:str

class Dragon(BaseModel):
    x: int
    y: int
    chase_cooldown: int = 0
    active:bool=True

class Level(BaseModel):
    level: list[list[str]]
    teleporters: list[Teleporter] = []
    fireballs: list[Fireball] = []
    skeletons: list[Skeleton] = []
    undead:list[Undead]=[]
    switches: list[Switch]=[]
    eyes:list[Eye]=[]
    rats :list[Rat]=[]
    snakes:list[Snake]=[]
    dragon:list[Dragon]=[]
    elf:list[Elf]=[]

class DungeonGame(BaseModel):
    status: str = "running"
    x: int
    y: int
    coins: int = 0
    health: int = 150
    items: list[str] = []
    current_level: Level
    level_number: int = 0
    short_sword:int=0
    bow:int=0
    bullets:int=0
    elf_flag: bool=False
    max_health : int=150
    weapons : list[str]=[]
    elf_collected_time: datetime = None  # Add this attribute to track time

def parse_level(level):
    return [list(row) for row in level]

 # Define levels as global variables
LEVEL_ONE = Level(
                level=parse_level([
                    "#####################",
                    "#$.K..P#.$....SP.#X$#",
                    "#....$P#.$#...KKK#X$#",
                    "#XX$..X####......#.$#",
                    "#...###K....XXX###$X#",
                    "#..X#$XXX.....##...$#",
                    "#...#..######.#..####",
                    "#d#.#...$$$...#..#.S#",
                    "#r#.#..$......#.$####",
                    "###.$$X.$...........#",
                    "#K.......X$$X.#..$$$#",
                    "#####################"
                ]),
                teleporters=[Teleporter(x=3, y=1, target_x=18, target_y=7)],
                fireballs=[Fireball(x=9, y=7, dir="right"),
                        Fireball(x=1, y=6, dir="up"),
                        Fireball(x=10, y=4, dir="right"),
                        Fireball(x=15, y=8, dir="up"),
                        Fireball(x=11, y=3, dir="up")],
                skeletons=[Skeleton(x=1, y=6, dir="up"),
                        Skeleton(x=11, y=1, dir="down"),
                        Skeleton(x=4, y=10, dir="left"),
                        Skeleton(x=14, y=10, dir="left")],
            
                
            )
LEVEL_TWO = Level(level=parse_level([
                "#####################",
                "#S.K....#.$S..#.ddd.#",
                "#......$#.$$..#.#####",
                "#..$$.$$#....$#.....#",
                "#r......#..XX.#.....#",
                "#.X.#####.....#.X...#",
                "#...#d...X..XX#.....#",
                "#P#.#..X...$$$..X...#",
                "##..#.XX...#####XXX.#",
                "##.X$$XX$..#...#....#",
                "#K.X.X..../#####...s#",
                "#####################"
            ]),
            switches=[Switch(x=19,y=1)],
            teleporters=[Teleporter(x=4, y=2, target_x=13, target_y=7), Teleporter(x=9, y=7, target_x=2, target_y=1)],
            fireballs=[
                Fireball(x=11, y=7, dir="left"),
                Fireball(x=6, y=5, dir="down"),
                Fireball(x=19, y=9, dir="left"),
                Fireball(x=4, y=3, dir="right"),
                Fireball(x=8, y=5, dir="up"),
                Fireball(x=15, y=8, dir="left"),
                Fireball(x=4, y=2, dir="right")
            ],
            skeletons=[Skeleton(x=2, y=5, dir="down"), 
                       Skeleton(x=8, y=4, dir="up"),
                       Skeleton(x=11, y=8, dir="left"),
                       Skeleton(x=3, y=4, dir="down"),
                       Skeleton(x=5, y=3, dir="left")
                       ],
            undead=[
                Undead(x=18, y=9, dir="right"),
                Undead(x=12, y=3, dir="down"),
                Undead(x=5, y=2, dir="left"),
                Undead(x=7, y=6, dir="up"),
                Undead(x=10, y=10, dir="right")
            ],
            eyes=[Eye(x=1,y=6,time_spent=0)],
            elf=[Elf(x=12,y=9)]
        )

LEVEL_THREE = Level(
            level=parse_level([
                "#s###################",    
                "#P..$.#$$$......|..S#",
                "#.|...#.............#",
                "#..$..#....#...PPP..#",
                "#.....#.###.#########",
                "#..$..#......|....d.#",
                "#.K...##########..###",
                "###...#|d......#....#",
                "#.d..###......#..|..#",
                "###.|...K.....#.....#",
                "#P.....$..$..|..$$$.#",
                "#####################"
            
            ]),
            teleporters=[],
            fireballs=[
                Fireball(x=11, y=7, dir="left"), 
                Fireball(x=6, y=5, dir="down"),
                Fireball(x=9, y=7, dir="right"),
                Fireball(x=18, y=5, dir="left")
            ],
            skeletons=[],
            eyes=[],
            rats=[
                Rat(x=4, y=1, dir="right"),
                Rat(x=19, y=9, dir="up"),
                Rat(x=11, y=1, dir="left"),
                Rat(x=15, y=7, dir="left"),
                Rat(x=7, y=6, dir="up")
            ],
            snakes=[Snake(x=1,y=8,dir="up"),Snake(x=19,y=5,dir="left")]
            
        )
LEVEL_FOUR = Level(
            level=parse_level([
                "#####################",
                "#..P.............K..#",
                "#.####.#####.##.#####",
                "#.#K.#.#.L.#.##.....#",
                "#.#....##F##.##.#..P#",
                "#.#..#.#...#.##.#...#",
                "#....#.##d##.##.##.##",
                "#.#..#.##.##P##.#...#",
                "#.#..#.##d##.##.#..K#",
                "#.#..#.##.##.##.#####",
                "#..................P#",
                "#s###################"
            ]),
            teleporters=[Teleporter(x=10, y=2, target_x=4, target_y=6)],
            dragon=[Dragon(x=11, y=1)],
            fireballs=[Fireball(x=8, y=5, dir="right")]

        
        )      

LEVELS = [LEVEL_ONE, LEVEL_TWO, LEVEL_THREE,LEVEL_FOUR]
def start_game():
    # Create the game with starting player attributes and the first level
    return DungeonGame(
        x=8,  # Starting x position of the player
        y=1,  # Starting y position of the player
        current_level=LEVEL_ONE # The level the player starts in
    )

# Functions to move player, fireballs, and skeletons, and to check collisions
def get_next_position(x, y, dir):
    if game.current_level== "FOUR" :  
        if dir == "right":
            x += 2
        elif dir == "left":
            x -= 2
        elif dir == "up":
            y -= 2
        elif dir == "down":
            y += 2
    else :
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
        if game.current_level != "LEVEL_FOUR":
            if game.current_level.level[y][x] in ".$k":
                f.x, f.y = x, y
            else:
                if f.dir == "right":
                    f.dir = "left"
                elif f.dir == "left":
                    f.dir = "right"
                elif f.dir == "up":
                    f.dir = "down"
                else:
                    f.dir = "up"
                x, y = get_next_position(f.x, f.y, f.dir)
                f.x, f.y = x, y
        else:
            # In Level Four, fireballs can move through walls
            f.x, f.y = x, y
            wrap_around(f)

def wrap_around(fireball):
    # Assuming level dimensions are 21x12
    if fireball.x < 0:
        fireball.x = 20
    elif fireball.x > 20:
        fireball.x = 0
    if fireball.y < 0:
        fireball.y = 11
    elif fireball.y > 11:
        fireball.y = 0


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
            if(u==game.current_level.undead[0]):
                if(x<15) :
                    x+=1
                if(y<8):
                    y+=1
            if game.current_level.level[y][x] in ".€k":
                    u.x, u.y = x, y
                    break


def get_opposite_direction(dir):
    if dir == "right":
        return "left"
    elif dir == "left":
        return "right"
    elif dir == "up":
        return "down"
    elif dir == "down":
        return "up"

def move_rat(game):
    for rat in game.current_level.rats:
        if "short_sword" in game.weapons:
            # Run away from the player
            best_direction = None
            max_distance = -1
            for dir in ["up", "down", "left", "right"]:
                x, y = get_next_position(rat.x, rat.y, dir)
                if game.current_level.level[y][x] in ".€k":
                    distance = abs(game.x - x) + abs(game.y - y)
                    if distance > max_distance:
                        best_direction = dir
                        max_distance = distance
            if best_direction:
                rat.x, rat.y = get_next_position(rat.x, rat.y, best_direction)
        else:
            # Chase the player
            best_direction = None
            min_distance = float('inf')
            for dir in ["up", "down", "left", "right"]:
                x, y = get_next_position(rat.x, rat.y, dir)
                if game.current_level.level[y][x] in ".€k":
                    distance = abs(game.x - x) + abs(game.y - y)
                    if distance < min_distance:
                        best_direction = dir
                        min_distance = distance
            if best_direction:
                rat.x, rat.y = get_next_position(rat.x, rat.y, best_direction)





def move_snake(game):
    for s in game.current_level.snakes:
        for i in range(10):
            dir = random.choice(["up", "down", "left", "right"])
            x, y = get_next_position(s.x, s.y, dir)
            if game.current_level.level[y][x] in ".D€k":
                s.x, s.y = x, y
                break
def eye(game):
    for e in game.current_level.eyes:
        if "scroll" in game.items :
            game.items.remove("scroll")
            e.dead=True
        elif (e.x==game.x-1 and e.y==game.y) or (e.x==game.x+1 and e.y==game.y) or (e.y==game.y-1 and e.x==game.x) or (e.y==game.y+1 and e.x==game.x) :
           e.time_spent+=5
           if(e.time_spent>0):
            curse_time=0
            while curse_time<40 :
               game.x=6
               game.y=4
               curse_time+=1

def check_collision(game): #fireball
    if game.elf_flag:  # Check if the elf has been collected
        return  # If so, skip collision checks for fireballs
    for f in game.current_level.fireballs:
        if f.x == game.x and f.y == game.y:
            fireball_hit_sound.play()  # Play fireball hit sound
            game.health -= 15

def check_collision_skeleton(game):
    if game.elf_flag:  # Check if the elf has been collected
        return  # If so, skip collision checks for skeletons
    
    for s in game.current_level.skeletons:
        if s.x == game.x and s.y == game.y:
            trap_fall_sound.play() 
            game.health -= 10

def check_collision_undead(game):
    if game.elf_flag:  # Check if the elf has been collected
        return  # If so, skip collision checks for undead
    for u in game.current_level.undead:
            if u.x == game.x and u.y == game.y:
                trap_fall_sound.play() 
                game.health -= 10

def check_collision_rat(game):
    for s in game.current_level.rats:
        if s.x == game.x and s.y == game.y and ("short_sword" not in game.weapons):
            game.health -= 5
        elif  s.x == game.x and s.y == game.y and ("short_sword" in game.weapons):
            s.active=False
            game.short_sword-=1
            game.weapons.remove("short_sword")

def check_collision_snake(game):
     for s in game.current_level.snakes:
        for r in game.current_level.rats:
            if s.x == r.x and s.y == r.y:
               r.active=False 

def collect_elf(game):
    for e in game.current_level.elf:
        if game.x == e.x and game.y == e.y:
            elf_collect_sound.play()  # Play fireball hit sound
            e.flag = True
            game.elf_flag = True
            game.elf_collected_time = datetime.now()  # Record the time when the elf is collected

def openswitchdoor(game):
    for s in game.current_level.switches:
        if game.x==s.x and game.y==s.y :
                s.flag=True
                game.current_level.level[9][11]="%"
                

def calculate_direction(dragon, player):
    dx = player.x - dragon.x
    dy = player.y - dragon.y
    if abs(dx) > abs(dy):
        return "right" if dx > 0 else "left"
    else:
        return "down" if dy > 0 else "up"

def move_dragon(game):
    for d in game.current_level.dragon:
        if d.chase_cooldown == 0:  # Only chase if not on cooldown
            dx = game.x - d.x
            dy = game.y - d.y
            if abs(dx) > abs(dy):
                if dx > 0:
                    new_x, new_y = d.x + 1, d.y
                else:
                    new_x, new_y = d.x - 1, d.y
            else:
                if dy > 0:
                    new_x, new_y = d.x, d.y + 1
                else:
                    new_x, new_y = d.x, d.y - 1
            
            # Ensure the dragon only moves to valid positions
            if game.current_level.level[new_y][new_x] in ".PK#D":
                d.x, d.y = new_x, new_y

            # Dragon spits fireballs periodically aiming at the player
            if random.randint(0, 10) < 8:
                direction = calculate_direction(d, game)
                game.current_level.fireballs.append(Fireball(x=d.x, y=d.y, dir=direction))
        elif d.chase_cooldown > 0:
            d.chase_cooldown -= 1  # Reduce cooldown over time

def check_collision_dragon(game) :
     for d in game.current_level.dragon :
            if d.x == game.x and d.y == game.y and "long_sword" not in game.items:
                game.health-=60
            elif d.x == game.x and d.y == game.y and "long_sword" in game.items:
                d.active=False

def calculate_direction_towards_target(start_x, start_y, target_x, target_y):
    dx = target_x - start_x
    dy = target_y - start_y
    if abs(dx) > abs(dy):
        return "right" if dx > 0 else "left"
    else:
        return "down" if dy > 0 else "up"



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
        coin_collect_sound.play() 
        game.items.append("key")
        game.current_level.level[y][x] = "."
    
    if game.current_level.level[y][x] == "L":
        game.items.append("long_sword")
        game.current_level.level[y][x] = "."

    elif "key" in game.items and game.current_level.level[y][x] == "d":
        game.items.remove("key")
        game.current_level.level[y][x] = "D"

    if game.current_level.level[y][x] == "/":
        game.items.append("scroll")
        game.current_level.level[y][x] = "."
    
    elif game.current_level.level[y][x] == "$":
        coin_collect_sound.play()  
        game.current_level.level[y][x] = "."
        game.coins += 1

    elif game.current_level.level[y][x] == "b":
        game.current_level.level[y][x] = "."
        game.bow += 1

    elif game.current_level.level[y][x] == "|":
        game.current_level.level[y][x] = "."
        game.short_sword += 1
        game.weapons.append("short_sword")

    elif game.current_level.level[y][x] == "P":
        elf_collect_sound.play()
        game.current_level.level[y][x] = "."
        game.health += 20

    elif game.current_level.level[y][x] == "r":
        game.current_level.level[y][x] = "."
        game.health += 40

    elif game.current_level.level[y][x] == "X":
        trap_fall_sound.play() 
        game.current_level.level[y][x] = "."
        game.health -= 17

    if game.current_level.level[y][x] == "A":
        game.armor_flag=True
        game.current_level.level[y][x] = "."

    if game.current_level.level[y][x] == "F":
        if game.coins>42 :
            game.current_level.level[y][x] = "."

    if game.current_level.level[y][x] in ".%D":
        game.x, game.y = x, y

    check_teleporters(game)
    check_collision(game)
    check_collision_skeleton(game)
    check_collision_undead(game)
    check_collision_rat(game)
    check_collision_snake(game)
    check_collision_dragon(game)
    remove_stuff(game)
    #LEVEL DOWN 
    if game.current_level.level[y][x] == "s":
        game.level_number -=1
        game.current_level=LEVELS[game.level_number]
    #LEVEL UP
    if game.current_level.level[y][x] == "S" and game.current_level==LEVEL_THREE:
        if (game.current_level.rats==[]) :
            game.level_number += 1
    elif game.current_level.level[y][x] == "S" and game.current_level!=LEVEL_THREE:
            game.level_number += 1
    if game.level_number < len(LEVELS):
        # move to next level
        game.current_level = LEVELS[game.level_number]
    else:
        # no more levels left
        game.status = "finished"
        
def remove_stuff(game):
    new=[]
    elf_list=[]
    dragon_list=[]
    eye_list=[]

    for r in game.current_level.rats:
        if r.active  :
            new.append(r)
    game.current_level.rats=new

    for e in game.current_level.eyes:
        if e.dead  :
            eye_list.append(e)
    game.current_level.eyes=eye_list

    for d in game.current_level.dragon:
        if d.active  :
            dragon_list.append(d)
    game.current_level.dragon=dragon_list

    for e in game.current_level.elf :
        if e.flag==False :
            elf_list.append(e)
    game.current_level.elf=elf_list


def check_teleporters(game):
    for t in game.current_level.teleporters:
        if game.x == t.x and game.y == t.y:
            game.x, game.y = t.target_x, t.target_y

def update(game):
    if game.health <= 0:
        game.status = "game over"

    if game.elf_flag:
        elapsed_time = (datetime.now() - game.elf_collected_time).total_seconds()
        if elapsed_time > 10:  # Check if more than 10 seconds have passed
            game.elf_flag = False  # Reset the elf flag
            game.elf_collected_time = None  # Clear the collected time

    openswitchdoor(game)
    move_fireball(game)
    check_collision(game)
    move_skeleton(game)
    check_collision_skeleton(game)
    move_undead(game)
    check_collision_undead(game)
    move_rat(game)
    check_collision_rat(game)
    move_snake(game)
    check_collision_snake(game)
    remove_stuff(game)
    eye(game)
    move_dragon(game)
    check_collision_dragon(game)
    collect_elf(game)
    

# Example of how to use the start_game function
game = start_game()


    
    