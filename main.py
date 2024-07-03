"""
graphics engine for 2D games
"""
import os
import numpy as np
import cv2
from game import start_game, move_player


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
SCREEN_SIZE_X, SCREEN_SIZE_Y = 840, 640
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
    cv2.putText(frame,
            str(game.coins),
            org=(730, 78),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.5,
            color=(95, 200, 150),
            thickness=3,
            )
    
     #draw coin icon 
    draw_tile(frame, x=10, y=0, image=images["coin"], xbase=20, ybase=35)
     # draw dungeon tiles
    for y, row in enumerate(game.level):
        for x, tile in enumerate(row):
            if tile == ".":
                draw_tile(frame, x=x, y=y, image=images["floor"])
            if tile == "#":
                draw_tile(frame, x=x, y=y, image=images["wall"])
            if tile == "F":
                draw_tile(frame, x=x, y=y, image=images["fountain"])
            if tile == "D":
                draw_tile(frame, x=x, y=y, image=images["dragon"])
            if tile == "S":
                draw_tile(frame, x=x, y=y, image=images["stairs_up"])
            if tile == "$":
                draw_tile(frame, x=x, y=y, image=images["coin"])
     # draw player
    draw_tile(frame, x=game.x, y=game.y, image=images["player"])
    # draw the heath bar
    frame[130:50 + game.health, 730:830] = (70, 50, 255)
    # put a heart symbol next to health
    draw_tile(frame, x=10, y=1, image=images["heart"], xbase=19, ybase=50)
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
while game.status == "running":

    draw(game, images)
    # health check
    def update(game):
        if game.health <= 0:
            game.status = "game over"
    handle_keyboard(game)

cv2.destroyAllWindows()
