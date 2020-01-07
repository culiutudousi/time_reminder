# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QLabel, QPushButton, QMessageBox,
                             QVBoxLayout, QHBoxLayout, QApplication, QFrame)


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.work_frame = QFrame(self)
        self.work_frame.setFrameShape(QFrame.StyledPanel)
        self.work_widget = ReminderWidget(self.work_frame)
        self.work_widget.setButtonTitle('Work!')
        self.work_widget.setRemindContent('Rest!')
        self.work_widget.setTime(50)

        self.rest_frame = QFrame(self)
        self.rest_frame.setFrameShape(QFrame.StyledPanel)
        self.rest_widget = ReminderWidget(self.rest_frame)
        self.rest_widget.setButtonTitle('Rest!')
        self.rest_widget.setRemindContent('Work!')
        self.rest_widget.setTime(10)

        self.work_widget.set_button_enable_signal.connect(self.setComponentsEnable)
        self.rest_widget.set_button_enable_signal.connect(self.setComponentsEnable)

        self.box = QHBoxLayout()
        self.box.addWidget(self.work_frame)
        self.box.addWidget(self.rest_frame)

        self.setLayout(self.box)

        self.setGeometry(300, 300, 270, 200)
        self.setWindowTitle('Time Reminder')
        self.show()

    def setComponentsEnable(self, bool):
        self.work_widget.setButtonEnable(bool)
        self.work_widget.setSliderEnable(bool)
        self.rest_widget.setButtonEnable(bool)
        self.rest_widget.setSliderEnable(bool)


class ReminderWidget(QWidget):

    set_button_enable_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ReminderWidget, self).__init__(parent)
        self.initUI()
        self.remind_content = 'reminder!'
        self.time = 0

    def initUI(self):
        self.time_setting = TimeSettingWidget(self)
        self.start_button = QPushButton('')
        self.start_button.setStyleSheet("QPushButton{font-size: 16px;font-family: Arial;}")

        self.box = QVBoxLayout()
        self.box.addWidget(self.time_setting)
        self.box.addWidget(self.start_button)
        self.setLayout(self.box)

        self.start_button.clicked.connect(self.onStartButtonClicked)

    def setButtonTitle(self, str):
        self.start_button.setText(str)

    def setButtonEnable(self, bool):
        self.start_button.setEnabled(bool)

    def setSliderEnable(self, bool):
        self.time_setting.setSliderEnable(bool)

    def setRemindContent(self, str):
        self.remind_content = str

    def setTime(self, t):
        self.time_setting.setTime(t)

    def onStartButtonClicked(self):
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.time = self.time_setting.getTime()
        self.timer.timeout.connect(self.elapse)
        self.set_button_enable_signal.emit(False)
        self.time_setting.setActiveStyle()
        self.timer.start(1000 * 60)
        # self.timer.start(500)

    def elapse(self):
        self.time -= 1
        self.time_setting.setDisplayTime(self.time)
        if self.time <= 0:
            self.timer.stop()
            self.remind()
            self.time_setting.freshDisplayTime()
            self.set_button_enable_signal.emit(True)
            self.time_setting.setInactiveStyle()

    def remind(self):
        msgBox = QMessageBox(QMessageBox.NoIcon, ' ', self.remind_content)
        msgBox.setWindowFlags(msgBox.windowFlags() | Qt.WindowStaysOnTopHint)
        msgBox.setStyleSheet("QMessageBox{font-size: 16px;font-family: Arial;min-width:500 px;}")
        msgBox.exec()


class TimeSettingWidget(QWidget):

    def __init__(self, parent=None):
        super(TimeSettingWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.lcd = QLCDNumber(self)
        self.lcd.setNumDigits(2)
        self.lcd.setMinimumHeight(80)
        self.lcd.setStyleSheet("QLCDNumber{ color: black;}")
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setMinimum(1)
        self.sld.setMaximum(90)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.lcd)
        self.vbox.addWidget(self.sld)

        self.setLayout(self.vbox)
        self.sld.valueChanged.connect(self.lcd.display)

    def setTime(self, t):
        self.sld.setValue(t)

    def setDisplayTime(self, t):
        self.lcd.display(t)

    def setActiveStyle(self):
        self.lcd.setStyleSheet("QLCDNumber{ color: green;}")

    def setInactiveStyle(self):
        self.lcd.setStyleSheet("QLCDNumber{ color: black;}")

    def setSliderEnable(self, bool):
        self.sld.setEnabled(bool)

    def freshDisplayTime(self):
        self.lcd.display(self.sld.value())

    def getTime(self):
        return self.sld.value()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
