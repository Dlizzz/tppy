#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tpimages.py       
    Description:
        talos-puzzle puzzle solutions drawing
"""
# Library import
from PIL import Image
from PIL import ImageDraw

# Functions
def draw_board(solution, cell_size, fill_color, shape_color):
    # Get dimension of solution
    rows = len(solution)
    columns = len(solution[0])
    # Create image with a drawing context 
    image = Image.new("RGB", (columns * cell_size, 
                                rows * cell_size), fill_color)
    draw = ImageDraw.Draw(image)
    # Draw outside borders of pieces (use draw.line to have line
    # width)
    draw.line([(0, 0), (image.width - 1, 0)], shape_color, 2)
    draw.line([(image.width - 2, 0), 
                (image.width - 2, image.height - 1)], 
                shape_color, 2)
    draw.line([(image.width - 1, image.height - 1), 
                (0, image.height - 1)], 
                shape_color, 2)
    draw.line([(1, image.height - 1), (1, 0)], shape_color, 2)
    # Draw inside right borders of pieces
    for row in range(rows):
        for col in range(columns - 1):
            # Look on the right side of the cell and draw border
            # if cell on the right is different
            if solution[row][col] != solution[row][col + 1]:
                X0 = (col + 1) * cell_size - 1
                Y0 = row * cell_size
                X1 = X0
                Y1 = (row + 1) * cell_size - 1
                draw.line([(X0, Y0), (X1, Y1)], 
                            shape_color, 2)
    # Draw borders bellow pieces
    for row in range(rows - 1):
        for col in range(columns):
            # Look bellow the cell and draw border
            # if cell bellow is different
            if solution[row][col] != solution[row + 1][col]:
                X0 = col * cell_size
                Y0 = (row + 1) * cell_size - 1
                X1 = (col + 1) * cell_size - 1
                Y1 = Y0
                draw.line([(X0, Y0), (X1, Y1)], 
                            shape_color, 2)
    return image  
