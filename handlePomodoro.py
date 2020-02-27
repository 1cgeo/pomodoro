import time
from datetime import date, timedelta
from PyQt5.QtCore import QThread, pyqtSignal
from qgis.core import QgsSettings
from .userHistoric import UserHistoric

class HandlePomodoro(QThread):

    updateTimer = pyqtSignal(int)
    updateHistoric = pyqtSignal(list)
    wasSucessful = pyqtSignal()

    def __init__(self, parent=None):
        super(HandlePomodoro, self).__init__(parent)
        self.running = True
        # TODO: Use QTimer()
        self.duration = 30
        self.today = date.today
        self.isTimerRunning = True
        # TODO: use a simple array
        self.session = {
            'historic' : []
        }
        self.historic = UserHistoric()

    def run(self):
        while self.running:
            if self.duration:
                for i in range(self.duration):
                    if self.isTimerRunning:
                        self.updateTimer.emit(i)
                        self.duration -= 1
                        if not self.duration:
                            self.session['historic'].append(True)
                            self.updateHistoric.emit(self.session['historic'])
                            self.isTimerRunning = False
                        # TODO: use QThread.sleep()
                        time.sleep(1)

        # timer = QTimer(self)
        # timer.setInterval(1000)
        # timer.timeout.connect(self.updateText)
        # timer.start()

    def changeState(self):
        self.running = ~self.running

    def refreshPomodoro(self, isMonitoring=True):
        # TODO: append the pixmap itself
        if isMonitoring:
            if self.duration:
                # TODO: call a function which triggers the append and updates the userHistoric
                self.session['historic'].append(False)
            self.updateHistoric.emit(self.session['historic'])
        self.duration = 30
        self.isTimerRunning = True
        # print(self.session)

    def refreshPomodoroByMonitor(self):
        self.isTimerRunning = False
        if self.duration:
            self.session['historic'].append(False)
        self.updateHistoric.emit(self.session['historic'])

    def lcdString(self):
        return '{:2}:{:0>2}'.format(self.duration // 60, self.duration % 60)

    def tick(self):
        self.duration -= 1

if __name__ == "__main__":
    pomodoro = HandlePomodoro()
    pomodoro.run()