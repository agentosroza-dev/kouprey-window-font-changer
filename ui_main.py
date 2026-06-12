import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QMessageBox, QFrame, QApplication,
    QFontDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap

from icons import lucide_icon
from theme import LIGHT_COLORS, DARK_COLORS
import win32_metrics
import PyQt6.QtWidgets as QtWidgets


class FontChangerWindow(QMainWindow):
    def __init__(self, lang, theme_mgr=None):
        super().__init__()
        self._lang = lang
        self._theme_mgr = theme_mgr
        self._theme_colors = LIGHT_COLORS

        self.setWindowTitle(lang.get('app_title'))
        self.setMinimumSize(750, 540)

        app_icon = QApplication.instance().windowIcon()
        if not app_icon.isNull():
            self.setWindowIcon(app_icon)

        self.dpi = win32_metrics.get_screen_dpi()
        self.font_data = {}

        self._load_fonts()

        central = QWidget()
        self.setCentralWidget(central)

        self.layout = QVBoxLayout(central)
        self.layout.setContentsMargins(32, 24, 32, 24)
        self.layout.setSpacing(20)

        self._build_title_row()
        self._build_subtitle()
        self._build_card()
        self._build_footer()
        self._connect_signals()

    def _build_title_row(self):
        title_row = QHBoxLayout()
        title_row.setSpacing(10)

        self.logo_label = QLabel()
        self.logo_label.setFixedSize(40, 40)

        self._base = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        self._update_logo()

        title_row.addWidget(self.logo_label)

        self.title_label = QLabel(self._lang.get('window_title'))
        self.title_label.setObjectName('titleLabel')
        title_row.addWidget(self.title_label)

        title_row.addStretch()

        icon_color = self._current_text_color()

        self.btn_lang = QPushButton()
        self.btn_lang.setObjectName('btn_icon')
        self.btn_lang.setIcon(lucide_icon('languages', 20, icon_color))
        self.btn_lang.setToolTip(self._lang.get('lang_tooltip').format(lang=self._lang.get('english')))
        self.btn_lang.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_lang.setFixedSize(36, 36)
        title_row.addWidget(self.btn_lang)

        self.btn_theme = QPushButton()
        self.btn_theme.setObjectName('btn_icon')
        self._update_theme_icon()
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.setFixedSize(36, 36)
        title_row.addWidget(self.btn_theme)

        self.layout.addLayout(title_row)

    def _build_subtitle(self):
        self.subtitle_label = QLabel(self._lang.get('subtitle'))
        self.subtitle_label.setObjectName('subtitleLabel')
        self.layout.addWidget(self.subtitle_label)

    def _build_card(self):
        card = QFrame()
        card.setObjectName('card')

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(14)

        bar = QHBoxLayout()
        bar.setSpacing(8)

        self.btn_default = QPushButton(self._lang.get('btn_default'))
        self.btn_change_all = QPushButton(self._lang.get('btn_change_all'))
        self.btn_agentos = QPushButton(self._lang.get('btn_agentos'))

        bar.addWidget(self.btn_default)
        bar.addWidget(self.btn_change_all)
        bar.addWidget(self.btn_agentos)
        bar.addStretch()

        self.btn_apply = QPushButton(self._lang.get('btn_apply'))
        self.btn_apply.setObjectName('btn_accent')
        bar.addWidget(self.btn_apply)

        card_layout.addLayout(bar)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([self._lang.get('col_element'), self._lang.get('col_font')])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(False)
        self.table.setMouseTracking(True)
        self.table.doubleClicked.connect(self._on_change)

        self._populate_table()

        card_layout.addWidget(self.table)
        self.layout.addWidget(card)

    def _build_footer(self):
        footer_layout = QHBoxLayout()

        self.footer_left = QLabel(self._lang.get('footer_creator'))
        self.footer_left.setObjectName('footerLabel')

        self.footer_right = QLabel(self._lang.get('footer_copyright') + ' | v' + self._lang.get('version'))
        self.footer_right.setObjectName('footerLabel')
        self.footer_right.setAlignment(Qt.AlignmentFlag.AlignRight)

        footer_layout.addWidget(self.footer_left)
        footer_layout.addWidget(self.footer_right)

        self.layout.addLayout(footer_layout)

    def _connect_signals(self):
        self.btn_default.clicked.connect(self._on_default)
        self.btn_change_all.clicked.connect(self._on_change_all)
        self.btn_agentos.clicked.connect(self._on_agentos)
        self.btn_apply.clicked.connect(self._on_apply)
        self.btn_lang.clicked.connect(self._on_toggle_lang)
        self.btn_theme.clicked.connect(self._on_toggle_theme)

    def _current_text_color(self):
        c = self._theme_colors
        return c.TextPrimary if c else '#000000'

    def _update_theme_icon(self):
        is_dark = self._theme_mgr and self._theme_mgr.get_mode() == 'dark'
        color = self._current_text_color()
        if is_dark:
            self.btn_theme.setIcon(lucide_icon('moon', 20, color))
            self.btn_theme.setToolTip(self._lang.get('theme_tooltip_dark'))
        else:
            self.btn_theme.setIcon(lucide_icon('sun', 20, color))
            self.btn_theme.setToolTip(self._lang.get('theme_tooltip_light'))

    def _retranslate_ui(self):
        lang = self._lang

        self.setWindowTitle(lang.get('app_title'))
        self.title_label.setText(lang.get('window_title'))
        self.subtitle_label.setText(lang.get('subtitle'))
        self.btn_default.setText(lang.get('btn_default'))
        self.btn_change_all.setText(lang.get('btn_change_all'))
        self.btn_agentos.setText(lang.get('btn_agentos'))
        self.btn_apply.setText(lang.get('btn_apply'))

        self.table.setHorizontalHeaderLabels([lang.get('col_element'), lang.get('col_font')])

        self.footer_left.setText(lang.get('footer_creator'))
        self.footer_right.setText(lang.get('footer_copyright') + ' | v' + lang.get('version'))

        self._update_theme_icon()

        lang_name = lang.get('english') if lang.current_lang == 'en' else lang.get('khmer')
        self.btn_lang.setToolTip(lang.get('lang_tooltip').format(lang=lang_name))

    def _on_toggle_lang(self):
        new_lang = 'km' if self._lang.current_lang == 'en' else 'en'
        self._lang.switch_to(new_lang)

        app = QApplication.instance()
        if app:
            if new_lang == 'km':
                f = QFont('Leelawadee UI', 11)
                f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
            else:
                f = QFont('Segoe UI Variable Display', 11)
                f.setFamilies(['Segoe UI Variable Display', 'Segoe UI', 'sans-serif'])
                f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
            app.setFont(f)

        self._retranslate_ui()

    def _update_logo(self):
        is_dark = self._theme_mgr and self._theme_mgr.get_mode() == 'dark'
        name = 'Kouprey Logo Black.png' if is_dark else 'Kouprey Logo White.png'
        path = os.path.join(self._base, 'assets', 'icons', name)

        if os.path.exists(path):
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def _on_toggle_theme(self):
        if not self._theme_mgr:
            return

        self._theme_mgr.toggle()
        is_dark = self._theme_mgr.get_mode() == 'dark'
        self._theme_colors = DARK_COLORS if is_dark else LIGHT_COLORS
        self._update_theme_icon()
        self._update_logo()

        icon_color = self._current_text_color()
        self.btn_lang.setIcon(lucide_icon('languages', 20, icon_color))

    def _load_fonts(self):
        for name in win32_metrics.ELEMENT_NAMES:
            lf = win32_metrics.get_logfont(name)
            if lf:
                qf = win32_metrics.logfont_to_qfont(lf, self.dpi)
            else:
                qf = QFont('Segoe UI', 9)

            self.font_data[name] = {
                'current': QFont(qf),
                'default': QFont(qf),
            }

    def _font_str(self, qf):
        parts = [f'{qf.family()} {qf.pointSize()}pt']
        w = qf.weight()
        if w >= 700:
            parts.append('Bold')
        elif w >= 600:
            parts.append('SemiBold')
        elif w <= 300:
            parts.append('Light')
        if qf.italic():
            parts.append('Italic')
        return ', '.join(parts)

    def _populate_table(self):
        names = win32_metrics.ELEMENT_NAMES
        self.table.setRowCount(len(names))

        for row, name in enumerate(names):
            item_name = QTableWidgetItem(name)
            item_font = QTableWidgetItem(self._font_str(self.font_data[name]['current']))
            self.table.setItem(row, 0, item_name)
            self.table.setItem(row, 1, item_font)

    def _refresh_table(self):
        for row, name in enumerate(win32_metrics.ELEMENT_NAMES):
            self.table.item(row, 1).setText(self._font_str(self.font_data[name]['current']))

    def _on_change(self, row):
        if row < 0:
            QMessageBox.information(self, self._lang.get('info_title'), self._lang.get('info_select'))
            return

        name = win32_metrics.ELEMENT_NAMES[row]
        current = self.font_data[name]['current']

        font, ok = QFontDialog.getFont(current, self, self._lang.get('select_font_for').format(name=name))
        if ok:
            self.font_data[name]['current'] = QFont(font)
            self._refresh_table()

    def _on_default(self):
        for n in win32_metrics.ELEMENT_NAMES:
            self.font_data[n]['current'] = QFont('Segoe UI', 9)
        self._refresh_table()

    def _on_change_all(self):
        font, ok = QFontDialog.getFont(QFont(), self, self._lang.get('select_font_all'))
        if ok:
            for n in win32_metrics.ELEMENT_NAMES:
                self.font_data[n]['current'] = QFont(font)
            self._refresh_table()

    def _on_agentos(self):
        font = QFont('AgentosUI', 10)
        for n in win32_metrics.ELEMENT_NAMES:
            self.font_data[n]['current'] = QFont(font)
        self._refresh_table()

    def _on_apply(self):
        font_map = {}
        for name in win32_metrics.ELEMENT_NAMES:
            font_map[name] = win32_metrics.qfont_to_logfont(self.font_data[name]['current'], self.dpi)

        if win32_metrics.apply_all_fonts(font_map):
            QMessageBox.information(self, self._lang.get('success'), self._lang.get('success_msg'))
        else:
            QMessageBox.warning(self, self._lang.get('error'), self._lang.get('error_msg'))
