"""
graphics engine for 2D games
"""
import random 
import os
import numpy as np
import cv2
from game import start_game, move_player, update
from pygame import mixer


mixer.init()
mixer.music.load("awesomeness.mp3")
mixer.music.play(loops=-1)

import cv2

# Function to display an image with centered text and wait for a key press
def display_screen(image_path, window_name, text_lines=None):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error loading image {image_path}")
        return

    # Add text to the image
    if text_lines:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0  # Adjust this value to change text size
        font_color = (255, 255, 255)  # White color in BGR format
        line_thickness = 2

        # Calculate total height required for all lines of text
        total_text_height = 0
        for line in text_lines:
            # Get the size of the text to be placed
            text_size, _ = cv2.getTextSize(line, font, font_scale, line_thickness)
            total_text_height += text_size[1] + 10  # Add some space between lines (10 pixels)

        # Calculate the starting y position to center vertically
        text_y = (img.shape[0] - total_text_height) // 2

        # Render each line of text
        for line in text_lines:
            # Get the size of the text to be placed
            text_size, _ = cv2.getTextSize(line, font, font_scale, line_thickness)

            # Calculate position to center the text horizontally
            text_x = (img.shape[1] - text_size[0]) // 2

            # Add text to the image
            text_position = (text_x, text_y)
            img = cv2.putText(img, line, text_position, font, font_scale, font_color, line_thickness, cv2.LINE_AA)

            # Move down to the next line
            text_y += text_size[1] + 10  # Add some space between lines (10 pixels)

    # Display the image
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Main function to demonstrate usage
def main():
    # Display title screen with "Press any key to start"
    title_image_path = 'titleimage.png'
    display_screen(title_image_path, "Title Screen", ["Press any key to start"])

    # Display instructions screen
    instructions_image_path = 'instructions.png'
    instructions_text = [
       
        "You are about to enter the dungeon......",
        "Tips :",
        "1) Dodge fireballs and escape from skeletons.",
        "2) Potions restore health.",
        "3) Keys open doors.",
        "4) Collect as many coins as you can!"
    ]
    display_screen(instructions_image_path, "Instructions", instructions_text)

if __name__ == "__main__":
    main()


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
screen = cv2.namedWindow(GAME_TITLE, cv2.WND_PROP_FULLSCREEN)
screen_size_x = int(cv2.getWindowProperty(GAME_TITLE, cv2.WND_PROP_FULLSCREEN))
screen_size_y = int(cv2.getWindowProperty(GAME_TITLE, cv2.WND_PROP_FULLSCREEN))
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

def write_text(
        frame,
        text:str,
        position :(int,int)):
    cv2.putText(frame,
               text,
               position,
               fontFace=cv2.FONT_HERSHEY_SIMPLEX,
               fontScale=1.5,
               color=(95, 200, 150),
               thickness=3, )

def draw(game, images):
    # initialize screen
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)

    write_text(frame,str(game.coins),(1343, 60))
    write_text(frame,str(game.bow),(1350,420))
    write_text(frame,str(game.short_sword),(1350,510))
    write_text(frame,str(game.bullets),(1350,610))
    

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
        "/":"scroll",
        "s":"stairs_down",
        "b":"bow",
        "|":"short_sword",
        "r":"ring",
        "T":"statue",
        "L":"long_sword"
    
    }
    # draw dungeon tiles,wall,fountain,dragon,stairs_up,coin
    for y, row in enumerate(game.current_level.level):
        for x, tile in enumerate(row):
            draw_tile(frame, x=x, y=y, image=images[SYMBOLS[tile]])

     #draw switch
    for t in game.current_level.switches:
        if t.flag==True:
            draw_tile(frame, x=t.x, y=t.y, image=images["prompt_yes"])
        else :
            draw_tile(frame, x=t.x, y=t.y, image=images["prompt_no"])
    
    #draw elf
    for t in game.current_level.elf:
        draw_tile(frame, x=t.x, y=t.y, image=images["elf_archer"])

    # draw teleporters
    for t in game.current_level.teleporters:
        draw_tile(frame, x=t.x, y=t.y, image=images["teleporter"])

    #draw all monsters
    Elements=[
        [game.current_level.fireballs, "fireball"],
        [game.current_level.skeletons, "skeleton"],
        [game.current_level.undead, "undead"],
        [game.current_level.eyes,"eye"],
        [game.current_level.rats,"rat"],
        [game.current_level.snakes,"snake"],
        [game.current_level.dragon,"dragon"]
          ]
    for monsters,imagename in Elements :
        for m in monsters :
            draw_tile(frame, x=m.x, y=m.y, image=images[imagename])
     # draw coin icon
    draw_tile(frame, x=10, y=0, image=images["coin"], xbase=750, ybase=15)
    # draw bow icon 
    draw_tile(frame, x=10, y=0, image=images["bow"], xbase=750, ybase=370)
    # draw short sword icon
    draw_tile(frame, x=10, y=0, image=images["short_sword"], xbase=750, ybase=465)
    #draw bullet icon
    draw_tile(frame, x=10, y=0, image=images["fireball"], xbase=750, ybase=568)
    # draw player
    if game.elf_flag==True :
        draw_tile(frame, x=game.x, y=game.y, image=images["elf_archer"])
    else :
        draw_tile(frame, x=game.x, y=game.y, image=images["player"])
    # draw the health bar
    frame[190 : 190 + game.health, 1375:1435] = (70, 50, 255)
    # put a heart symbol next to health
    draw_tile(frame, x=10, y=1, image=images["heart"], xbase=732, ybase=45)
    # display the inventory
    for i, item in enumerate(game.items):
        y = i // 2  # floor division: rounded down
        x = i % 2  # modulo: remainder of an integer division
        draw_tile(frame, xbase=1340, ybase=670, x=x, y=y, image=images[item])
    
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
    if game.current_level=="THREE" :
        if counter%10==0:
            update(game)
    else  :
            if(counter%30==0):
                update(game)
    handle_keyboard(game)

cv2.destroyAllWindows()

