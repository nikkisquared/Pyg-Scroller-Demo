#!/usr/bin/python

class Settings:
    """Holds information about all settings in an easy to retrieve place"""


    # what the program is running as: DEBUG, RPG, RPGDEBUG
    run = "RPGDEBUG"

    # scrolling type for program: KB (keyboard), MOUSE (not working)
    scroll_type = "KB"
    # width/height of cell margin for mouse scrolling
    mouse_margin = 2

    # used to limit speed of the program
    FPS = 30
    # cells covered by wall border
    border_size = 3

    # window X dimension
    width = 50
    # window Y dimension
    if "DEBUG" in run:
        height = 28
    elif "RPG" in run:
        height = 26
    # how many Y cells the textbox takes up. set it to 0 to have it not appear
    if "DEBUG" in run:
        textbox_height = 4
    elif "RPG" in run:
        textbox_height = 2

    # default text color
    fgcolor = (255, 255, 255)
    # color to fill screen with
    bgcolor = (0, 0, 0)

    # base for maximum x or y distance that can be seen
    boundary = 100
    # movement boundary limits - can be manually set for special effects
    left_boundary = 0
    right_boundary = boundary
    top_boundary = textbox_height * - 1
    bottom_boundary = boundary

    # reference points from starting view
    center_x = right_boundary / 2
    center_y = bottom_boundary / 2
    max_x = right_boundary
    max_y = bottom_boundary