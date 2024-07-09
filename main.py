"""
graphics engine for 2D games
"""
import random 
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
    # copy the image to the screen
    frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = image


def draw(game, images):
    # initialize screen
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)
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
        "%": "slot",
        "A": "armor"
    }
    # draw dungeon tiles,wall,fountain,dragon,stairs_up,coin
    for y, row in enumerate(game.current_level.level):
        for x, tile in enumerate(row):
            draw_tile(frame, x=x, y=y, image=images[SYMBOLS[tile]])
     #draw switch
    for t in game.current_level.switches:
        draw_tile(frame, x=t.x, y=t.y, image=images["prompt_no"])
    # draw teleporters
    for t in game.current_level.teleporters:
        draw_tile(frame, x=t.x, y=t.y, image=images["teleporter"])
    # draw fireballs 
    for t in game.current_level.fireballs:
        draw_tile(frame,x=t.x,y=t.y,image=images["fireball"])
    # draw skeleton
    for t in game.current_level.skeletons:
        draw_tile(frame,x=t.x,y=t.y,image=images["skeleton"])
    #draw undead 
    for t in game.current_level.undead:
        draw_tile(frame,x=t.x,y=t.y,image=images["undead"])
    # draw eyes
    for t in game.current_level.eyes:
        draw_tile(frame,x=t.x,y=t.y,image=images["eye"])
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
    if counter%30==0 :
        update(game)
    handle_keyboard(game)

cv2.destroyAllWindows()

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
