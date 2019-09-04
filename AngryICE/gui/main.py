from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
import timeloop
from datetime import timedelta

t = timeloop.Timeloop()
@t.job(interval=timedelta(seconds=1))
def run():
    # win.label.setText(win.label.text() + '1')
    win.label.setPixmap(QPixmap('image1.png'))
app = QApplication([])
win = uic.loadUi('mainwindow.ui')
t.start(block=False)
win.show()
app.exec()
