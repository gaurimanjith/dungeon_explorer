"""
the Dungeon Explorer game logic
"""
from pydantic import BaseModel


class DungeonGame(BaseModel):
    status: str = "running"
    x: int
    y: int
    level: list[list[str]]
    coins: int = 0
    health: int= 100

def move_player(game, direction: str) -> None:
    """Things that happen when the player walks on stuff"""
    x = game.x
    y = game.y
    
    if direction == "right" and x<9 :
        x += 1
    elif direction == "left" and  x>0 :
        x -= 1
    elif direction== "up" and y>0 :
        y-=1
    elif direction == "down" and  y< 9 :
        y+=1
    if game.level[y][x] == "$":
        game.level[y][x] = "."
        game.coins+=1
    if game.level[y][x] == ".":
        game.x = x
        game.y =y
    if game.level[y][x] == "S":
        game.status = "finished"
    

def start_game():
    return DungeonGame(
        x=8,
        y=1,
        level= parse_level([
                "D..#####.D",
                ".......#..",
                ".F.....#..",
                "..$$$$.#..",
                "...#####..",
                "....$$....",
                "..###...F.",
                "....#.....",
                "....####S.",
                "....$$..$."
                ])
    )
def parse_level(level):
    return [list(row) for row in level]
def update(game):
    # health check
    if game.health <= 0:
        game.status = "game over"