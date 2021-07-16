import sys
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import qdarkstyle
from mainwindow import MainWindow
from resultwindow_neu import ResultWindowNeu
from application import Application
from settings_dialog import SettingsDialog


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

    try:
        lbl = _show_splash_screen()
        istgutgelaufen = True
        app.loadConfig()
        app.connectServer()
    except Exception as ex:
        istgutgelaufen = False
        QMessageBox.critical(None, "ma", str(ex))
    finally:
        lbl.hide()

    if istgutgelaufen:
        #app.mainWindow = ResultWindowNeu()
        app.mainWindow = MainWindow()
        app.mainWindow.show()
        app.exec_()
        app.closeConnection()
    else:
        # wenns nicht gut geht, dialog auftun, dass man connection aendern kann
        dlg = SettingsDialog(app.settings)
        dlg.show()
        app.exec_()
        if dlg.result() == SettingsDialog.Accepted:
            app.settings = dlg.getData()
            app.saveConfig()
