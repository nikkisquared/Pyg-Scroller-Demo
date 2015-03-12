#!/usr/bin/python

import pygcurse
import drawing, movement, settings
# sys is used for exiting the program, nothing else
import sys

# needed for compiling as an exe [BROKEN]
#import pygame._view
import pygame
from pygame import key
from pygame.locals import *


info = settings.Settings()
drawing.make_objects(info)

win = pygcurse.PygcurseWindow(info.width, info.height)
win.setscreencolors(info.fgcolor, info.bgcolor)
# disables autoupdate to prevent flickering
win.autoupdate = False
box = pygcurse.PygcurseTextbox(win, (0, 0, info.width, info.textbox_height),
                                fgcolor="black", bgcolor="white", border=None)

# saves the width/length (they are equal) of cells in pixels
PIXELS_PER_CELL = win.cellwidth


def pygame_events(view_X, view_Y, displayText):
    """Runs through pygame events"""


    for event in pygame.event.get():

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            syinfo.exit()

        # returns the character in and the colours of the cell clicked on
        if "DEBUG" in info.run and event.type == MOUSEBUTTONDOWN:
            
            displayText = ""

            cell_X, cell_Y = win.getcoordinatesatpixel(event.pos)
            char = win.getcharatpixel(cell_X * PIXELS_PER_CELL, cell_Y * PIXELS_PER_CELL)
            colors = win.getdisplayedcolors(cell_X, cell_Y)

            string = "You just clicked on a '%s' at cell X:%s Y:%s"
            displayText += string % (char, cell_X + view_X, cell_Y + view_Y)
            string = "\nThe fg color values are: R:%s G:%s B:%s"
            displayText += string % (colors[0][0], colors[0][1], colors[0][2])
            string = "\nThe bg color values are: R:%s G:%s B:%s"
            displayText += string % (colors[1][0], colors[1][1], colors[1][2])

    return displayText


def get_surrounding_colors(player_X, player_Y):
    """Creates a list of dicts of colors around the player's current position"""

    wall_grid = []

    for x in (-1, 0, 1):
        newRow = []
        for y in (-1, 0, 1):
            newRow.append( win.getdisplayedcolors(player_X + x, player_Y + y)[1] )
        wall_grid.append(newRow)

    return wall_grid


def write_text(win, view_X, view_Y, player_X, player_Y, displayText):
    """Writes important text to the screen"""

    # only writes to the textbox if wanted
    if info.textbox_height > 0:
        box.text = "# = X:%s Y:%s" % (view_X, view_Y)
        if "RPG" in info.run:
            box.text += " You are at X:%s Y:%s" % (player_X, player_Y)
        box.update()

    win.putchars(displayText, x = 0, y = 1)


def main():
    """Runs everything from here"""

    # view axes are used against locations of objects/map parts, and laid onto the screen
    view_X = info.max_x / 4
    view_Y = int(info.max_y / 2.5) - info.textbox_height

    # player directions are relative to the -screen-
    player_X = info.width / 2
    player_Y = info.height / 2
    # what directions the player can move in, and thusly what the view can not move along
    playerDirs = ''
    # if the cell the player is trying to move into is a wall
    isWall = False

    # keeps track of time
    mainClock = pygame.time.Clock()
    # information to show to the user in top-screen textbox
    displayText = ""

    # loops until user quit
    while True:

        # runs through pygame events, and gets the current text to display
        displayText = pygame_events(view_X, view_Y, displayText)

        # adjusts view and player position, depending on scrolling type
        if info.scroll_type == "MOUSE" and hasattr(event, "pos"):
            cell_X, cell_Y = win.getcoordinatesatpixel(event.pos)
            view_X, view_Y = movement.shift_view_mouse(info, view_X, view_Y, cell_X, cell_Y)

        elif info.scroll_type == "KB":
            keys = key.get_pressed()
            if "RPG" in info.run:
                wall_grid = get_surrounding_colors(player_X, player_Y)
                move = movement.player(info, keys, view_X, view_Y, player_X, player_Y, wall_grid)
                view_X, view_Y, player_X, player_Y = move
                
            else:
                view_X, view_Y = movement.shift_view_kb(keys, view_X, view_Y, playerDirs)

        view_X, view_Y = movement.check_view_boundaries(info, view_X, view_Y)
        
        # draws everything to the screen
        # completely blanks the map to begin with
        win.fill(bgcolor = info.bgcolor)
        drawing.draw_objects(win, view_X, view_Y)
        drawing.draw_map(win, info, view_X, view_Y)
        write_text(win, view_X, view_Y, player_X, player_Y, displayText)

        if "RPG" in info.run:
            win.putchars('@', x = player_X, y = player_Y)

        # manually updates the window
        win.update()
        # keeps the program update speed down
        mainClock.tick(info.FPS)

main()