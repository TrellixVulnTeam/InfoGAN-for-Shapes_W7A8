import pygame
import os
import numpy as np
from scipy import misc

def getPath(shape, code):
    return os.path.join('images', shape + 's', shape +
            str(code) + '.png')

def subMatrix(matrix):
     # white is 255, black is 0, the matrices are 8 bit encoded, so modulo 255,
     # so 255 + 1 = 0, 0 + 1 = 1
     return matrix + 1

def getMatrix(imageName):

    imageMatrix = misc.imread(imageName, flatten=True)
   # imageMatrix = misc.imread(imageName)
    #imageMatrix = (subMatrix(imageMatrix[:,:,0])/3 +
     #       subMatrix(imageMatrix[:,:,1])/3 +
      #      subMatrix(imageMatrix[:,:,2])/3)
    #print(imageMatrix)
    matrix = subMatrix(imageMatrix) % 256

    return matrix

def checkMatrix(matrix, imageSize):
    # for a 28x28 image we want shapes which are bigger than 9 pixels. 28x28/80
    # = 9
    matrixok = False
    # check if big enough
    if np.sum(matrix) > ((imageSize[0] * imageSize[1]) / 80) and np.sum(matrix) < (imageSize[0] * imageSize[1]):
        # check if ratio of height to length ok, to rule out super lengthy objects
        shaperow = []
        shapecol = []
        for i in range(imageSize[0]):
            for j in range(imageSize[1]):
                if matrix[i,j] != 0:
                    shaperow.append(i)
                    shapecol.append(j)
        length = max(shaperow) - min(shaperow)
        height = max(shapecol) - min(shapecol)
        if height > 0 and length > 0:
            ratio = length/height
            if ratio < 4 and ratio > 0.25:
                matrixok = True
    return matrixok

def rotate(matrix, angle, imageSize):

    # get middle point of matrix around which we want to rotate the matrix

    shaperow = []
    shapecol = []
    shape = []

    for i in range(imageSize[0]):
        for j in range(imageSize[1]):
            if matrix[i,j] != 0:
                shaperow.append(i)
                shapecol.append(j)
                shape.append([i,j,matrix[i,j]])
    middlepointrow = min(shaperow) + ((max(shaperow) - min(shaperow))/2.)
    middlepointcol = min(shapecol) + ((max(shapecol) - min(shapecol))/2.)

    s = np.sin(angle);
    c = np.cos(angle);

    rotatetmatrix = np.full((imageSize[0],imageSize[1]), 0)

    for point in shape:
        # translate point back to origin:
        point[0] -= middlepointrow;
        point[1] -= middlepointcol;

        #rotate point
        xnew = point[0] * c - (point[1] * s);
        ynew = point[0] * s + (point[1] * c);

        #translate point back: (The 0.5 is to round the number and not only cut the decimals off)
        x1 = int(xnew + middlepointrow - 0.5);
        y1 = int(ynew + middlepointcol - 0.5);
        x2 = int(xnew + middlepointrow + 0.5);
        y2 = int(ynew + middlepointcol + 0.5);

        if x1 < imageSize[0] and x1 >= 0 and y1 < imageSize[1] and y1 >= 0 :
            rotatetmatrix[x1,y1] = point[2]
        if x2 < imageSize[0] and x2 >= 0 and y2 < imageSize[1] and y2 >= 0:
            rotatetmatrix[x2,y2] = point[2]
        if x2 < imageSize[0] and x2 >= 0 and y1 < imageSize[1] and y1 >= 0 :
            rotatetmatrix[x2,y1] = point[2]
        if x1 < imageSize[0] and x1 >= 0 and y2 < imageSize[1] and y2 >= 0:
            rotatetmatrix[x1,y2] = point[2]

    return rotatetmatrix;

class Ellipse:

    def __init__(self, area, color, borderWidth, matrixContainer, count):
        self.color = color
        self.borderWidth = borderWidth
        self.area = area
        self.imageName = getPath('ellipse', self.area)
        self.matrixContainer = matrixContainer
        self.count = count

    def draw(self, imageSize):
        screen = pygame.display.set_mode(imageSize)
        white = [255,255,255]
        screen.fill(white)
        pygame.draw.ellipse(screen, self.color, self.area, self.borderWidth)
        pygame.image.save(screen, self.imageName)
        imageMatrix = getMatrix(self.imageName)
        if checkMatrix(imageMatrix, imageSize):

            self.matrixContainer.put(imageMatrix, 'ellipse')

            rotate15 = rotate(imageMatrix, 15, imageSize)
            if checkMatrix(rotate15, imageSize):
                self.matrixContainer.put(rotate15, 'ellipse')

            rotate30 = rotate(imageMatrix, 30, imageSize)
            if checkMatrix(rotate30, imageSize):
                self.matrixContainer.put(rotate30, 'ellipse')

            rotate45 = rotate(imageMatrix, 45, imageSize)
            if checkMatrix(rotate45, imageSize):
                self.matrixContainer.put(rotate45, 'ellipse')

            rotate60 = rotate(imageMatrix, 60, imageSize)
            if checkMatrix(rotate60, imageSize):
                self.matrixContainer.put(rotate60, 'ellipse')

            rotate75 = rotate(imageMatrix, 75, imageSize)
            if checkMatrix(rotate75, imageSize):
                self.matrixContainer.put(rotate75, 'ellipse')

class Triangle:

    def __init__(self, pointlist, color, borderWidth, matrixContainer):
        self.color = color
        self.borderWidth = borderWidth
        self.pointlist = pointlist
        self.imageName = getPath('triangle', self.pointlist)
        self.matrixContainer = matrixContainer

    def draw(self, imageSize):
        screen = pygame.display.set_mode(imageSize)
        white = [255,255,255]
        screen.fill(white)
        pygame.draw.polygon(screen, self.color, self.pointlist, self.borderWidth)
        pygame.image.save(screen, self.imageName)
        imageMatrix = getMatrix(self.imageName)
        if checkMatrix(imageMatrix, imageSize):

            self.matrixContainer.put(imageMatrix, 'triangle')

            

class Rectangle:

    def __init__(self, area, color, borderWidth, matrixContainer, count):
        self.color = color
        self.borderWidth = borderWidth
        self.area = area
        self.imageName = getPath('rectangle', self.area)
        self.matrixContainer = matrixContainer
        self.count = count

    def draw(self, imageSize):
        screen = pygame.display.set_mode(imageSize)
        white = [255,255,255]
        screen.fill(white)
        pygame.draw.rect(screen, self.color, self.area, self.borderWidth)
        pygame.image.save(screen, self.imageName)
        imageMatrix = getMatrix(self.imageName)
        if checkMatrix(imageMatrix, imageSize):

            self.matrixContainer.put(imageMatrix, 'rectangle')

            rotate15 = rotate(imageMatrix, 15, imageSize)
            if checkMatrix(rotate15, imageSize):
                self.matrixContainer.put(rotate15, 'rectangle')

            rotate30 = rotate(imageMatrix, 30, imageSize)
            if checkMatrix(rotate30, imageSize):
                self.matrixContainer.put(rotate30, 'rectangle')

            rotate45 = rotate(imageMatrix, 45, imageSize)
            if checkMatrix(rotate45, imageSize):
                self.matrixContainer.put(rotate45, 'rectangle')

            rotate60 = rotate(imageMatrix, 60, imageSize)
            if checkMatrix(rotate60, imageSize):
                self.matrixContainer.put(rotate60, 'rectangle')

            rotate75 = rotate(imageMatrix, 75, imageSize)
            if checkMatrix(rotate75, imageSize):
                self.matrixContainer.put(rotate75, 'rectangle')
            


# class Circle:

#     def __init__(self, imageSize, color, borderWidth, margin):
#         self.color = color
#         self.borderWidth = borderWidth
#         # radius 0 would lead to no shape. The circle has to fit on the smaller
#         # side of the image, therefor 'min'. Twice the radius should not be
#         # bigger than the size of the smaller side of the image without the
#         # margins on both sites.
#         smallerSide = min(imageSize[0], imageSize[1])
#         self.radius = np.random.randint(1,  int(smallerSide - 2 * margin) / 2)
#         # The y-Coordinate of the middle point should be at least as far from
#         # each border as the radius + margin
#         yCoordinate = np.random.randint(margin + radius, imageSize[0] - margin
#                 - radius)
#         xCoordinate = np.random.randint(margin + radius, imageSize[1] - margin
#                 - radius)
#         self.position = [xCoordinate, yCoordinate]

#     def draw(self, screen):
#         pygame.draw.circle(screen, self.color, self.position, self.radius, self.borderWidth)
