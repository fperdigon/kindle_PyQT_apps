import sys
from PyQt4 import QtCore, QtGui, uic
 
qtCreatorFile = "scical.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtGui.QMainWindow, Ui_MainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.addButton.clicked.connect(self.add)
		self.subtractButton.clicked.connect(self.subtract)
		self.multiplyButton.clicked.connect(self.multiply)
		self.divideButton.clicked.connect(self.divide)
		self.numeral_1.clicked.connect(self.num1)
		self.numeral_2.clicked.connect(self.num2)
		self.numeral_3.clicked.connect(self.num3)
		self.numeral_4.clicked.connect(self.num4)
		self.numeral_5.clicked.connect(self.num5)
		self.numeral_6.clicked.connect(self.num6)
		self.numeral_7.clicked.connect(self.num7)
		self.numeral_8.clicked.connect(self.num8)
		self.numeral_9.clicked.connect(self.num9)
		self.numeral_0.clicked.connect(self.num0)
		self.decimalButton.clicked.connect(self.decimal)
		self.openBButton.clicked.connect(self.openB)
		self.closedBButton.clicked.connect(self.closedB)
		self.piButton.clicked.connect(self.pi)
		self.eButton.clicked.connect(self.e)
		self.sinButton.clicked.connect(self.sin)
		self.cosButton.clicked.connect(self.cos)
		self.tanButton.clicked.connect(self.tan)
		self.logButton.clicked.connect(self.log)
		self.lnButton.clicked.connect(self.ln)
		self.xraiseyButton.clicked.connect(self.xraisey)
		self.tenraiseButton.clicked.connect(self.tenraise)
		self.eraiseButton.clicked.connect(self.eraise)
		self.sqrButton.clicked.connect(self.sqr)
		self.ansButton.clicked.connect(self.ans)
		self.clearButton.clicked.connect(self.clear)

	def add(self):
		strfn=str(self.dispText.toPlainText())
		strfn+=' + '
		self.dispText.setText(strfn)

	def subtract(self):
		strfn=str(self.dispText.toPlainText())
		strfn+=' - '
		self.dispText.setText(strfn)

	def multiply(self):
		strfn=str(self.dispText.toPlainText())
		strfn+=' x '
		self.dispText.setText(strfn)

	def divide(self):
		strfn=str(self.dispText.toPlainText())
		strfn+=' / '
		self.dispText.setText(strfn)

	def num1(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='1'
		self.dispText.setText(strfn)

	def num2(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='2'
		self.dispText.setText(strfn)

	def num3(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='3'
		self.dispText.setText(strfn)

	def num4(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='4'
		self.dispText.setText(strfn)

	def num5(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='5'
		self.dispText.setText(strfn)

	def num6(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='6'
		self.dispText.setText(strfn)

	def num7(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='7'
		self.dispText.setText(strfn)

	def num8(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='8'
		self.dispText.setText(strfn)

	def num9(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='9'
		self.dispText.setText(strfn)

	def num0(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='0'
		self.dispText.setText(strfn)

	def num0(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='0'
		self.dispText.setText(strfn)

	def decimal(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='.'
		self.dispText.setText(strfn)

	def openB(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='('
		self.dispText.setText(strfn)

	def closedB(self):
		strfn=str(self.dispText.toPlainText())
		strfn+=')'
		self.dispText.setText(strfn)

	def pi(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='pi'
		self.dispText.setText(strfn)

	def e(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='e'
		self.dispText.setText(strfn)

	def sin(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='sin('
		self.dispText.setText(strfn)

	def cos(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='cos('
		self.dispText.setText(strfn)

	def tan(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='tan('
		self.dispText.setText(strfn)

	def log(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='log('
		self.dispText.setText(strfn)

	def ln(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='ln('
		self.dispText.setText(strfn)

	def xraisey(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='^'
		self.dispText.setText(strfn)

	def tenraise(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='10^'
		self.dispText.setText(strfn)

	def eraise(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='e^'
		self.dispText.setText(strfn)

	def sqr(self):
		strfn=str(self.dispText.toPlainText())
		strfn+='^2'
		self.dispText.setText(strfn)

	def ans(self):
		strfn=str(self.dispText.toPlainText())
		finalans=eval(strfn)
		self.dispText.setText(str(finalans))

	def clear(self):
		self.dispText.setText("")

		 
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())