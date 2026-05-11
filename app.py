import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from config import Config
from main_window import MainWindow
from utils.icons import resolve_icon_theme

config: Config = Config.load()
app: QApplication = QApplication(sys.argv)

QIcon.setThemeName(resolve_icon_theme(config.settings["theme"]))


window: MainWindow = MainWindow(config)
window.show()

sys.exit(app.exec())
