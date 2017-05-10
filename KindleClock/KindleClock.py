__author__ = 'francisco'

import KindleClock_UI
import analogclock
from PyQt4 import QtCore, QtGui
import datetime

class Ui_MainWindowImpl(KindleClock_UI.Ui_MainWindow):

    def setupUi(self, MainWindow):

        # Variables

        # Analog Clock Variables
        super(Ui_MainWindowImpl, self).setupUi(MainWindow)
        self.AnalogClockWidget = analogclock.PyAnalogClock(self.tab1)
        self.AnalogClockWidget.setGeometry(QtCore.QRect(40, 90, 450, 450))

        # Alarm variables
        self.alarm_hour = 0
        self.alarm_minutes = 0
        self.alarm_seconds = 0
        self.alarm_clear = False

        # Chronometer variables
        self.chron_hour = 0
        self.chron_minutes = 0
        self.chron_seconds = 0
        self.chron_pause = False

        # StopWatch variables
        self.swatch_hour = 0
        self.swatch_minutes = 0
        self.swatch_seconds = 0
        self.swatch_clear = False

        # Digital Clock Timer creation
        self.timerDC=QtCore.QTimer()
        self.timerDC.timeout.connect(self.timerDC_func)
        self.timerDC.start(1000)
        self.timerDC_func()


        # Connecting buttons

        # Alarm buttons
        self.pushButton_3.clicked.connect(self.inc_alarm_hour_func)
        self.pushButton_11.clicked.connect(self.dec_alarm_hour_func)
        self.pushButton_4.clicked.connect(self.inc_alarm_minutes_func)
        self.pushButton_10.clicked.connect(self.dec_alarm_minutes_func)
        self.pushButton_15.clicked.connect(self.alarm_set)

        # Chronometer buttons
        self.pushButton.clicked.connect(self.startCH_func)
        self.pushButton_2.clicked.connect(self.stopCH_func)

        # StopWatch buttons
        self.pushButton_8.clicked.connect(self.inc_swatch_hour_func)
        self.pushButton_13.clicked.connect(self.dec_swatch_hour_func)
        self.pushButton_7.clicked.connect(self.inc_swatch_minutes_func)
        self.pushButton_14.clicked.connect(self.dec_swatch_minutes_func)
        self.pushButton_6.clicked.connect(self.inc_swatch_seconds_func)
        self.pushButton_12.clicked.connect(self.dec_swatch_seconds_func)

        self.pushButton_16.clicked.connect(self.startSW_func)

        # MenuBar
        self.actionQuit.triggered.connect(self.actionQuit_fun)
        self.actionAbout_KindleClock.triggered.connect(self.actionAbout_KindleClock_func)

    # Digital Clock funtions
    def timerDC_func(self):
        """Digital Clock Timer function"""
        # Get python time
        x = datetime.datetime.now()

        # Divide time in digits
        h0 = x.hour/10
        h1 = x.hour%10
        m0 = x.minute/10
        m1 = x.minute%10
        s0 = x.second/10
        s1 = x.second%10

        # Show time in displays
        self.lcdNumber_4.display(h0)
        self.lcdNumber.display(h1)
        self.lcdNumber_2.display(m0)
        self.lcdNumber_5.display(m1)
        #self.lcdNumber_3.display(s0)
        #self.lcdNumber_6.display(s1)

    # Alarm functions
    def alarm_set(self):
        # Alarm Timer creation
        self.timerAL=QtCore.QTimer()
        self.timerAL.timeout.connect(self.timerAL_func)
        self.timerAL.start(500)

    def timerAL_func(self):
        """Alarm Timer function"""
        # Get python time
        x = datetime.datetime.now()
        if (x.hour == self.alarm_hour and x.minute == self.alarm_minutes and x.second == self.alarm_seconds):
            self.alarm_hour = 0
            self.alarm_minutes = 0
            self.alarm_seconds = 0

            QtGui.QMessageBox.about(QtGui.QMainWindow(), "L:A_N:application_ID:KC Alarm Notice",
                "<H1>Alarm Activated</H1>".decode("utf8"))

    def alarm_updateUI_func(self):
        # Show time in displays
        self.lcdNumber_7.display(self.alarm_hour/10)
        self.lcdNumber_8.display(self.alarm_hour%10)
        self.lcdNumber_9.display(self.alarm_minutes/10)
        self.lcdNumber_10.display(self.alarm_minutes%10)
        #self.lcdNumber_11.display(self.alarm_seconds/10)
        #self.lcdNumber_12.display(self.alarm_seconds%10)

    def inc_alarm_hour_func(self):
        self.alarm_hour+=1

        if self.alarm_hour > 23 :
            self.alarm_hour = 0

        self.alarm_updateUI_func()

    def dec_alarm_hour_func(self):
        self.alarm_hour-=1

        if self.alarm_hour < 0 :
            self.alarm_hour = 23

        self.alarm_updateUI_func()

    def inc_alarm_minutes_func(self):
        self.alarm_minutes+=1

        if self.alarm_minutes > 59 :
            self.alarm_minutes = 0

        self.alarm_updateUI_func()

    def dec_alarm_minutes_func(self):
        self.alarm_minutes-=1

        if self.alarm_minutes < 0 :
            self.alarm_minutes = 59

        self.alarm_updateUI_func()

    def inc_alarm_seconds_func(self):
        self.alarm_seconds+=1

        if self.alarm_seconds > 59 :
            self.alarm_seconds = 0

        self.alarm_updateUI_func()

    def dec_alarm_seconds_func(self):
        self.alarm_seconds-=1

        if self.alarm_seconds < 0 :
            self.alarm_seconds = 59

        self.alarm_updateUI_func()

    # Chronometrs functions
    def startCH_func(self):
        if (self.chron_pause == False):
            self.chron_updateUI_func()
            # Chronometer Timer creation
            self.timerCH=QtCore.QTimer()
            self.timerCH.timeout.connect(self.timerCH_func)
            self.timerCH.start(1000)
            self.chron_pause = True
            self.pushButton.setText("PAUSE")
        else:
            self.timerCH.stop()
            self.chron_pause = False
            self.pushButton.setText("START")

    def stopCH_func(self):
        self.chron_seconds = 0
        self.chron_minutes = 0
        self.chron_hour = 0

        self.timerCH.stop()
        self.chron_pause = False
        self.pushButton.setText("START")

    def timerCH_func(self):
        self.chron_update_func()
        self.chron_updateUI_func()

    def chron_update_func(self):
        self.chron_seconds += 1

        if (self.chron_seconds > 59):
            self.chron_seconds = 0
            self.chron_minutes += 1

        if (self.chron_minutes > 59):
            self.chron_minutes = 0
            self.chron_hour += 1

        if (self.chron_hour > 99):
            self.chron_seconds = 0
            self.chron_minutes = 0
            self.chron_hour = 0

            QtGui.QMessageBox.about(QtGui.QMainWindow(), "L:A_N:application_ID:KC Chronometer Notice",
                "<H1>Chronometer time stored :(</H1>".decode("utf8"))


        # Show time in displays
        self.lcdNumber_13.display(self.chron_hour/10)
        self.lcdNumber_14.display(self.chron_hour%10)
        self.lcdNumber_15.display(self.chron_minutes/10)
        self.lcdNumber_16.display(self.chron_minutes%10)
        self.lcdNumber_17.display(self.chron_seconds/10)
        self.lcdNumber_18.display(self.chron_seconds%10)

    def chron_updateUI_func(self):
        # Show time in displays
        self.lcdNumber_13.display(self.chron_hour/10)
        self.lcdNumber_14.display(self.chron_hour%10)
        self.lcdNumber_15.display(self.chron_minutes/10)
        self.lcdNumber_16.display(self.chron_minutes%10)
        self.lcdNumber_17.display(self.chron_seconds/10)
        self.lcdNumber_18.display(self.chron_seconds%10)

    # StopWatch functions
    def startSW_func(self):
        if (self.swatch_clear == False):
            # StopWatch Timer creation
            self.timerSW=QtCore.QTimer()
            self.timerSW.timeout.connect(self.timerSW_func)
            self.timerSW.start(1000)
            self.swatch_clear = True
            self.pushButton_16.setText("CLEAR")
        else:
            self.timerSW.stop()
            self.swatch_clear = False
            self.swatch_seconds = 0
            self.swatch_minutes = 0
            self.swatch_hour = 0
            self.swatch_updateUI_func()
            self.pushButton_16.setText("SET")

    def timerSW_func(self):
        self.swatch_update_func()
        self.swatch_updateUI_func()

    def swatch_update_func(self):
        self.swatch_seconds -= 1

        if (self.swatch_seconds < 0):
            self.swatch_seconds = 59
            self.swatch_minutes -= 1

        if (self.swatch_minutes <0):
            self.swatch_minutes = 59
            self.swatch_hour -= 1

        if (self.swatch_hour == 00 and self.swatch_minutes == 0 and self.swatch_seconds == 0):
            self.timerSW.stop()
            self.swatch_clear = False
            self.swatch_seconds = 0
            self.swatch_minutes = 0
            self.swatch_hour = 0
            self.swatch_updateUI_func()
            self.pushButton_16.setText("SET")
            QtGui.QMessageBox.about(QtGui.QMainWindow(), "L:A_N:application_ID:KC StopWatch Notice",
                "<H1>StopWatch time stored :(</H1>".decode("utf8"))

    def swatch_updateUI_func(self):
        # Show time in displays
        self.lcdNumber_19.display(self.swatch_hour/10)
        self.lcdNumber_20.display(self.swatch_hour%10)
        self.lcdNumber_21.display(self.swatch_minutes/10)
        self.lcdNumber_22.display(self.swatch_minutes%10)
        self.lcdNumber_23.display(self.swatch_seconds/10)
        self.lcdNumber_24.display(self.swatch_seconds%10)

    def inc_swatch_hour_func(self):
        self.swatch_hour+=1

        if self.swatch_hour > 23 :
            self.swatch_hour = 0

        self.swatch_updateUI_func()

    def dec_swatch_hour_func(self):
        self.swatch_hour-=1

        if self.swatch_hour < 0 :
            self.swatch_hour = 23

        self.swatch_updateUI_func()

    def inc_swatch_minutes_func(self):
        self.swatch_minutes+=1

        if self.swatch_minutes > 59 :
            self.swatch_minutes = 0

        self.swatch_updateUI_func()

    def dec_swatch_minutes_func(self):
        self.swatch_minutes-=1

        if self.swatch_minutes < 0 :
            self.swatch_minutes = 59

        self.swatch_updateUI_func()

    def inc_swatch_seconds_func(self):
        self.swatch_seconds+=1

        if self.swatch_seconds > 59 :
            self.swatch_seconds = 0

        self.swatch_updateUI_func()

    def dec_swatch_seconds_func(self):
        self.swatch_seconds-=1

        if self.swatch_seconds < 0 :
            self.swatch_seconds = 59

        self.swatch_updateUI_func()

    # Actions functions
    def actionQuit_fun(self):
        quit()

    def actionAbout_KindleClock_func(self):
        QtGui.QMessageBox.about(QtGui.QMainWindow(), "L:A_N:application_ID:About KindleClock",
                "<H3>About KindleClock</H3>"
                "<br>KindleClock is an application for time jobs, include: "
                "<br>Analog Clock, Digital Clock, Alarm, Chronometer, StopWatch"
                "<br>and Calendar. It's developed in PyQt4."
                "<br><br>Programer: Francisco Perdigon Romero (AKA bosito7)."
                "<br>Email: <a href=\"mailto:bosito7@gmail.com\">bosito7@gmail.com</a>"
                "<br>Licence: GPL v3."
                "<br><br>WEB:."
                "<br> <a href=\"http://www.mobileread.com/\">http://www.mobileread.com/</a> "
                "<br> <a href=\"https://gutl.jovenclub.cu/\">https://gutl.jovenclub.cu/</a> "
                "<br><br>Chat IRC WEB:."
                "<br> <a href=\"https://irc.mr.gd/\">https://irc.mr.gd/</a> ".decode("utf8"))

    def retranslateUi(self, MainWindow):
        super(Ui_MainWindowImpl, self).retranslateUi(MainWindow)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindowImpl()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
