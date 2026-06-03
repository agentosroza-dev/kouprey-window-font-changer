import ctypes
from ctypes import wintypes, windll

user32 = windll.user32
gdi32 = windll.gdi32

SPI_GETNONCLIENTMETRICS = 0x0029
SPI_SETNONCLIENTMETRICS = 0x002A
SPI_GETICONTITLELOGFONT = 0x001F
SPI_SETICONTITLELOGFONT = 0x0022
SPIF_UPDATEINIFILE = 0x0001
SPIF_SENDCHANGE = 0x0002

LOGPIXELSY = 90
DEFAULT_CHARSET = 1
CLEARTYPE_QUALITY = 5


class LOGFONTW(ctypes.Structure):
    _fields_ = [
        ('lfHeight', wintypes.LONG),
        ('lfWidth', wintypes.LONG),
        ('lfEscapement', wintypes.LONG),
        ('lfOrientation', wintypes.LONG),
        ('lfWeight', wintypes.LONG),
        ('lfItalic', wintypes.BYTE),
        ('lfUnderline', wintypes.BYTE),
        ('lfStrikeOut', wintypes.BYTE),
        ('lfCharSet', wintypes.BYTE),
        ('lfOutPrecision', wintypes.BYTE),
        ('lfClipPrecision', wintypes.BYTE),
        ('lfQuality', wintypes.BYTE),
        ('lfPitchAndFamily', wintypes.BYTE),
        ('lfFaceName', wintypes.WCHAR * 32),
    ]


class NONCLIENTMETRICSW(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.UINT),
        ('iBorderWidth', wintypes.INT),
        ('iScrollWidth', wintypes.INT),
        ('iScrollHeight', wintypes.INT),
        ('iCaptionWidth', wintypes.INT),
        ('iCaptionHeight', wintypes.INT),
        ('lfCaptionFont', LOGFONTW),
        ('iSmCaptionWidth', wintypes.INT),
        ('iSmCaptionHeight', wintypes.INT),
        ('lfSmCaptionFont', LOGFONTW),
        ('iMenuWidth', wintypes.INT),
        ('iMenuHeight', wintypes.INT),
        ('lfMenuFont', LOGFONTW),
        ('lfStatusFont', LOGFONTW),
        ('lfMessageFont', LOGFONTW),
        ('iPaddedBorderWidth', wintypes.INT),
    ]


FONT_ELEMENTS = (
    ('Font Icon', 'ICON'),
    ('Font Message boxes', 'NCM', 'lfMessageFont'),
    ('Font Tooltips', 'NCM', 'lfStatusFont'),
    ('Font Menus', 'NCM', 'lfMenuFont'),
    ('Font Title Bars', 'NCM', 'lfCaptionFont'),
    ('Font Palette Titles', 'NCM', 'lfSmCaptionFont'),
)

ELEMENT_NAMES = tuple(item[0] for item in FONT_ELEMENTS)


def get_screen_dpi():
    dc = user32.GetDC(0)
    dpi = gdi32.GetDeviceCaps(dc, LOGPIXELSY)
    user32.ReleaseDC(0, dc)
    return dpi


def _get_nonclient_metrics():
    ncm = NONCLIENTMETRICSW()
    ncm.cbSize = ctypes.sizeof(NONCLIENTMETRICSW)
    if user32.SystemParametersInfoW(SPI_GETNONCLIENTMETRICS, ncm.cbSize, ctypes.byref(ncm), 0):
        return ncm

    ncm2 = NONCLIENTMETRICSW()
    ncm2.cbSize = ctypes.sizeof(NONCLIENTMETRICSW) - 4
    if user32.SystemParametersInfoW(SPI_GETNONCLIENTMETRICS, ncm2.cbSize, ctypes.byref(ncm2), 0):
        return ncm2

    return None


def _get_icon_title_logfont():
    lf = LOGFONTW()
    if user32.SystemParametersInfoW(SPI_GETICONTITLELOGFONT, ctypes.sizeof(lf), ctypes.byref(lf), 0):
        return lf
    return None


def get_logfont(element_name: str):
    for item in FONT_ELEMENTS:
        if item[0] == element_name:
            if item[1] == 'ICON':
                return _get_icon_title_logfont()
            ncm = _get_nonclient_metrics()
            if ncm:
                return getattr(ncm, item[2])
    return None


def logfont_to_qfont(lf, dpi=None):
    from PyQt6.QtGui import QFont

    if dpi is None:
        dpi = get_screen_dpi()

    family = lf.lfFaceName or 'Segoe UI'

    if lf.lfHeight < 0:
        point_size = max(1, round(-lf.lfHeight * 72 / dpi))
    else:
        point_size = max(1, round(lf.lfHeight * 72 / dpi))

    qf = QFont(family, point_size)
    qf.setWeight(lf.lfWeight)
    qf.setItalic(bool(lf.lfItalic))
    return qf


def qfont_to_logfont(qf, dpi=None):
    if dpi is None:
        dpi = get_screen_dpi()

    lf = LOGFONTW()
    lf.lfHeight = -round(qf.pointSize() * dpi / 72)
    lf.lfWeight = qf.weight()
    lf.lfItalic = 1 if qf.italic() else 0
    lf.lfFaceName = qf.family()
    lf.lfCharSet = DEFAULT_CHARSET
    lf.lfQuality = CLEARTYPE_QUALITY
    return lf


def apply_all_fonts(font_map):
    ncm = _get_nonclient_metrics()
    if ncm is None:
        return False

    icon_lf = None

    for element_name, lf in font_map.items():
        for item in FONT_ELEMENTS:
            if item[0] == element_name:
                if item[1] == 'NCM':
                    setattr(ncm, item[2], lf)
                elif item[1] == 'ICON':
                    icon_lf = lf

    ncm.cbSize = ctypes.sizeof(NONCLIENTMETRICSW)
    ok = user32.SystemParametersInfoW(SPI_SETNONCLIENTMETRICS, ncm.cbSize, ctypes.byref(ncm), SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

    if icon_lf:
        user32.SystemParametersInfoW(SPI_SETICONTITLELOGFONT, ctypes.sizeof(LOGFONTW), ctypes.byref(icon_lf), SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

    return bool(ok)
