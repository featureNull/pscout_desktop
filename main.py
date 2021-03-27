import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import qdarkstyle
from mainwindow import MainWindow
from application import Application


def _show_splash_screen():
    pixmap = QPixmap('./ui/png/splashlogo.png')
    lbl = QLabel('')
    lbl.setPixmap(pixmap)
    lbl.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    lbl.show()
    return lbl


if __name__ == "__main__":
    app = Application(sys.argv)
    logo = QPixmap('./ui/png/tasklogo.png')
    app.setWindowIcon(QIcon(logo))

    style = qdarkstyle.load_stylesheet()
    app.setStyleSheet(style)

    lbl = _show_splash_screen()
    app.connectServer()
    lbl.hide()

    wnd = MainWindow()
    wnd.show()
    app.exec_()

    app.closeConnection()
