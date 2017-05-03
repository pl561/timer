#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/SIC/plefevre/gui_timer.ui'
#
# Created by: PyQt4 UI code generator 4.12.1.dev1703241106
#
# WARNING! All changes made in this file will be lost!

# http://stackoverflow.com/questions/12661211/cant-seem-to-get-pyqt-countdown-timer-to-work
# http://stackoverflow.com/questions/16982588/cant-type-in-qlineedit-if-the-keypressevent-is-on (how to reimplement keyPressEvent())
import os
import sys
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class myLCDNumber(QtGui.QLCDNumber):
    value = 60
    stop_signal = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def count(self):
        self.display(conversion_min_fromsec(self.value))
        if self.value > 0:
            self.value = self.value - 1
        else:
            self.stop_signal.emit()
            sound_path = '../sounds/sms-alert-4-daniel_simon.wav'
            os.system('aplay {}&'.format(sound_path))
            os.system('aplay {}&'.format(sound_path))


class myQLineEdit(QtGui.QLineEdit):
    my_customsignal = QtCore.pyqtSignal()

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
            self.my_customsignal.emit()
        else:
            super(myQLineEdit, self).keyPressEvent(event)


class TimerWidget(QtGui.QMainWindow):
    def __init__(self, position=(10, 10), size=(1600, 600)):
        super(TimerWidget, self).__init__()
        p_x, p_y = position
        s_x, s_y = size
        self.setGeometry(p_x, p_y, s_x, s_y)
        self.setWindowTitle('Timer application')
        QtGui.QToolTip.setFont(QtGui.QFont('Monospace', 12))

        self.setup_ui(self)

    def setup_ui(self, MainWindow):
        # MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(400, 268)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.timer = QtCore.QTimer()

        self.timer_stop = QtGui.QPushButton(self.centralwidget)
        self.timer_stop.setGeometry(QtCore.QRect(290, 10, 98, 27))
        self.timer_stop.setObjectName(_fromUtf8("timer_stop"))
        self.timer_stop.clicked.connect(self.trigger_stop)

        self.timer_reset = QtGui.QPushButton(self.centralwidget)
        self.timer_reset.setGeometry(QtCore.QRect(190, 50, 98, 27))
        self.timer_reset.setObjectName(_fromUtf8("timer_reset"))
        self.timer_reset.clicked.connect(self.trigger_reset)

        self.timer_start = QtGui.QPushButton(self.centralwidget)
        self.timer_start.setGeometry(QtCore.QRect(190, 10, 98, 27))
        self.timer_start.setObjectName(_fromUtf8("timer_start"))
        self.timer_start.clicked.connect(self.trigger_start)

        self.timer_timeamount = myQLineEdit(self.centralwidget)
        self.timer_timeamount.setGeometry(QtCore.QRect(290, 50, 98, 27))
        self.timer_timeamount.setObjectName(_fromUtf8("timer_timeamount"))
        self.timer_timeamount.setText('60')
        self.readvalue_fromqle()
        self.timer_timeamount.my_customsignal.connect(self.trigger_action_qle)
        # self.timer_timeamount.returnPressed.connect(self.trigger_action_qle)


        # self.start_action = QtGui.QAction(None, 'Start timer key event',
        #                                   parent=self.timer_timeamount)
        # self.start_action.setShortcut(QtCore.Qt.Key_Return)
        # self.start_action.triggered.connect(self.trigger_action_qle)

        self.timer_set25 = QtGui.QPushButton('25 min',
                                             parent=self.centralwidget)
        self.timer_set25.setGeometry(QtCore.QRect(190, 90, 98, 27))
        self.timer_set25.setObjectName(_fromUtf8("timer_set25"))
        self.timer_set25.clicked.connect(self.trigger_set25)

        self.timer_set10 = QtGui.QPushButton('10 min',
                                             parent=self.centralwidget)
        self.timer_set10.setGeometry(QtCore.QRect(290, 90, 98, 27))
        self.timer_set10.setObjectName(_fromUtf8("timer_set10"))
        self.timer_set10.clicked.connect(self.trigger_set10)

        self.timer_set15 = QtGui.QPushButton('15 min',
                                             parent=self.centralwidget)
        self.timer_set15.setGeometry(QtCore.QRect(190, 130, 98, 27))
        self.timer_set15.setObjectName(_fromUtf8("timer_set15"))
        self.timer_set15.clicked.connect(self.trigger_set15)

        self.timer_set5 = QtGui.QPushButton('5 min', parent=self.centralwidget)
        self.timer_set5.setGeometry(QtCore.QRect(290, 130, 98, 27))
        self.timer_set5.setObjectName(_fromUtf8("timer_set5"))
        self.timer_set5.clicked.connect(self.trigger_set5)

        self.timer_display = myLCDNumber(self.centralwidget)
        self.timer_display.setGeometry(QtCore.QRect(10, 10, 171, 121))
        self.timer_display.setObjectName(_fromUtf8("timer_display"))
        self.timer_display.display(conversion_min_fromsec(self.amount))
        # self.timer_display.connect(self.timer, QtCore.SIGNAL('timeout()'), self.timer_display, QtCore.SLOT('count()'))

        # self.timer.timeout.connect(self.timer_display.count)
        self.timer.timeout.connect(self.trigger_count)
        self.timer_display.stop_signal.connect(self.trigger_stop)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.timer_stop.setText(_translate("MainWindow", "Stop", None))
        self.timer_reset.setText(_translate("MainWindow", "Reset", None))
        self.timer_start.setText(_translate("MainWindow", "Start", None))

    def trigger_start(self):
        # self.timer_display.value = self.amount - 1
        self.timer.start(1000)

    def trigger_stop(self):
        self.timer.stop()

    def trigger_reset(self):
        self.readvalue_fromqle()
        self.timer_display.value = self.amount
        self.timer_display.display(conversion_min_fromsec(self.amount))

    def trigger_action_qle(self):
        self.trigger_reset()
        self.trigger_start()
        self.statusbar.showMessage('Starting countdown:{}.'.format(self.amount))

    def readvalue_fromqle(self):
        text = self.timer_timeamount.text()

        try:
            self.amount = int(text)

            msg = 'Timer countdown from {}.'.format(text)
            self.statusbar.showMessage(msg)
        except ValueError:
            self.statusbar.showMessage('Invalid time amount !')
            return

    def trigger_set25(self):
        self.timer_timeamount.setText('1500')
        self.trigger_reset()
        self.trigger_start()

    def trigger_set10(self):
        self.timer_timeamount.setText('600')
        self.trigger_reset()
        self.trigger_start()

    def trigger_set15(self):
        self.timer_timeamount.setText('900')
        self.trigger_reset()
        self.trigger_start()

    def trigger_set5(self):
        self.timer_timeamount.setText('300')
        self.trigger_reset()
        self.trigger_start()

    def trigger_count(self):
        title = conversion_min_fromsec(self.timer_display.value)
        self.setWindowTitle(title)
        self.timer_display.count()


def conversion_min_fromsec(seconds):
    minutes, seconds = divmod(seconds, 60)
    minutes = str(minutes).zfill(2)
    seconds = str(seconds).zfill(2)
    return '{}:{}'.format(minutes, seconds)


def main():
    app = QtGui.QApplication(sys.argv)
    window = TimerWidget(position=(30, 60))
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main())
