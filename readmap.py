#!/usr/bin/python

# reads map data from a file, and returns it

FILENAME = "map.txt"

def read_map():
    """Reads in the pixel color data from a text file"""

    f = open(FILENAME, 'r')
    data = f.read().split('\n')
    f.close()

    size = data[0].split(',')
    colors = data[1].split(',')
    pixels = data[2].split(',')

    map_x = int(size[0])
    map_y = int(size[1])

    colorTable = []
    byte = 0

    while byte < len(colors):
        colorValue = ( int(colors[byte]), int(colors[byte + 1]), int(colors[byte + 2]) )
        colorTable.append(colorValue)
        byte += 3

    colorGrid = []
    currRow = []

    for p in pixels:
        currRow.append( int(p) )
        if len(currRow) == map_x:
            colorGrid.append(currRow)
            currRow = []

    return colorTable, colorGrid