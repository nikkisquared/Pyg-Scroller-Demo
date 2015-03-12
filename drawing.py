#!/usr/bin/python

# a couple functions for drawing to the screen, and a large data dump

import readmap

COLORTABLE, COLORGRID = readmap.read_map()

# holds the large information for character colour data in an easy to read layout

CHAR_COLORS = {
            # most of main road
            (185,) * 3: '=', (163,) * 3: '=',
            # near the center
            (162,) * 3: ['=', (230,) * 3],
            (169,) * 3: ['=', (215,) * 3],
            (170,) * 3: ['=', (195,) * 3],

            # # most of roadside
            (42,) * 3: ['-', (200,) * 3],
            # near the center
            (39,) * 3: ['-', (75,) * 3],
            (32,) * 3: ['-', (75,) * 3],
            (75,) * 3: ['-', (32,) * 3],
                
            # green area
            (62, 218, 31): ['+', (11, 40, 5)],
            (49, 173, 25): '/',
            (45, 167, 23): '\\',
            (142, 207, 49): '^',
            (141, 206, 49): '^',
            (145, 208, 50): 'O',

            # blue area
            (57, 35, 134): '&',
            (55, 27, 131): '>',
            (54, 22, 129): '<',
            (56, 31, 132): '?',

            (): ''
            }


# data for every object to place on the map
OBJECTS = []

def make_objects(info):
    # creates the list of objects

    # posX and posY is relative to the start of 0, 0
    # towards the max_x is rightwards, towards maxy is downwards, towards 0 is leftwards/upwards

    # objects are drawn IN THE ORDER THEY ARE WRITEN

    global OBJECTS

    # fill-in-the-blanks example         
    OBJECTS.append(
                    # the character to fill this with
                    {'char': ' ',
                    # fgcolor (text) and bgcolor colouring
                    'text': 'white', 'color': 'white',
                    # the (x, y) cartesian location of object
                    'posX': 0, 'posY': 0,
                    # how large the object / box is towards the right and bottom
                    'sizeX': 0, 'sizeY': 0})

    # top section of border
    OBJECTS.append({'char': '*',
                    'text': 'black', 'color': 'purple',
                    'posX': 0, 'posY': 0,
                    'sizeX': info.max_x, 'sizeY': info.border_size})

    # left section of border
    OBJECTS.append({'char': '*',
                    'text': 'black', 'color': 'purple',
                    'posX': 0, 'posY': 0,
                    'sizeX': info.border_size, 'sizeY': info.max_y})

    # right section of border
    OBJECTS.append({'char': '*',
                    'text': 'black', 'color': 'purple',
                    'posX': info.max_x - info.border_size, 'posY': 0,
                    'sizeX': info.border_size, 'sizeY': info.max_y})

    # bottom section of border
    OBJECTS.append({'char': '*',
                    'text': 'black', 'color': 'purple',
                    'posX': 0, 'posY': info.max_y - info.border_size,
                    'sizeX': info.max_x, 'sizeY': info.border_size})


    # small blue box
    OBJECTS.append({'char': ' ',
                    'text': 'gray', 'color': 'blue',
                    'posX': info.center_x + 5, 'posY': info.center_y + 5,
                    'sizeX': 2, 'sizeY': 2})

    # small yellow box
    OBJECTS.append({'char': ' ',
                    'text': 'black', 'color': 'yellow',
                    'posX': info.center_x - 5, 'posY': info.center_y - 5,
                    'sizeX': 2, 'sizeY': 2})

    # small green box
    OBJECTS.append({'char': ' ',
                    'text': 'maroon', 'color': 'green',
                    'posX': info.center_x - 5, 'posY': info.center_y + 5,
                    'sizeX': 2, 'sizeY': 2})

    # small red box
    OBJECTS.append({'char': ' ',
                    'text': 'blue', 'color': 'red',
                    'posX': info.center_x + 5, 'posY': info.center_y - 5,
                    'sizeX': 2, 'sizeY': 2})

    # centered brown box
    OBJECTS.append({'char': ' ',
                    'text': 'black', 'color': 'maroon',
                    'posX': info.center_x, 'posY': info.center_y,
                    'sizeX': 2, 'sizeY': 2})


    # red box with green dashes off to the upper left
    OBJECTS.append({'char': '.',
                    'text': 'green', 'color': (254, 0, 0),
                    'posX': 15, 'posY': 20,
                    'sizeX': 10, 'sizeY': 10})


    # teal box with weird stuff off to the lower left
    OBJECTS.append({'char': '%',
                    'text': 'fuchsia', 'color': 'teal',
                    'posX': 20, 'posY': 70,
                    'sizeX': 20, 'sizeY': 20})

    # black box to make the previous object an interesting shape
    OBJECTS.append({'char': ' ',
                    'text': 'white', 'color': 'black',
                    'posX': 27, 'posY': 75,
                    'sizeX': 14, 'sizeY': 10})


def draw_objects(win, view_X, view_Y):
    # draws objects to the screen

    for obj in OBJECTS:
        win.fill(obj['char'],                 # filling character
                obj['text'], obj['color'],    # text and color colors
                (obj['posX'] - view_X,        # create the screen X position
                 obj['posY'] - view_Y,        # create the screen Y position
                 obj['sizeX'], obj['sizeY'])) # sizes


def draw_map(win, info, view_X, view_Y):
    # draws the visible map to the screen

    for y in range(view_Y, view_Y + info.height):
        # stop drawing because the wanted y range is not possible
        if y > len(COLORGRID): break

        for x in range(view_X, view_X + info.width):
            # skip to the next line because the wanted x range is not possibly
            if x > len(COLORGRID[0]): break

            color = COLORTABLE[ COLORGRID[y][x] ]
            if color == info.bgcolor:
                continue

            c = CHAR_COLORS.get(color, ' ')

            if len(c) == 1:
                fg = info.fgcolor
            else:
                fg = c[1]
                c = c[0]
            
            win.fill(c, fg, color, (x - view_X, y - view_Y, 1, 1))
