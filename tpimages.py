#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tpimages.py       
    Description:
        talos-puzzle puzzle solutions drawing
"""
# Library import
import os
from PIL import Image, ImageDraw, ImageColor

# Class
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ImagesError(Error):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message

class Images(object):
    """Class: define and draw the solutions as png images"""
    def __init__(self, args):
        """Constructor: Init Images parameters from verified args"""
        self.cell_size = args.cell_size
        self.fill_color = ImageColor.getrgb(args.fill_color)
        self.shape_color = ImageColor.getrgb(args.shape_color)
        self.output_dir = (args.output_dir 
                           + "\\Board {}Rx{}C - {}LR {}LL {}SR {}SL {}TE {}BA "
                           "{}SQ".format(args.rows, args.columns, 
                           args.l_right, args.l_left, args.step_right, 
                           args.step_left, args.tee, args.bar, args.square))

    def __draw(self, solution):
        """Method (protected): draw the given solution, which is 2 dimensional 
           array with pieces number in cells
        """
        # Get dimension of solution
        rows = len(solution)
        columns = len(solution[0])
        # Create image with a drawing context 
        image = Image.new("RGB", (columns * self.cell_size, 
                                  rows * self.cell_size), self.fill_color)
        draw = ImageDraw.Draw(image)
        # Draw outside borders of pieces (use draw.line to have line
        # width)
        draw.line([(0, 0), (image.width - 1, 0)], self.shape_color, 2)
        draw.line([(image.width - 2, 0), 
                    (image.width - 2, image.height - 1)], 
                    self.shape_color, 2)
        draw.line([(image.width - 1, image.height - 1), 
                    (0, image.height - 1)], 
                    self.shape_color, 2)
        draw.line([(1, image.height - 1), (1, 0)], self.shape_color, 2)
        # Draw inside right borders of pieces
        for row in range(rows):
            for col in range(columns - 1):
                # Look on the right side of the cell and draw border
                # if cell on the right is different
                if solution[row][col] != solution[row][col + 1]:
                    X0 = (col + 1) * self.cell_size - 1
                    Y0 = row * self.cell_size
                    X1 = X0
                    Y1 = (row + 1) * self.cell_size - 1
                    draw.line([(X0, Y0), (X1, Y1)], 
                                self.shape_color, 2)
        # Draw borders bellow pieces
        for row in range(rows - 1):
            for col in range(columns):
                # Look bellow the cell and draw border
                # if cell bellow is different
                if solution[row][col] != solution[row + 1][col]:
                    X0 = col * self.cell_size
                    Y0 = (row + 1) * self.cell_size - 1
                    X1 = (col + 1) * self.cell_size - 1
                    Y1 = Y0
                    draw.line([(X0, Y0), (X1, Y1)], 
                                self.shape_color, 2)
        return image  

    def output_solution(self, solution_idx, solution):
        """Method (public): draw and save the given solution
           Raise ImagesError exception if ioerror
        """
        # Create directory to store the images
        try:
            os.makedirs(self.output_dir,exist_ok=True)
        except:
            message = ("Fatal: Can\'t create output directory {}"
                       .format(self.output_dir))
            raise(ImagesError(message)) 
    
        # Draw the image
        image = self.__draw(solution)
    
        # Save the image
        image_name = (self.output_dir + "\\Solution #{:0>2}.png"
                      .format(solution_idx))
        try:
            image.save(image_name)
        except:
            message = "Fatal: Can't save image {}".format(image_name)
            raise(ImagesError(message)) 


