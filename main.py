import os
import sys
import platform

os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '1'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
os.environ['QT_SCALE_FACTOR'] = '1'

from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMessageBox
from ui_main import FontChangerWindow
from theme import ThemeManager
from language import LanguageManager


def main():
    app = QApplication(sys.argv)

    if platform.system() != 'Windows':
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle('Error')
        msg.setText('This application only runs on Windows.')
        msg.exec()
        return

    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'Kouprey Logo White-icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    app.setApplicationName('Kouprey-Window-Font-Changer')
    app.setOrganizationName('Kouprey')

    font = QFont('Leelawadee UI', 11)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)

    lang_dir = os.path.join(os.path.dirname(__file__), 'assets', 'lang')
    lang = LanguageManager(lang_dir)
    lang.switch_to('km')

    theme_mgr = ThemeManager(app)
    theme_mgr.set_mode('light')

    window = FontChangerWindow(lang, theme_mgr)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
