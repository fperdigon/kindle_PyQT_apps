"""
Python PyQt Tic tac toe game NegaMax Algorithm with Alpha Beta Pruning
http://en.wikipedia.org/wiki/Negamax
Copyright (C) 2013 Mike 
https://github.com/miketwes/tic-tac-toe
E-mail mt.kongtong@gmail.com
chessboard 369 x 369 edge 15 cell 107 pading 9 

"""


import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PyQt4.QtWidgets import *
from nega import *

class T(QWidget):	
	
	n = stop = 0
	Lo = [-1, 4, -3, -2, 0 ,2, 3, -4, 1]
	b = dict(zip(Lo, [0]*9))
	h = []
	
	def __init__(self):		
		
		super(T, self).__init__()		
		self.setWindowTitle("Tic Tac Toe")
		self.label = QLabel()		
		self.label.setGeometry(0, 0, 369, 369);
		self.label.setPixmap(QPixmap("b2.png"))
		self.label.installEventFilter(self) 		
		self.grid = QGridLayout()
		self.grid.addWidget(self.label)
		self.setLayout(self.grid)

		
	def clear_up(self):
		
		self.n = self.stop = 0 
		for i in self.h:
			i.setParent(None) 
		self.b = dict(zip(self.Lo, [0]*9))

				
	def eventFilter(self, obj, event):		
	
		if event.type() == QEvent.MouseButtonPress:	
									
			if obj==self.label:
				if event.button() == Qt.LeftButton:  
					if self.n >= 8 or self.stop == 1:                    
						self.clear_up()
						return False					                 
					self.click_on(event)	
				elif event.button() == Qt.MiddleButton:
					self.stop == 1
					if self.n >= 1 :                    
						self.clear_up()
					return	False			
				elif event.button() == Qt.RightButton:
					return	False
					
			return	True
					
		elif event.type() == QEvent.MouseButtonRelease: 
			
			if event.button() == Qt.MiddleButton or event.button() == Qt.RightButton:
				return	False	
			if self.n == 0 and self.stop != 1:
				self.start()
				return	True 		
			elif self.stop != 1 and self.n < 8 and self.n > 0:
				p = best_move(self.b, self.Lo) 				
				self.add_p(p)
				return	True
				
		return False

	def addpane(self, x,y):	
		
		pic = ["x2.png", "o2.png"]
		xo = QLabel()	
		xo.setParent(self.label)
		xo.setPixmap(QPixmap(pic[self.n % 2]))
		xo.move(15 + (x-1)*116, 15 + (y-1)*116)
		xo.show()
		self.h.append(xo)
		self.n = self.n + 1		
		if self.n >= 4:
			wnnr = c(self.b)
			if wnnr != 0:
				self.stop = 1

	def add_p(self, p):
		
				self.b[p] = 1			
				x, y = self.ntoxy(self.Lo.index(p))
				self.addpane(x, y)
	
	def start(self):
		
		p = random.choice(self.Lo)
		self.add_p(p)
		
	def click_on(self, event):
				
		p = QPoint( event.pos().x(), event.pos().y())				
		x = self.get_x_y(p.x())
		y = self.get_x_y(p.y())		
		if x and y:
			po = x + (y - 1) * 3 - 1
			dot  = self.Lo[po]
			self.b[dot] = -1
			self.addpane(x,y)		
		else:
			return False	

	def ntoxy(self, p):
		return p % 3 + 1 , int(p/3) + 1
	
	def get_x_y(self, x):	
		
		for i in range(1,4):			
			if x > 15 + (i-1)*116 and x < 122 + (i-1)*116 :
				return i
		return 0
		
def main():
    
	app = QApplication(sys.argv)
	app.setStyle(QStyleFactory.create("gtk"))
	widget = T()	
	widget.resize(369, 369)
	qr = widget.frameGeometry()
	cp = QDesktopWidget().availableGeometry().center()
	qr.moveCenter(cp)
	widget.move(qr.topLeft())
	widget.setWindowFlags(widget.windowFlags() & ~Qt.WindowMaximizeButtonHint)
	widget.show()
	sys.exit(app.exec_())    
    
if __name__ == '__main__':
    main()
