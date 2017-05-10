# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 20:14:39 2016

@author: Utkarsh Rastogi
"""

import sys
import random
from PyQt4 import QtGui,QtCore

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
 
        self.setWindowTitle('Minesweeper')
        self.setWindowIcon(QtGui.QIcon('minesweeper.ico'))
        self.setStyleSheet("QMenuBar { background-color: #dddddd; }")
        self.setFixedSize(324,380)
        
        self.centralwidget = QtGui.QWidget()
        self.setCentralWidget(self.centralwidget)    
        
        self.vLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.hLayout = QtGui.QHBoxLayout()
        
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSpacing(0)
        
        # center the grid with stretch on both sides
        self.hLayout.addStretch()
        self.hLayout.addLayout(self.gridLayout)
        self.hLayout.addStretch()
        
        self.vLayout.addLayout(self.hLayout)
        # push grid to the top of the window
        self.vLayout.addStretch()
       
        self.buttonLayout = QtGui.QHBoxLayout()
        self.buttonLayout.addStretch()
        
        self.timeLabel = QtGui.QLabel('0.0 Sec')
        self.timeLabel.setStyleSheet('QLabel {font:  16px; color: #b6135d}') 
        self.flagLabel = QtGui.QLabel("Flags: ")
        self.flagLabel.setStyleSheet('QLabel {font:  16px; color: black}') 
        self.flagCnt = QtGui.QLabel("0/10")
        self.flagCnt.setStyleSheet('QLabel {font:  16px; color: black}')
        
        self.buttonLayout.addWidget(self.timeLabel)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.flagLabel)
        self.buttonLayout.addWidget(self.flagCnt) 
        self.buttonLayout.addStretch()
             
        self.gridLayout.addLayout(self.buttonLayout,0,0,1,9)
        
        self.newGame()
        
        exitAction = QtGui.QAction( '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(QtGui.qApp.quit) 
        newAction = QtGui.QAction( '&New Game', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Start New Game')
        newAction.triggered.connect(self.newGame)

        menubar = self.menuBar()
        optionMenu = menubar.addMenu('&File')
        optionMenu.addAction(newAction)
        optionMenu.addAction(exitAction)
    
    
    def newGame(self):
        self.buttons = []
        for i in xrange(9):
            l=[]
            for j in xrange(9):
                b=QtGui.QPushButton()
                b.setFixedSize(35,35)
                l.append(b)
                self.gridLayout.addWidget(b, i+1, j)
                b.setStatusTip(str(i) + str(j))
                b.clicked = False
                b.flagged = False
                b.row = i
                b.col = j
                b.isMine = False
                b.mineCount = -1
                b.setFlat(False)
                b.setEnabled(True)
                QtCore.QObject.connect(b, QtCore.SIGNAL("clicked()"), self.buttonClicked )
                b.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                b.customContextMenuRequested.connect(self.rightClick)
            self.buttons.append(l)
        
        
        self.placeMines()
        self.mineGrid()
        
        self.time = QtCore.QTime(0,0,0)
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateTimer)
        self.timer.stop()
        
        self.timerRunning = False
        self.flags = 0
        self.flagCnt.setText( "0/10" )
        self.timeLabel.setText( "0.0 Sec" )        
        return
        
    
    def buttonClicked(self):
        if self.timerRunning == False:
            self.time.start()
            self.timer.start(100)
            self.timerRunning = True
            
        button = self.sender()
        r = button.row
        c = button.col
        self.revealNearby(r,c)
        return
    
    
    def rightClick(self):
        button = self.sender()
        r = button.row
        c = button.col
        if self.buttons[r][c].flagged==True:
            self.flags = self.flags - 1
            self.buttons[r][c].flagged=False
            txt = ''
            self.buttons[r][c].setText(txt)
            self.buttons[r][c].setStyleSheet('QPushButton {font: bold 20px; color: black}')
        else:
            self.flags = self.flags + 1
            self.buttons[r][c].flagged=True
            txt = '?'
            self.buttons[r][c].setText(txt)
            self.buttons[r][c].setStyleSheet('QPushButton {font: bold 20px; color: black}')
        
        self.flagCnt.setText(str(self.flags) + "/10")
        val = self.isGameOver()
        if val == True:
            self.timer.stop()
            self.gameOver()
            self.displayMessage('win')            
        return
    
    
    def updateTimer(self):
        self.secs = self.time.elapsed() / float(1000)
        self.timeLabel.setText( str(round(self.secs,1)) + " Sec" )
        return
        
        
    def revealNearby(self, r, c):
        mineCnt = self.buttons[r][c].mineCount
        if mineCnt != -1:
            txt = str(mineCnt)
            self.buttons[r][c].setText(txt)
            self.buttons[r][c].clicked = True
            self.buttons[r][c].setFlat(True)
            self.buttons[r][c].setEnabled(False)
            self.buttons[r][c].setStyleSheet('QPushButton { background-color: #cccccc; \
                                            border:1px; font: 22px; color: blue}')
            
            if mineCnt == 0:
                x = [0, 0,1,1, 1,-1,-1,-1]
                y = [1,-1,0,1,-1, 0, 1,-1]
                
                for z in range(8):
                    if self.isSafe(r+x[z],c+y[z]) and self.buttons[r+x[z]][c+y[z]].clicked != True:
                        self.revealNearby(r+x[z],c+y[z]) 
        
        else:
            txt = 'X'
            self.buttons[r][c].setText(txt)
            self.buttons[r][c].clicked = True
            self.buttons[r][c].setFlat(True)
            self.buttons[r][c].setEnabled(False)
            self.buttons[r][c].setStyleSheet('QPushButton { background-color: #cccccc; \
                                            border:1px; font: bold 20px; color: #ff3333}')
            self.timer.stop()                                
            self.gameOver()
            self.displayMessage('lose')            
        return
    
    
    def isGameOver(self):
        if self.flags !=10:
            return False
            
        for i in range (9):
            for j in range (9):
                if self.buttons[i][j].flagged == True and self.buttons[i][j].isMine !=True:
                    return False       
        return True
    
    
    def gameOver(self):
        for i in range(9):
            for j in range(9):
                mineCnt = self.buttons[i][j].mineCount
                if self.buttons[i][j].flagged == True and mineCnt == -1:
                    txt = 'X'
                    self.buttons[i][j].setText(txt)
                    self.buttons[i][j].clicked = True
                    self.buttons[i][j].setFlat(True)
                    self.buttons[i][j].setEnabled(False)
                    self.buttons[i][j].setStyleSheet('QPushButton { background-color: #cccccc; \
                                                    border:1px; font: bold 20px; color: #5cd65c}')
                elif (self.buttons[i][j].flagged == True and mineCnt != -1) or (self.buttons[i][j].flagged == False and mineCnt == -1):
                    txt = str(mineCnt) if mineCnt != -1 else 'X' 
                    self.buttons[i][j].setText(txt)
                    self.buttons[i][j].clicked = True
                    self.buttons[i][j].setFlat(True)
                    self.buttons[i][j].setEnabled(False)
                    self.buttons[i][j].setStyleSheet('QPushButton { background-color: #cccccc; \
                                                    border:1px; font: bold 20px; color: #ff3333}')
                else:
                    txt = str(mineCnt)
                    self.buttons[i][j].setText(txt)
                    self.buttons[i][j].clicked = True
                    self.buttons[i][j].setFlat(True)
                    self.buttons[i][j].setEnabled(False)
                    self.buttons[i][j].setStyleSheet('QPushButton { background-color: #cccccc; \
                                                    border:1px; font: 22px; color: blue}')
        return


    def displayMessage(self, m):
        msgBox = QtGui.QMessageBox();
        f = open('highscore.txt', 'r')
        highScore = float(f.read())
        f.close()
        
        if m=='win':
            txt = 'You flagged all Mines.\nYou Win.'
            title = 'Congratulations!!!'
            if self.secs < highScore:
                f = open('highscore.txt', 'w')
                highScore = round(self.secs,1)
                f.write(str(highScore))
                f.close()
                detailTxt = "New Highscore is " + str(highScore) + " Sec."
            else:
                detailTxt = "Highscore is " + str(highScore) + " Sec."
            msgBox.setInformativeText("Your time is " + str(round(self.secs,1)) + " Sec.\n\n" + detailTxt)
        else:
            txt = 'You clicked a Mine.\nGame Over'
            
            title = 'Oops!!!'
        
        msgBox.setText(txt)
        msgBox.setWindowTitle(title)
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setWindowIcon(QtGui.QIcon('minesweeper.ico'))
        msgBox.exec_()               
        return
           
           
    def placeMines(self):
        mines = random.sample(range(81),10)
        #print mines
        for i in range(9):
            for j in range(9):
                if i*9+j in mines:
                    self.buttons[i][j].isMine = True
        return


    def mineGrid(self):
        x = [0, 0,1,1, 1,-1,-1,-1]
        y = [1,-1,0,1,-1, 0, 1,-1]
        
        for i in range(9):
            for j in range(9):
                cnt = 0
                if self.buttons[i][j].isMine == False:
                    for z in range(8):
                        if self.isSafe(i+x[z],j+y[z]) and self.buttons[i+x[z]][j+y[z]].isMine==True :
                            cnt = cnt + 1
                    self.buttons[i][j].mineCount = cnt               
        return

    
    def isSafe(self, i, j):
        if i<9 and i>=0 and j<9 and j>=0:
            return True
        else:
            return False

    
    def debug(self):
        print 'debug'
        return;


def main():
    app = QtGui.QApplication(sys.argv)
    foo = MainWindow()
    foo.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
