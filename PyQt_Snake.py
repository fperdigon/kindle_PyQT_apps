__author__ = 'fco'
#!/usr/bin/env python
"""
PyWorm - Snake clone

Amir Hadzic (alias: schmrz)
Date: March, 18th, 2009
Licence: GPL

"""

import sys
import random
from PyQt4 import QtGui, QtCore, Qt

class PyWorm(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        gameSpeed = QtGui.QInputDialog.getInteger(self, "Speed", "Enter speed", 200, 200, 1000)[0]
        sizeFactor_a = QtGui.QInputDialog.getInteger(self, "Size factor", "Enter size factor", 20, 20, 50)[0]
        self.resize(300, 300)
        self.board = Board(self, sizeFactor_a, gameSpeed)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.board)
        self.setLayout(self.layout)
        self.changedDirection = False

        self.center()

    def center(self):
        DesktopScreen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((DesktopScreen.width()-size.width())/2, (DesktopScreen.height()-size.height())/2)

class Board(QtGui.QFrame):
    def __init__(self, parent, sizeFactor, speed):
        QtGui.QFrame.__init__(self, parent)
        print sizeFactor
        print speed
        self.sizeFactor = sizeFactor

        # Number of fields
        self.area = sizeFactor * sizeFactor
        self.GameSpeed = speed

        # Timer is the one updating parts
        # foodTimer is the one taking care that the Worm has enough food
        self.timer = QtCore.QBasicTimer()
        self.foodTimer = QtCore.QBasicTimer()
        self.direction = Direction.UP
        self.fields = []
        self.worm = []
        self.food = Part(Part.FoodPart)
        self.foodInterval = 5000
        self.startPosition = int((self.sizeFactor * self.getCenterCoord()) + self.getCenterCoord())
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # Set worm head
        self.worm.append(Part(partType = Part.WormPart))
        self.worm[0].setPosition(self.startPosition)
        self.worm[0].brushType = QtCore.Qt.Dense3Pattern

        # Add some worm parts to the head
        for x in range(4):
            self.worm.append(Part(partType = Part.WormPart, parent = self.worm[x]))
            self.worm[x+1].setPosition(self.startPosition)

        # Give it some colors
        self.colorifyWorm()

        # Fill in the fields
        self.sortBoard()

        # Start the game
        self.timer.start(self.GameSpeed, self)
        self.foodTimer.start(self.foodInterval, self)

    def keyPressEvent(self, event):
        key = event.key()

        if self.changedDirection:
            QtGui.QWidget.keyPressEvent(self, event)
            return

        # Change worm direction only if it is not opposite of current position
        if key == QtCore.Qt.Key_Left and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif key == QtCore.Qt.Key_Right and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        elif key == QtCore.Qt.Key_Up and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif key == QtCore.Qt.Key_Down and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        else:
            QtGui.QWidget.keyPressEvent(self, event)

        self.changedDirection = True

    def timerEvent(self, event):
        # timer
        if event.timerId() == self.timer.timerId():
            self.moveParts()
            self.changedDirection = False
            self.sortBoard()
            self.update()
        # foodTimer
        elif event.timerId() == self.foodTimer.timerId():
            self.placeFood()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush(QtGui.QColor("white"))
        size = self.getPartSize()

        for i in range(len(self.fields)):
            # Get grid coordinates
            x,y = self.getCoord(i)
            # Get "real" pixel coordinates
            x,y = self.toPixels(x, y)

            # Fill the rectangle
            brush.setColor(self.fields[i].background)
            brush.setStyle(self.fields[i].brushType)
            rect = QtCore.QRect(x,y,size,size)
            painter.fillRect(rect, brush)

            pos = self.toPixels(0,0)
            rect = QtCore.QRect(pos[0], pos[1], self.sizeFactor*self.getPartSize(), self.sizeFactor*self.getPartSize())
            painter.drawRect(rect)

    def colorifyWorm(self):
        for x in range(len(self.worm)):
            self.worm[x].background = QtGui.QColor(Part.colors[self.worm[x].type])

        for x in range(0, len(self.worm), 2):
            self.worm[x].background = QtGui.QColor("brown")

    def placeFood(self):
        # Get a number between 0 and area-a (because list index begins with 0)
        position = random.randint(0, self.area-1)
        self.food.setPosition(position)

    def sortBoard(self):
        self.fields = []

        # Set all fields to Part with type EmptyPart
        for x in range(self.area):
            self.fields.append(Part(partType = Part.EmptyPart))

        # Set all fields in first row to be blocking parts
        for x in range(self.sizeFactor):
            self.fields[x] = Part(partType = Part.BlockPart)

        # Set all fields in last row to be blocking parts
        for x in range(self.area - self.sizeFactor, self.area):
            self.fields[x] = Part(partType = Part.BlockPart)

        # Set worm fields
        for x in self.worm:
            self.fields[x.position] = x

        # Draw food only if the selected field is empty.
        if self.food.position:
            if self.fields[self.food.position].type == Part.EmptyPart:
                self.fields[self.food.position] = self.food
            else:
                self.placeFood()

    def toPixels(self, x, y):
        return (x * self.getPartSize(), y * self.getPartSize())

    def getCenterCoord(self):
        return round(self.sizeFactor/2)

    def getCoord(self, fieldNumber):
        if fieldNumber % self.sizeFactor == 0:
            y = fieldNumber / self.sizeFactor
        else:
            row = str(float(fieldNumber) / float(self.sizeFactor))
            y = int(row.split('.')[0])

        return (fieldNumber - (self.sizeFactor*y), y)

    def getPartSize(self):
        return int(round(self.width() / self.sizeFactor))

    def nextField(self, part):
        if self.direction == Direction.RIGHT:
            newpos = part.position + 1

        elif self.direction == Direction.LEFT:
            newpos = part.position - 1

        elif self.direction == Direction.UP:
            newpos = part.position - self.sizeFactor

        elif self.direction == Direction.DOWN:
            newpos = part.position + self.sizeFactor

        oldRow = self.getRow(part.position)
        newRow = self.getRow(newpos)

        if oldRow != newRow and newpos > 0 and newpos < self.area:
            # If the worm enters the right wall teleport it back to the left one
            if self.direction == Direction.RIGHT:
                newpos = part.position - (self.sizeFactor-1)
                return newpos
            # If the worm enters the left wall teleport it back to the right one
            if self.direction == Direction.LEFT:
                newpos = part.position + (self.sizeFactor-1)
                return newpos
            # If the new position is above the current position or under it...
            if (part.position + self.sizeFactor) == newpos or (part.position - self.sizeFactor) == newpos:
                return newpos

        # If the worm enters the top wall, teleport it back to the bottom one
        if newpos < 0:
            newpos = self.area - newpos
            return newpos
        # Try to guess this one.
        if newpos > self.area:
            newpos = newpos - self.area
            return newpos

        return newpos

    def isFieldInvalid(self, oldField, newField):
        if newField > self.area or newField < 0: return 1

        if self.fields[newField].type == Part.BlockPart: return 1

        for x in self.worm:
            if newField == x.position: return 1

        return 0

    def getRow(self, pos):
        row = str(float(pos) / float(self.sizeFactor))
        y = int(row.split('.')[0])
        return y

    def moveParts(self):
        if self.isFieldInvalid(self.worm[0].position, self.nextField(self.worm[0])):
            self.timer.stop()
            self.foodTimer.stop()
            QtGui.QMessageBox.information(None, "Game over.", "You have lost. Your score is " + str(len(self.worm)))
        else:
            if self.fields[self.nextField(self.worm[0])].type == Part.FoodPart:
                # Feed the worm
                self.worm.append(Part(Part.WormPart, self.worm[len(self.worm)-1]))
                # Get some fresh food
                self.placeFood()
                # Restart the food timer
                self.foodTimer.stop()
                self.foodTimer.start(self.foodInterval, self)
                # Colorify worm
                self.colorifyWorm()

            # Move the worm head
            self.worm[0].changePosition(self.nextField(self.worm[0]))

            # Move the other parts of worm
            for x in range(1, len(self.worm)):
                self.worm[x].trackParent()

class Direction(object):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

class Part(object):
    EmptyPart = 0
    WormPart = 1
    FoodPart = 2
    BlockPart = 3

    colors = [0xF0F0F0, 0xFF9900, "red", 0xB3B3B3]
    brushTypes = [QtCore.Qt.SolidPattern, QtCore.Qt.SolidPattern, QtCore.Qt.Dense2Pattern, QtCore.Qt.Dense1Pattern]

    def __init__(self, partType, parent=None):
        self.parent = parent
        self.type = partType
        self.background = QtGui.QColor(self.colors[self.type])
        self.brushType = self.brushTypes[self.type]
        self.position = None

    def setLastPosition(self, pos):
        self.lastPosition = pos

    def setPosition(self, pos):
        self.position = pos

    def changePosition(self, pos):
        self.lastPosition = self.position
        self.position = pos

    def trackParent(self):
        self.changePosition(self.parent.lastPosition)

app = QtGui.QApplication(sys.argv)
game = PyWorm()

game.show()
sys.exit(app.exec_())
