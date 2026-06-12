from PyQt6.QtCore import QObject
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication


class ThemeColors:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


LIGHT_COLORS = ThemeColors(
    Surface='#FFFFFF',
    SurfaceAlt='#FFFFFF',
    SurfaceCard='#FFFFFF',
    SurfaceHover='#F0F0F0',
    TextPrimary='#000000',
    TextSecondary='#555555',
    Accent='#000000',
    AccentLight='#E6E6E6',
    AccentHover='#333333',
    AccentPressed='#666666',
    Border='#D4D4D4',
    BorderSubtle='#E8E8E8',
    TextOnAccent='#FFFFFF',
)

DARK_COLORS = ThemeColors(
    Surface='#000000',
    SurfaceAlt='#1A1A1A',
    SurfaceCard='#1A1A1A',
    SurfaceHover='#2A2A2A',
    TextPrimary='#FFFFFF',
    TextSecondary='#AAAAAA',
    Accent='#FFFFFF',
    AccentLight='#333333',
    AccentHover='#CCCCCC',
    AccentPressed='#999999',
    Border='#333333',
    BorderSubtle='#2A2A2A',
    TextOnAccent='#000000',
)


def _build_stylesheet(c: ThemeColors) -> str:
    return ''.join([
        '\nQMainWindow, QWidget {\n    background-color: ',
        c.Surface,
        ';\n    color: ',
        c.TextPrimary,
        ';\n    font-size: 11pt;\n}\nQFrame#card {\n    background: ',
        c.SurfaceAlt,
        ';\n    border: 1px solid ',
        c.Border,
        ';\n    border-radius: 8px;\n}\nQLabel#titleLabel {\n    font-size: 16pt;\n    font-weight: 600;\n    color: ',
        c.TextPrimary,
        ';\n    letter-spacing: -0.5px;\n    background: transparent;\n}\nQLabel#subtitleLabel {\n    font-size: 11pt;\n    color: ',
        c.TextSecondary,
        ';\n    background: transparent;\n}\nQLabel#footerLabel {\n    font-size: 9pt;\n    color: ',
        c.TextSecondary,
        ';\n    padding-top: 4px;\n    background: transparent;\n}\nQPushButton {\n    background: ',
        c.SurfaceAlt,
        ';\n    color: ',
        c.TextPrimary,
        ';\n    border: 1px solid ',
        c.Border,
        ';\n    border-radius: 6px;\n    padding: 6px 18px;\n    font-size: 11pt;\n    font-weight: 500;\n    min-height: 28px;\n}\nQPushButton:hover {\n    background: ',
        c.SurfaceHover,
        ';\n    border-color: ',
        c.Border,
        ';\n}\nQPushButton:pressed {\n    background: ',
        c.Border,
        ';\n}\nQPushButton#btn_accent {\n    background: ',
        c.Accent,
        ';\n    color: ',
        c.TextOnAccent,
        ';\n    border: 1px solid ',
        c.Accent,
        ';\n    font-weight: 600;\n}\nQPushButton#btn_accent:hover {\n    background: ',
        c.AccentHover,
        ';\n    border-color: ',
        c.AccentHover,
        ';\n    color: ',
        c.TextOnAccent,
        ';\n}\nQPushButton#btn_accent:pressed {\n    background: ',
        c.AccentPressed,
        ';\n    border-color: ',
        c.AccentPressed,
        ';\n    color: ',
        c.TextOnAccent,
        ';\n}\nQPushButton#btn_icon {\n    background: transparent;\n    border: none;\n    border-radius: 6px;\n    padding: 6px;\n    min-height: 32px;\n    min-width: 32px;\n}\nQPushButton#btn_icon:hover {\n    background: ',
        c.SurfaceHover,
        ';\n}\nQTableWidget {\n    background: ',
        c.SurfaceCard,
        ';\n    border: 1px solid ',
        c.Border,
        ';\n    border-radius: 8px;\n    gridline-color: transparent;\n    outline: none;\n}\nQTableWidget::item {\n    padding: 8px 12px;\n    border: none;\n    border-bottom: 1px solid ',
        c.BorderSubtle,
        ';\n}\nQTableWidget::item:hover {\n    background: ',
        c.SurfaceHover,
        ';\n}\nQTableWidget::item:selected {\n    background: ',
        c.AccentLight,
        ';\n    color: ',
        c.TextPrimary,
        ';\n}\nQHeaderView::section {\n    background: transparent;\n    color: ',
        c.TextSecondary,
        ';\n    border: none;\n    border-bottom: 1px solid ',
        c.Border,
        ';\n    padding: 8px 12px;\n    font-weight: 600;\n    font-size: 10pt;\n}\nQTableWidget::item:alternate {\n    background: transparent;\n}\n',
    ])


class ThemeManager(QObject):
    def __init__(self, app: QApplication):
        super().__init__()
        self._app = app
        self._mode = 'light'

    def get_mode(self) -> str:
        return self._mode

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        colors = DARK_COLORS if mode == 'dark' else LIGHT_COLORS
        self._apply(colors)

    def toggle(self) -> str:
        new = 'dark' if self._mode == 'light' else 'light'
        self.set_mode(new)
        return new

    def _apply(self, c: ThemeColors) -> None:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(c.Surface))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(c.TextPrimary))
        palette.setColor(QPalette.ColorRole.Base, QColor(c.SurfaceCard))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(c.SurfaceAlt))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(c.SurfaceCard))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(c.TextPrimary))
        palette.setColor(QPalette.ColorRole.Text, QColor(c.TextPrimary))
        palette.setColor(QPalette.ColorRole.Button, QColor(c.SurfaceCard))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(c.TextPrimary))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(c.TextPrimary))
        palette.setColor(QPalette.ColorRole.Link, QColor(c.Accent))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(c.Accent))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(c.TextPrimary))
        self._app.setPalette(palette)

        stylesheet = _build_stylesheet(c)
        self._app.setStyleSheet(stylesheet)
