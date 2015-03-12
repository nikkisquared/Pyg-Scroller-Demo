#!/usr/bin/python

# functions for moving the view and the player

from pygame import key
from pygame.locals import *

# just holds the large information for wall data in an easy to read layout

WALLS = [
    # blue C building
    (0, 128, 128),
    # main border
    (128, 0, 128),
    # walls of green area
    (12, 45, 6), (11, 40, 5), (2, 8, 1), (9, 32, 4), (21, 76, 11),
    # walls of blue area
    (62, 140, 130), (15, 35, 33), (20, 49, 43),
    ()]


def shift_view_mouse(info, view_X, view_Y, cell_X, cell_Y):
    """Scrolls the view as the player moves the mouse"""

    if cell_X >= info.width - info.mouse_margin - 1:
        view_X += 1
    elif cell_X <= info.mouse_margin:
        view_X -= 1

    if cell_Y >= info.height - info.mouse_margin - info.textbox_height - 1:
        view_Y += 1
    elif cell_Y <= info.mouse_margin:
        view_Y -= 1

    return view_X, view_Y
    

def shift_view_kb(keys, view_X, view_Y, playerDirs):
    """Shifts the view as the player holds down keys"""

    if 'R' not in playerDirs and (keys[K_RIGHT] or keys[K_d]):
        view_X += 1
    elif 'L' not in playerDirs and (keys[K_LEFT] or keys[K_a]):
        view_X -= 1

    if 'D' not in playerDirs and (keys[K_DOWN] or keys[K_s]):
        view_Y += 1
    elif 'U' not in playerDirs and (keys[K_UP] or keys[K_w]):
        view_Y -= 1

    return view_X, view_Y


def check_view_boundaries(info, view_X, view_Y):
    """Verifies that the current view or player is not going outside of the playing area"""

    if view_X > info.right_boundary - info.width:
        view_X = info.right_boundary - info.width
    elif view_X < info.left_boundary:
        view_X = info.left_boundary

    if view_Y > info.bottom_boundary - info.height:
        view_Y = info.bottom_boundary - info.height
    elif view_Y < info.top_boundary:
        view_Y = info.top_boundary

    return view_X, view_Y


def get_player_dirs(info, view_X, view_Y, player_X, player_Y):
    """Sets the possible player movement axes and returns them"""

    playerDirs = ''

    if view_X == info.left_boundary:
        playerDirs += 'L'
        if player_X != info.width / 2:
            playerDirs += 'R'

    elif view_X == info.right_boundary - info.width:
        playerDirs += 'R'
        if player_X != info.width / 2:
            playerDirs += 'L'

    if view_Y == info.top_boundary:
        playerDirs += 'U'
        if player_Y != info.height / 2:
            playerDirs += 'D'

    elif view_Y == info.bottom_boundary - info.height:
        playerDirs += 'D'
        if player_Y != info.height / 2:
            playerDirs += 'U'

    return playerDirs


def move_player(info, keys, player_X, player_Y, playerDirs, wall_grid):
    """Moves the player character, if possible"""

    old_X = player_X
    old_Y = player_Y

    # wall_X and wall_Y is set to the center of the wall grid
    wall_X = 1
    wall_Y = 1
    isWall = False

    if keys[K_RIGHT] or keys[K_d]:
        if 'R' in playerDirs: player_X += 1
        wall_X += 1
    elif (keys[K_LEFT] or keys[K_a]):
        if 'L' in playerDirs: player_X -= 1
        wall_X -= 1

    if (keys[K_DOWN] or keys[K_s]):
        if 'D' in playerDirs: player_Y += 1
        wall_Y += 1
    elif (keys[K_UP] or keys[K_w]):
        if 'U' in playerDirs: player_Y -= 1
        wall_Y -= 1

    move = check_player_boundaries(info, player_X, player_Y, wall_X, wall_Y)
    player_X, player_Y, wall_X, wall_Y = move

    isWall = wall_grid[wall_X][wall_Y] in WALLS

    if isWall:
        # can not allow player to move
        player_X = old_X
        player_Y = old_Y

    return player_X, player_Y, isWall


def check_player_boundaries(info, player_X, player_Y, wall_X, wall_Y):
    """Verifies that the current view or player is not going outside of the playing area"""

    if player_X > info.width - 1:
        player_X = info.width - 1
        wall_X -= 1
    elif player_X < 0:
        player_X = 0
        wall_X += 1

    if player_Y > info.height - 1:
        player_Y = info.height - 1
        wall_Y -= 1
    elif player_Y < 0 + info.textbox_height:
        player_Y = 0 + info.textbox_height
        wall_Y += 1

    return player_X, player_Y, wall_X, wall_Y


def player(info, keys, view_X, view_Y, player_X, player_Y, wall_grid):
    """Handles positioning of the view and player movement"""

    playerDirs = get_player_dirs(info, view_X, view_Y, player_X, player_Y)
    move = move_player(info, keys, player_X, player_Y, playerDirs, wall_grid)
    player_X, player_Y, isWall = move

    if not isWall:
        view_X, view_Y = shift_view_kb(keys, view_X, view_Y, playerDirs)

    return view_X, view_Y, player_X, player_Y