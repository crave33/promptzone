
from __future__ import annotations

import sys
import ctypes
from ctypes import wintypes
from pathlib import Path
import shutil

from PySide6 import QtCore, QtGui, QtWidgets
try:
    from PySide6 import QtMultimedia, QtMultimediaWidgets
except Exception:
    QtMultimedia = None
    QtMultimediaWidgets = None

try:
    import qdarktheme
except Exception:
    qdarktheme = None

from promptzone_core import PromptZoneCore, PROMPT_TEXT_EXTENSIONS

APP_TITLE = "PromptZone"
DIVIDER = "\n\n" + ("-" * 48) + "\n\n"

DEFAULT_SLOTS = [
    {"id": "slot_1", "label": "SLOT_1", "prefix": "SLOT_1_", "enabled": True, "minimized": False},
]

IMAGE_PREVIEW_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif")
VIDEO_PREVIEW_EXTENSIONS = (".webm", ".mp4", ".m4v", ".mov", ".avi", ".mkv", ".wmv", ".mpg", ".mpeg")
MEDIA_PREVIEW_EXTENSIONS = IMAGE_PREVIEW_EXTENSIONS + VIDEO_PREVIEW_EXTENSIONS

DEFAULT_THEME_COLORS = {
    "topbar": "#0f172a",
    "panel": "#0b1220",
    "panel_2": "#0f1624",
    "border": "#1e2a44",
    "text": "#e7eefc",
    "muted": "#9fb0d0",
    "accent": "#3b82f6",
    "accent_2": "#22c55e",
    "danger": "#ef4444",
    "warn": "#f59e0b",
    "button": "#0f1b33",
    "button_hover": "#15264a",
    "checkbox_on": "#22c55e",
    "list_bg": "#0f1624",
    "list_select": "#1f2f4d",
}

THEME_PRESETS = {
    "Glass": {
        "topbar": "#0d1324",
        "panel": "#0f1629",
        "panel_2": "#141e36",
        "border": "#2b3a5c",
        "text": "#e8f3ff",
        "muted": "#a7b5d6",
        "accent": "#7bd7ff",
        "accent_2": "#7cf2c1",
        "danger": "#ff6b8a",
        "warn": "#ffd08a",
        "button": "#18233f",
        "button_hover": "#1f2b4a",
        "checkbox_on": "#7cf2c1",
        "list_bg": "#141e36",
        "list_select": "#1e2a4a",
    },
    "Pastel": {
        "topbar": "#f3dce8",
        "panel": "#f8f5f8",
        "panel_2": "#f1eaf4",
        "border": "#d9c9da",
        "text": "#2a2a2f",
        "muted": "#6b5f73",
        "accent": "#8fb3ff",
        "accent_2": "#8fe3b0",
        "danger": "#ff8bb3",
        "warn": "#ffc48b",
        "button": "#ece3ef",
        "button_hover": "#e3d9e7",
        "checkbox_on": "#8fe3b0",
        "list_bg": "#f1eaf4",
        "list_select": "#e3d9e7",
    },
    "Pastel Sage": {
        "topbar": "#aebbaa",
        "panel": "#cdd6cc",
        "panel_2": "#c2cec2",
        "border": "#a4b4a0",
        "text": "#1e2320",
        "muted": "#5b655e",
        "accent": "#7fb6a2",
        "accent_2": "#6cc9b8",
        "danger": "#ff7f9b",
        "warn": "#ffb06b",
        "button": "#bcc7bb",
        "button_hover": "#b1bdb0",
        "checkbox_on": "#6cc9b8",
        "list_bg": "#c2cec2",
        "list_select": "#b1bdb0",
    },
    "Pastel Storm": {
        "topbar": "#a8b1c6",
        "panel": "#c8cfdd",
        "panel_2": "#bcc6d8",
        "border": "#9fa9bf",
        "text": "#1d2127",
        "muted": "#58606f",
        "accent": "#8aa1ff",
        "accent_2": "#7fcbb8",
        "danger": "#ff7f9c",
        "warn": "#ffb16c",
        "button": "#b6bfd1",
        "button_hover": "#acb6ca",
        "checkbox_on": "#7fcbb8",
        "list_bg": "#bcc6d8",
        "list_select": "#acb6ca",
    },
    "Cyberpunk 2077": {
        "topbar": "#0a0f1f",
        "panel": "#0a0d1a",
        "panel_2": "#121933",
        "border": "#24345c",
        "text": "#e8f4ff",
        "muted": "#95a6c9",
        "accent": "#00f5ff",
        "accent_2": "#ffe600",
        "danger": "#ff2a6d",
        "warn": "#ffb300",
        "button": "#151d3d",
        "button_hover": "#1d2752",
        "checkbox_on": "#ffe600",
        "list_bg": "#121933",
        "list_select": "#1c2854",
    },
    "Brutalist": {
        "topbar": "#0b0b0b",
        "panel": "#0f0f0f",
        "panel_2": "#0b0b0b",
        "border": "#ffffff",
        "text": "#ffffff",
        "muted": "#d0d0d0",
        "accent": "#ff2e2e",
        "accent_2": "#ffd500",
        "danger": "#ff2e2e",
        "warn": "#ffd500",
        "button": "#0f0f0f",
        "button_hover": "#1b1b1b",
        "checkbox_on": "#ffd500",
        "list_bg": "#0b0b0b",
        "list_select": "#1f1f1f",
    },
    "Dracula": {
        "topbar": "#1f202a",
        "panel": "#1b1c25",
        "panel_2": "#232636",
        "border": "#44475a",
        "text": "#f8f8f2",
        "muted": "#b5b5c0",
        "accent": "#bd93f9",
        "accent_2": "#50fa7b",
        "danger": "#ff5555",
        "warn": "#f1fa8c",
        "button": "#282a36",
        "button_hover": "#323449",
        "checkbox_on": "#50fa7b",
        "list_bg": "#232636",
        "list_select": "#2b2e3e",
    },
    "VS Code Dark Modern": {
        "topbar": "#181818",
        "panel": "#1F1F1F",
        "panel_2": "#181818",
        "border": "#2B2B2B",
        "text": "#CCCCCC",
        "muted": "#9D9D9D",
        "accent": "#0078D4",
        "accent_2": "#2EA043",
        "danger": "#F85149",
        "warn": "#9E6A03",
        "button": "#0078D4",
        "button_hover": "#026EC1",
        "checkbox_on": "#2EA043",
        "list_bg": "#1F1F1F",
        "list_select": "#0078D4",
    },
    "WhatsApp": {
        "topbar": "#075E54",
        "panel": "#ECE5DD",
        "panel_2": "#DCF8C6",
        "border": "#128C7E",
        "text": "#1E1E1E",
        "muted": "#128C7E",
        "accent": "#25D366",
        "accent_2": "#34B7F1",
        "danger": "#128C7E",
        "warn": "#34B7F1",
        "button": "#128C7E",
        "button_hover": "#075E54",
        "checkbox_on": "#34B7F1",
        "list_bg": "#ECE5DD",
        "list_select": "#DCF8C6",
    },
    "Spotify": {
        "topbar": "#191414",
        "panel": "#121212",
        "panel_2": "#191414",
        "border": "#2A2A2A",
        "text": "#FFFFFF",
        "muted": "#B3B3B3",
        "accent": "#1DB954",
        "accent_2": "#1DB954",
        "danger": "#1DB954",
        "warn": "#1DB954",
        "button": "#1DB954",
        "button_hover": "#169C46",
        "checkbox_on": "#1DB954",
        "list_bg": "#121212",
        "list_select": "#2A2A2A",
    },
    "Steam": {
        "topbar": "#171A21",
        "panel": "#1B2838",
        "panel_2": "#16202D",
        "border": "#2A475E",
        "text": "#C7D5E0",
        "muted": "#8F98A0",
        "accent": "#66C0F4",
        "accent_2": "#5C7E10",
        "danger": "#C23C2A",
        "warn": "#E3B050",
        "button": "#2A475E",
        "button_hover": "#3B5B7A",
        "checkbox_on": "#5C7E10",
        "list_bg": "#16202D",
        "list_select": "#2A475E",
    },
    "Dark": {
        "topbar": "#302E31",
        "panel": "#232225",
        "panel_2": "#302E31",
        "border": "#3A383C",
        "text": "#C4C2C4",
        "muted": "#9A989B",
        "accent": "#C4C2C4",
        "accent_2": "#9A989B",
        "danger": "#C4C2C4",
        "warn": "#C4C2C4",
        "button": "#3A383C",
        "button_hover": "#444146",
        "checkbox_on": "#9A989B",
        "list_bg": "#2B2A2D",
        "list_select": "#3A383C",
    },
    "Photoshop": {
        "topbar": "#001E36",
        "panel": "#0B2239",
        "panel_2": "#0F2A44",
        "border": "#12314F",
        "text": "#DCEBFF",
        "muted": "#8FB3D9",
        "accent": "#31A8FF",
        "accent_2": "#31A8FF",
        "danger": "#31A8FF",
        "warn": "#31A8FF",
        "button": "#12314F",
        "button_hover": "#184062",
        "checkbox_on": "#31A8FF",
        "list_bg": "#0F2A44",
        "list_select": "#12314F",
    },
}

ICON_FILES = {
    "generate": "autorenew",
    "copy": "content_copy",
    "save": "save",
    "create": "create_new_folder",
    "assign_tag": "note_add",
    "manage_slots": "dashboard_2_edit",
    "reload": "refresh",
    "customise": "tune",
    "browse": "folder_open",
    "clear": "delete_sweep",
    "reset": "history",
    "exclude_tag": "delete_sweep",
    "new_category": "create_new_folder",
    "new_prompt": "note_add",
}

BRAND_ICON_PATH = Path("assets") / "branding" / "promptzone_logo.png"
BRAND_ICON_ICO = Path("assets") / "branding" / "promptzone_logo.ico"
FONT_DIR = Path("assets") / "fonts" / "TitilliumWeb"
ROBOTO_DIR = Path("assets") / "fonts" / "Roboto"


class AutoResizeText(QtWidgets.QTextEdit):
    def __init__(self, min_lines=3, max_lines=24, max_chars=1000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._min_lines = min_lines
        self._max_lines = max_lines
        self._max_chars = max_chars
        self._measure_doc = QtGui.QTextDocument(self)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.setAcceptRichText(False)
        self.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.FixedColumnWidth)
        self.setLineWrapColumnOrWidth(165)
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.document().contentsChanged.connect(self._recalc_height)
        QtCore.QTimer.singleShot(0, self._recalc_height)

    def _recalc_height(self):
        text_len = len(self.toPlainText())
        if text_len > self._max_chars:
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        else:
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        h = self._calc_height()
        self.setFixedHeight(h)
        self.updateGeometry()

    def _calc_height(self):
        fm = self.fontMetrics()
        line_height = fm.lineSpacing()
        min_h = int(self._min_lines * line_height + 16)
        width = self._wrap_text_width(fm)
        doc = self._measure_doc
        doc.setDefaultFont(self.font())
        doc.setTextWidth(width)
        doc.setPlainText(self.toPlainText())
        doc_h = doc.size().height()
        h = int(doc_h + 16)
        max_h = self._calc_max_height()
        return max(min_h, min(max_h, h))

    def _calc_max_height(self):
        line_height = self.fontMetrics().lineSpacing()
        return int(self._max_lines * line_height + 16)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._recalc_height()

    def _wrap_text_width(self, fm: QtGui.QFontMetrics) -> int:
        if self.lineWrapMode() == QtWidgets.QTextEdit.LineWrapMode.FixedColumnWidth:
            cols = max(1, int(self.lineWrapColumnOrWidth()))
            return max(1, fm.horizontalAdvance("M") * cols)
        return max(1, self.viewport().width())


class LimitText(QtWidgets.QPlainTextEdit):
    pass


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _resolve_core_from_widget(widget: QtWidgets.QWidget):
    def _core_of(obj):
        if obj is None:
            return None
        core = getattr(obj, "core", None)
        if core is not None:
            return core
        app = getattr(obj, "app", None)
        return getattr(app, "core", None) if app is not None else None

    core = _core_of(widget)
    if core is not None:
        return core
    parent = widget.parent()
    while parent is not None:
        core = _core_of(parent)
        if core is not None:
            return core
        parent = parent.parent()
    return None


def _restore_popup_geometry(widget: QtWidgets.QWidget, key: str, fallback_size: QtCore.QSize | None = None):
    restored = False
    core = _resolve_core_from_widget(widget)
    if core is not None and isinstance(getattr(core, "settings", None), dict):
        pop = core.settings.get("popup_geometry", {})
        if isinstance(pop, dict):
            enc = pop.get(key)
            if isinstance(enc, str) and enc.strip():
                try:
                    data = QtCore.QByteArray.fromBase64(enc.encode("ascii"))
                    if not data.isEmpty():
                        restored = bool(widget.restoreGeometry(data))
                except Exception:
                    restored = False
    if not restored and fallback_size is not None:
        try:
            widget.resize(fallback_size)
        except Exception:
            pass
    try:
        widget.setMinimumSize(0, 0)
    except Exception:
        pass


def _save_popup_geometry(widget: QtWidgets.QWidget, key: str):
    core = _resolve_core_from_widget(widget)
    if core is None or not isinstance(getattr(core, "settings", None), dict):
        return
    pop = core.settings.get("popup_geometry", {})
    if not isinstance(pop, dict):
        pop = {}
    try:
        pop[key] = bytes(widget.saveGeometry().toBase64()).decode("ascii")
    except Exception:
        return
    core.settings["popup_geometry"] = pop
    core.save_settings()


def _restore_popup_splitter(splitter: QtWidgets.QSplitter, key: str, fallback_sizes: list[int] | None = None):
    restored = False
    core = _resolve_core_from_widget(splitter)
    if core is not None and isinstance(getattr(core, "settings", None), dict):
        pop = core.settings.get("popup_splitters", {})
        if isinstance(pop, dict):
            enc = pop.get(key)
            if isinstance(enc, str) and enc.strip():
                try:
                    data = QtCore.QByteArray.fromBase64(enc.encode("ascii"))
                    if not data.isEmpty():
                        restored = bool(splitter.restoreState(data))
                except Exception:
                    restored = False
    if not restored and fallback_sizes:
        try:
            splitter.setSizes([max(0, int(v)) for v in fallback_sizes])
        except Exception:
            pass


def _save_popup_splitter(splitter: QtWidgets.QSplitter, key: str):
    core = _resolve_core_from_widget(splitter)
    if core is None or not isinstance(getattr(core, "settings", None), dict):
        return
    pop = core.settings.get("popup_splitters", {})
    if not isinstance(pop, dict):
        pop = {}
    try:
        pop[key] = bytes(splitter.saveState().toBase64()).decode("ascii")
    except Exception:
        return
    core.settings["popup_splitters"] = pop
    core.save_settings()


def _enable_media_player_loop(player):
    if QtMultimedia is None or player is None:
        return
    # Prefer native loop support when available.
    try:
        if hasattr(player, "setLoops"):
            infinite = getattr(QtMultimedia.QMediaPlayer, "Infinite", -1)
            player.setLoops(int(infinite))
            return
    except Exception:
        pass
    # Fallback for older backends: restart on EndOfMedia.
    if getattr(player, "_pz_loop_hooked", False):
        return
    try:
        end_of_media = getattr(QtMultimedia.QMediaPlayer, "EndOfMedia", None)

        def _restart(status):
            if end_of_media is not None and status != end_of_media:
                return
            try:
                player.setPosition(0)
                player.play()
            except Exception:
                pass

        player.mediaStatusChanged.connect(_restart)
        player._pz_loop_cb = _restart
        player._pz_loop_hooked = True
    except Exception:
        pass


class BrowseDialog(QtWidgets.QDialog):
    MEDIA_EXT_PRIORITY = MEDIA_PREVIEW_EXTENSIONS

    def __init__(self, parent, core: PromptZoneCore, kind: str, prefix: str | None = None):
        super().__init__(parent)
        self.core = core
        self.kind = kind
        self.prefix = (prefix or "").strip() or None
        self.entries: list[tuple[str, Path, str]] = []
        self.selected_text = ""
        self._media_movie: QtGui.QMovie | None = None
        self._media_pixmap_source: QtGui.QPixmap | None = None
        self._media_player = None
        self._media_audio = None

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        if parent:
            self.setStyleSheet(parent.styleSheet())
        self.setAutoFillBackground(True)
        self.setWindowTitle(f"Browse {kind}")
        if parent and hasattr(parent, "_apply_titlebar_to"):
            parent._apply_titlebar_to(self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        top = QtWidgets.QHBoxLayout()
        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Search filename + content...")
        self.btn_inject = QtWidgets.QPushButton("Inject")
        self.btn_inject_lock = QtWidgets.QPushButton("Inject + Lock")
        top.addWidget(self.search, 1)
        top.addWidget(self.btn_inject)
        top.addWidget(self.btn_inject_lock)
        layout.addLayout(top)

        self.main_split = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.main_split.setChildrenCollapsible(False)
        self.main_split.setHandleWidth(6)
        self.list = QtWidgets.QListWidget()

        right = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)

        self.media_frame = QtWidgets.QFrame()
        self.media_frame.setObjectName("slot")
        self.media_frame.setMinimumHeight(180)
        media_layout = QtWidgets.QVBoxLayout(self.media_frame)
        media_layout.setContentsMargins(6, 6, 6, 6)
        media_layout.setSpacing(0)
        self.media_label = QtWidgets.QLabel("No media preview")
        self.media_label.setAlignment(QtCore.Qt.AlignCenter)
        self.media_label.setWordWrap(True)
        self.media_label.setObjectName("muted")
        self.media_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        media_layout.addWidget(self.media_label, 1)

        self.video_widget = None
        if QtMultimediaWidgets is not None:
            try:
                self.video_widget = QtMultimediaWidgets.QVideoWidget(self.media_frame)
                self.video_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                try:
                    self.video_widget.setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
                except Exception:
                    pass
                self.video_widget.setVisible(False)
                media_layout.addWidget(self.video_widget, 1)
            except Exception:
                self.video_widget = None

        self.preview = QtWidgets.QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setObjectName("slot")

        self.preview_split = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.preview_split.setChildrenCollapsible(False)
        self.preview_split.setHandleWidth(6)
        self.preview_split.addWidget(self.media_frame)
        self.preview_split.addWidget(self.preview)
        self.preview_split.setStretchFactor(0, 1)
        self.preview_split.setStretchFactor(1, 1)
        right_layout.addWidget(self.preview_split, 1)

        self.main_split.addWidget(self.list)
        self.main_split.addWidget(right)
        self.main_split.setStretchFactor(0, 1)
        self.main_split.setStretchFactor(1, 2)
        layout.addWidget(self.main_split, 1)
        self.main_split.splitterMoved.connect(lambda *_: QtCore.QTimer.singleShot(0, self._update_media_scaling))
        self.preview_split.splitterMoved.connect(lambda *_: QtCore.QTimer.singleShot(0, self._update_media_scaling))
        self.media_frame.installEventFilter(self)
        self.media_label.installEventFilter(self)

        self.search.textChanged.connect(self.refresh)
        self.list.currentRowChanged.connect(self._on_select)
        self.list.itemDoubleClicked.connect(lambda _: self._inject(False))
        self.btn_inject.clicked.connect(lambda: self._inject(False))
        self.btn_inject_lock.clicked.connect(lambda: self._inject(True))

        self.refresh()
        self._finalize_size()
        self.finished.connect(lambda _: self._save_dialog_state())

    def _finalize_size(self):
        self.adjustSize()
        fallback = QtCore.QSize(640, 420)
        parent = self.parent()
        if parent is not None:
            try:
                psize = parent.size()
                fallback = QtCore.QSize(max(480, psize.width() // 2), max(360, psize.height() // 2))
            except Exception:
                pass
        _restore_popup_geometry(self, "browse_dialog", fallback)
        QtCore.QTimer.singleShot(0, self._restore_splitters)

    def _restore_splitters(self):
        total_w = max(520, self.width())
        total_h = max(360, self.height())
        _restore_popup_splitter(
            self.main_split,
            "browse_dialog_main_splitter",
            [max(220, total_w // 3), max(280, total_w - (total_w // 3))],
        )
        _restore_popup_splitter(
            self.preview_split,
            "browse_dialog_preview_splitter",
            [max(140, total_h // 3), max(200, total_h - (total_h // 3))],
        )

    def _save_dialog_state(self):
        _save_popup_splitter(self.main_split, "browse_dialog_main_splitter")
        _save_popup_splitter(self.preview_split, "browse_dialog_preview_splitter")
        _save_popup_geometry(self, "browse_dialog")

    def refresh(self):
        q = self.search.text()
        self.entries = self.core.browse_entries(self.kind, q, prefix=self.prefix)
        self.list.clear()
        for label, _, text in self.entries:
            first = (text.strip().splitlines()[0] if text.strip() else "").strip()
            self.list.addItem(f"{label} - {first[:120]}")
        if self.entries:
            self.list.setCurrentRow(0)
        else:
            self._clear_media_preview()
            self.preview.clear()

    def _find_media_preview(self, prompt_path: Path) -> Path | None:
        stem = prompt_path.stem
        folder = prompt_path.parent
        for ext in self.MEDIA_EXT_PRIORITY:
            cand = folder / f"{stem}{ext}"
            if cand.exists() and cand.is_file():
                return cand
        return None

    def _clear_media_preview(self):
        self._media_pixmap_source = None
        if self._media_movie is not None:
            try:
                self._media_movie.stop()
            except Exception:
                pass
            self.media_label.setMovie(None)
            self._media_movie = None
        if self._media_player is not None:
            try:
                self._media_player.stop()
            except Exception:
                pass
        if self.video_widget is not None:
            self.video_widget.setVisible(False)
        self.media_label.setPixmap(QtGui.QPixmap())
        self.media_label.setText("No media preview")
        self.media_label.setVisible(True)

    @staticmethod
    def _fit_aspect_size(src: QtCore.QSize, dst: QtCore.QSize) -> QtCore.QSize:
        if src.width() <= 0 or src.height() <= 0:
            return dst
        return src.scaled(dst, QtCore.Qt.KeepAspectRatio)

    def _media_target_size(self) -> QtCore.QSize:
        margins = self.media_frame.contentsMargins()
        size = self.media_frame.size() - QtCore.QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        if size.width() < 20 or size.height() < 20:
            size = QtCore.QSize(320, 180)
        return size

    def _update_media_scaling(self):
        target = self._media_target_size()
        if self._media_movie is not None:
            src = self._media_movie.currentPixmap().size()
            if src.width() <= 0 or src.height() <= 0:
                src = self._media_movie.frameRect().size()
            if src.width() > 0 and src.height() > 0:
                self._media_movie.setScaledSize(self._fit_aspect_size(src, target))
            return
        if self._media_pixmap_source is not None and not self._media_pixmap_source.isNull():
            scaled = self._media_pixmap_source.scaled(
                target, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            self.media_label.setPixmap(scaled)

    def _show_media_preview(self, prompt_path: Path):
        self._clear_media_preview()
        media_path = self._find_media_preview(prompt_path)
        if media_path is None:
            return

        suffix = media_path.suffix.lower()
        if suffix == ".gif":
            movie = QtGui.QMovie(str(media_path))
            if movie.isValid():
                self._media_movie = movie
                self.media_label.setText("")
                self.media_label.setMovie(movie)
                self.media_label.setVisible(True)
                self._update_media_scaling()
                movie.start()
                QtCore.QTimer.singleShot(0, self._update_media_scaling)
                return

        if suffix in VIDEO_PREVIEW_EXTENSIONS:
            if QtMultimedia is None or self.video_widget is None:
                self.media_label.setText(f"Preview available: {media_path.name}")
                return
            try:
                if self._media_player is None:
                    self._media_player = QtMultimedia.QMediaPlayer(self)
                    self._media_audio = QtMultimedia.QAudioOutput(self)
                    self._media_audio.setMuted(True)
                    self._media_player.setAudioOutput(self._media_audio)
                    self._media_player.setVideoOutput(self.video_widget)
                    _enable_media_player_loop(self._media_player)
                self.media_label.setVisible(False)
                self.video_widget.setVisible(True)
                self._media_player.setSource(QtCore.QUrl.fromLocalFile(str(media_path)))
                self._media_player.play()
                QtCore.QTimer.singleShot(0, self._update_media_scaling)
                return
            except Exception:
                self.media_label.setVisible(True)
                self.media_label.setText(f"Preview available: {media_path.name}")
                return

        pix = QtGui.QPixmap(str(media_path))
        if pix.isNull():
            self.media_label.setText(f"Preview available: {media_path.name}")
            return
        self._media_pixmap_source = pix
        self.media_label.setText("")
        self._update_media_scaling()
        QtCore.QTimer.singleShot(0, self._update_media_scaling)

    def showEvent(self, event):
        super().showEvent(event)
        QtCore.QTimer.singleShot(0, self._update_media_scaling)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_media_scaling()

    def eventFilter(self, obj, event):
        if obj in (self.media_frame, self.media_label) and event.type() in (
            QtCore.QEvent.Resize,
            QtCore.QEvent.Show,
            QtCore.QEvent.LayoutRequest,
        ):
            QtCore.QTimer.singleShot(0, self._update_media_scaling)
        return super().eventFilter(obj, event)

    def _on_select(self, idx: int):
        if idx < 0 or idx >= len(self.entries):
            self._clear_media_preview()
            self.preview.clear()
            return
        _, prompt_path, text = self.entries[idx]
        self._show_media_preview(prompt_path)
        self.preview.setPlainText(text.strip())

    def _inject(self, lock: bool):
        idx = self.list.currentRow()
        if idx < 0 or idx >= len(self.entries):
            return
        _, _, text = self.entries[idx]
        self.selected_text = text.strip()
        self.done(2 if lock else 1)


class ThemeDialog(QtWidgets.QDialog):
    def __init__(self, parent, colors: dict, on_apply, current_preset: str | None = None):
        super().__init__(parent)
        self.colors = dict(colors)
        self.on_apply = on_apply
        self.rows: dict[str, QtWidgets.QLineEdit] = {}
        self.swatches: dict[str, QtWidgets.QFrame] = {}

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        self.setAutoFillBackground(True)
        self.setWindowTitle("Customise Theme")
        if parent and hasattr(parent, "_apply_titlebar_to"):
            parent._apply_titlebar_to(self)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        top = QtWidgets.QHBoxLayout()
        self.preset = QtWidgets.QComboBox()
        self.preset.addItems(list(THEME_PRESETS.keys()))
        if current_preset:
            self.preset.setCurrentText(current_preset)
        self.btn_apply_preset = QtWidgets.QPushButton("Apply preset")
        self.btn_reset = QtWidgets.QPushButton("Reset to default")
        self.btn_save_as = QtWidgets.QPushButton("Save to new")
        self.btn_save = QtWidgets.QPushButton("Save")
        top.addWidget(self.preset)
        top.addWidget(self.btn_apply_preset)
        top.addWidget(self.btn_reset)
        top.addWidget(self.btn_save_as)
        top.addStretch(1)
        top.addWidget(self.btn_save)
        root.addLayout(top)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        body = QtWidgets.QWidget()
        body.setObjectName("card")
        form = QtWidgets.QGridLayout(body)
        form.setContentsMargins(8, 8, 8, 8)
        form.setHorizontalSpacing(8)
        form.setVerticalSpacing(6)
        scroll.setWidget(body)
        root.addWidget(scroll, 1)

        for r, key in enumerate(self.colors.keys()):
            form.addWidget(QtWidgets.QLabel(key), r, 0)
            edit = QtWidgets.QLineEdit(self.colors[key])
            self.rows[key] = edit
            form.addWidget(edit, r, 1)
            swatch = QtWidgets.QFrame()
            swatch.setFixedSize(32, 20)
            swatch.setStyleSheet(f"background: {self.colors[key]}; border: 1px solid #333;")
            self.swatches[key] = swatch
            form.addWidget(swatch, r, 2)
            btn = QtWidgets.QPushButton("Pick")
            btn.clicked.connect(lambda _, k=key: self._pick_color(k))
            form.addWidget(btn, r, 3)

        self.btn_apply_preset.clicked.connect(self._apply_preset)
        self.btn_reset.clicked.connect(self._reset_defaults)
        self.btn_save_as.clicked.connect(self._save_as_new)
        self.btn_save.clicked.connect(self._save)
        self._apply_theme()
        self._finalize_size()
        self.finished.connect(lambda _: _save_popup_geometry(self, "theme_dialog"))

    def _apply_theme(self):
        if qdarktheme is not None and getattr(self.parent(), "use_qdarktheme", False):
            return
        c = self.colors
        self.setStyleSheet(
            f"""
            QDialog {{ background: {c['panel_2']}; }}
            QWidget {{ color: {c['text']}; font-family: 'Roboto'; font-size: 12pt; }}
            QLabel {{ color: {c['text']}; }}
            QLineEdit {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 6px; }}
            QComboBox {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 6px; padding-left: 6px; }}
            QComboBox QAbstractItemView {{ background: {c['panel']}; color: {c['text']}; selection-background-color: {c['list_select']}; }}
            QPushButton {{ background: {c['button']}; border-radius: 8px; padding: 6px 12px; }}
            QPushButton:hover {{ background: {c['button_hover']}; }}
            QScrollArea {{ border: none; }}
            QScrollArea QWidget {{ background: {c['panel_2']}; }}
            """
        )

    def _finalize_size(self):
        self.adjustSize()
        hint = self.sizeHint()
        fallback = hint if hint.isValid() else QtCore.QSize(820, 620)
        _restore_popup_geometry(self, "theme_dialog", fallback)

    def _pick_color(self, key: str):
        col = QtWidgets.QColorDialog.getColor(QtGui.QColor(self.rows[key].text()), self, f"Pick {key}")
        if not col.isValid():
            return
        self.rows[key].setText(col.name())
        self.swatches[key].setStyleSheet(f"background: {col.name()}; border: 1px solid #333;")

    def _apply_preset(self):
        preset = THEME_PRESETS.get(self.preset.currentText())
        if not preset:
            return
        for k, v in preset.items():
            if k in self.rows:
                self.rows[k].setText(v)
                self.swatches[k].setStyleSheet(f"background: {v}; border: 1px solid #333;")
        self.colors.update(preset)
        self._apply_theme()
        if hasattr(self.parent(), "core"):
            self.parent().core.settings["theme_preset"] = self.preset.currentText()
            self.parent().core.save_settings()
        try:
            self.on_apply(dict(self.colors))
        except Exception:
            pass

    def _reset_defaults(self):
        for k, v in DEFAULT_THEME_COLORS.items():
            if k in self.rows:
                self.rows[k].setText(v)
                self.swatches[k].setStyleSheet(f"background: {v}; border: 1px solid #333;")
        self.colors = dict(DEFAULT_THEME_COLORS)
        self._apply_theme()

    def _save(self):
        colors = {k: self.rows[k].text().strip() for k in self.rows}
        preset_name = None
        for name, preset in THEME_PRESETS.items():
            if all(colors.get(k) == v for k, v in preset.items()):
                preset_name = name
                break
        self.on_apply(colors)
        if hasattr(self.parent(), "core"):
            self.parent().core.settings["theme_preset"] = preset_name or "Custom"
            self.parent().core.save_settings()
        self.accept()

    def _save_as_new(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Save theme", "Theme name:")
        if not ok:
            return
        name = (name or "").strip()
        if not name:
            return

        parent = self.parent()
        if parent is None or not hasattr(parent, "core"):
            return

        if name in THEME_PRESETS:
            res = QtWidgets.QMessageBox.question(
                self,
                "Overwrite preset?",
                f"A preset named \"{name}\" already exists. Overwrite it?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )
            if res != QtWidgets.QMessageBox.Yes:
                return

        colors = {k: self.rows[k].text().strip() for k in self.rows}
        THEME_PRESETS[name] = dict(colors)
        custom = parent.core.settings.get("custom_presets", {})
        if not isinstance(custom, dict):
            custom = {}
        custom[name] = dict(colors)
        parent.core.settings["custom_presets"] = custom
        parent.core.settings["theme_preset"] = name
        parent.core.save_settings()

        if self.preset.findText(name) < 0:
            self.preset.addItem(name)
        self.preset.setCurrentText(name)
        if hasattr(parent, "preset_combo"):
            if parent.preset_combo.findText(name) < 0:
                parent.preset_combo.addItem(name)
            parent.preset_combo.setCurrentText(name)


class SlotsTable(QtWidgets.QTableWidget):
    orderChanged = QtCore.Signal()
    pass


class ManageSlotsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.setWindowTitle("Manage Slots")
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        if parent:
            self.setStyleSheet(parent.styleSheet())
        self.setAutoFillBackground(True)
        if parent and hasattr(parent, "_apply_titlebar_to"):
            parent._apply_titlebar_to(self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        hint_row = QtWidgets.QHBoxLayout()
        hint_icon = QtWidgets.QLabel()
        hint_icon.setPixmap(self.style().standardIcon(QtWidgets.QStyle.SP_ArrowUp).pixmap(12, 12))
        hint_text = QtWidgets.QLabel("Use Up/Down to reorder.")
        hint_text.setObjectName("muted")
        hint_row.addWidget(hint_icon, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        hint_row.addWidget(hint_text, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        hint_row.addStretch(1)
        layout.addLayout(hint_row)

        self.table = SlotsTable(0, 6, self)
        self.table.setHorizontalHeaderLabels(["#", "Name", "Prefix", "Auto", "Enabled", "Minimized"])
        header_tips = [
            "Current row order.",
            "Slot display name.",
            "Prefix used to match folders (e.g. ACTIONSTYLE_).",
            "When checked, prefix updates automatically when you rename the slot.",
            "Whether this slot is active.",
            "Hide this slot in the UI.",
        ]
        for idx, tip in enumerate(header_tips):
            item = self.table.horizontalHeaderItem(idx)
            if item is not None:
                item.setToolTip(tip)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setDragEnabled(False)
        self.table.setAcceptDrops(False)
        self.table.setDropIndicatorShown(False)
        self.table.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.table.setSortingEnabled(False)
        self._apply_table_theme()
        layout.addWidget(self.table, 1)

        btns = QtWidgets.QHBoxLayout()
        self.btn_up = QtWidgets.QPushButton("Up")
        self.btn_down = QtWidgets.QPushButton("Down")
        self.btn_add = QtWidgets.QPushButton("Add Slot")
        self.btn_remove = QtWidgets.QPushButton("Remove Slot")
        self.btn_close = QtWidgets.QPushButton("Close")
        btns.addWidget(self.btn_up)
        btns.addWidget(self.btn_down)
        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_remove)
        btns.addStretch(1)
        btns.addWidget(self.btn_close)
        layout.addLayout(btns)

        self.btn_up.clicked.connect(lambda: self._move_selected_row(-1))
        self.btn_down.clicked.connect(lambda: self._move_selected_row(1))
        self.btn_add.clicked.connect(self._add_row)
        self.btn_remove.clicked.connect(self._remove_row)
        self.btn_close.clicked.connect(self._close_and_save)
        self.table.itemChanged.connect(self._on_item_changed)

        self._load()
        _restore_popup_geometry(self, "manage_slots_dialog", QtCore.QSize(720, 420))
        self.finished.connect(lambda _: _save_popup_geometry(self, "manage_slots_dialog"))

    def _apply_table_theme(self):
        c = getattr(self.app, "colors", DEFAULT_THEME_COLORS)
        self.table.setStyleSheet(
            f"""
            QTableWidget {{
                background: {c['panel']};
                color: {c['text']};
                border: 1px solid {c['border']};
                border-radius: 6px;
                gridline-color: {c['border']};
                selection-background-color: {c['list_select']};
                selection-color: {c['text']};
            }}
            QTableWidget::item {{
                background: {c['panel']};
                color: {c['text']};
            }}
            QTableWidget QCheckBox {{
                background: transparent;
            }}
            QHeaderView::section {{
                background: {c['panel_2']};
                color: {c['text']};
                border: 1px solid {c['border']};
                padding: 4px;
            }}
            QTableCornerButton::section {{
                background: {c['panel_2']};
                border: 1px solid {c['border']};
            }}
            """
        )

    @staticmethod
    def _slug_prefix(name: str) -> str:
        raw = "".join(ch for ch in (name or "").upper().replace(" ", "_") if ch.isalnum() or ch == "_").strip("_")
        return f"{raw}_" if raw else ""

    def _load(self):
        slots = self.app.core.settings.get("slots", DEFAULT_SLOTS)
        if not isinstance(slots, list):
            slots = DEFAULT_SLOTS
        blocker = QtCore.QSignalBlocker(self.table)
        try:
            self.table.setRowCount(0)
            for s in slots:
                self._add_row(s)
        finally:
            del blocker
        self._refresh_row_numbers()

    def _add_row(self, slot=None):
        row = self.table.rowCount()
        self.table.insertRow(row)

        name = (slot or {}).get("label", f"Slot {row + 1}")
        prefix = (slot or {}).get("prefix", self._slug_prefix(name))
        auto = (slot or {}).get("auto", True)
        enabled = (slot or {}).get("enabled", True)
        minimized = (slot or {}).get("minimized", False)
        slot_id = (slot or {}).get("id", f"slot_{row+1}")

        drag_item = QtWidgets.QTableWidgetItem(str(row + 1))
        drag_item.setTextAlignment(QtCore.Qt.AlignCenter)
        drag_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        name_item = QtWidgets.QTableWidgetItem(name)
        name_item.setData(QtCore.Qt.UserRole, slot_id)
        prefix_item = QtWidgets.QTableWidgetItem(prefix)
        auto_item = QtWidgets.QTableWidgetItem()
        enabled_item = QtWidgets.QTableWidgetItem()
        minimized_item = QtWidgets.QTableWidgetItem()
        auto_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        enabled_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        minimized_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        auto_item.setTextAlignment(QtCore.Qt.AlignCenter)
        enabled_item.setTextAlignment(QtCore.Qt.AlignCenter)
        minimized_item.setTextAlignment(QtCore.Qt.AlignCenter)

        self.table.setItem(row, 0, drag_item)
        self.table.setItem(row, 1, name_item)
        self.table.setItem(row, 2, prefix_item)
        self.table.setItem(row, 3, auto_item)
        self.table.setItem(row, 4, enabled_item)
        self.table.setItem(row, 5, minimized_item)
        self.table.setCellWidget(row, 3, self._centered_checkbox(auto))
        self.table.setCellWidget(row, 4, self._centered_checkbox(enabled))
        self.table.setCellWidget(row, 5, self._centered_checkbox(minimized))
        self._refresh_row_numbers()
        self._wire_row_checkboxes(row)

    def _close_and_save(self):
        self._save()
        self.accept()

    def _remove_row(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)
            self._refresh_row_numbers()
            self._save()

    def _move_selected_row(self, delta: int):
        row = self.table.currentRow()
        if row < 0:
            return
        target = row + delta
        if target < 0 or target >= self.table.rowCount():
            return
        self._swap_rows(row, target)
        self.table.clearSelection()
        self.table.selectRow(target)
        self._refresh_row_numbers()
        self._save()

    def _swap_rows(self, a: int, b: int):
        col_count = self.table.columnCount()
        blocker = QtCore.QSignalBlocker(self.table)
        try:
            a_items = [self.table.takeItem(a, c) for c in range(col_count)]
            b_items = [self.table.takeItem(b, c) for c in range(col_count)]
            a_widgets = [self.table.cellWidget(a, c) for c in range(col_count)]
            b_widgets = [self.table.cellWidget(b, c) for c in range(col_count)]
            for c in range(col_count):
                if a_widgets[c] is not None:
                    self.table.removeCellWidget(a, c)
                if b_widgets[c] is not None:
                    self.table.removeCellWidget(b, c)
            for c in range(col_count):
                self.table.setItem(a, c, b_items[c] if b_items[c] is not None else QtWidgets.QTableWidgetItem(""))
                self.table.setItem(b, c, a_items[c] if a_items[c] is not None else QtWidgets.QTableWidgetItem(""))
                if b_widgets[c] is not None:
                    self.table.setCellWidget(a, c, b_widgets[c])
                if a_widgets[c] is not None:
                    self.table.setCellWidget(b, c, a_widgets[c])
        finally:
            del blocker
        self._wire_row_checkboxes(a)
        self._wire_row_checkboxes(b)

    def _centered_checkbox(self, checked: bool) -> QtWidgets.QWidget:
        wrapper = QtWidgets.QWidget(self.table)
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        cb = QtWidgets.QCheckBox(wrapper)
        cb.setChecked(bool(checked))
        layout.addWidget(cb)
        return wrapper

    def _checkbox_at(self, row: int, col: int) -> QtWidgets.QCheckBox | None:
        w = self.table.cellWidget(row, col)
        if w is None:
            return None
        return w.findChild(QtWidgets.QCheckBox)

    def _checkbox_checked(self, row: int, col: int, default: bool) -> bool:
        cb = self._checkbox_at(row, col)
        return cb.isChecked() if cb is not None else default

    def _set_checkbox_checked(self, row: int, col: int, checked: bool):
        cb = self._checkbox_at(row, col)
        if cb is None:
            return
        blocker = QtCore.QSignalBlocker(cb)
        try:
            cb.setChecked(bool(checked))
        finally:
            del blocker

    def _wire_row_checkboxes(self, row: int):
        for col in (3, 4, 5):
            cb = self._checkbox_at(row, col)
            if cb is None:
                continue
            if not bool(cb.property("_save_connected")):
                cb.stateChanged.connect(self._save)
                cb.setProperty("_save_connected", True)
    def _refresh_row_numbers(self):
        blocker = QtCore.QSignalBlocker(self.table)
        try:
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 0)
                if item is None:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                    self.table.setItem(row, 0, item)
                item.setText(str(row + 1))
        finally:
            del blocker

    def _on_item_changed(self, item: QtWidgets.QTableWidgetItem):
        row = item.row()
        if item.column() == 1:  # name changed
            if self._checkbox_checked(row, 3, True):
                prefix_item = self.table.item(row, 2)
                new_prefix = self._slug_prefix(item.text())
                if prefix_item is not None:
                    prefix_item.setText(new_prefix)
        if item.column() == 2:  # prefix changed
            name_item = self.table.item(row, 1)
            if name_item:
                gen = self._slug_prefix(name_item.text())
                if item.text() != gen:
                    self._set_checkbox_checked(row, 3, False)
        self._save()

    def _save(self):
        slots = []
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 1)
            prefix_item = self.table.item(row, 2)
            label = name_item.text().strip() if name_item else f"Slot {row + 1}"
            prefix = prefix_item.text().strip() if prefix_item else self._slug_prefix(label)
            slot_id = None
            if name_item is not None:
                slot_id = name_item.data(QtCore.Qt.UserRole)
            slots.append(
                {
                    "id": str(slot_id or f"slot_{row+1}"),
                    "label": label,
                    "prefix": prefix if prefix.endswith("_") else (prefix + "_" if prefix else ""),
                    "auto": self._checkbox_checked(row, 3, True),
                    "enabled": self._checkbox_checked(row, 4, True),
                    "minimized": self._checkbox_checked(row, 5, False),
                }
            )
        self.app.core.settings["slots"] = slots
        self.app.core.save_settings()


class CreateDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.new_prompt_image: QtGui.QImage | None = None
        self.new_prompt_media_path: Path | None = None
        self.new_prompt_image_ext = ".png"
        self.new_prompt_media_ext = ".png"
        self._create_media_player = None
        self._create_media_audio = None
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        if parent:
            self.setStyleSheet(parent.styleSheet())
        self.setAutoFillBackground(True)
        self.setWindowTitle("Create")
        if parent and hasattr(parent, "_apply_titlebar_to"):
            parent._apply_titlebar_to(self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        tabs = QtWidgets.QTabWidget()
        tabs.setObjectName("card")
        layout.addWidget(tabs, 1)

        tab_cat = QtWidgets.QWidget()
        tab_cat.setObjectName("card")
        cat_layout = QtWidgets.QVBoxLayout(tab_cat)
        cat_layout.setContentsMargins(8, 8, 8, 8)
        cat_layout.setSpacing(8)
        self.new_cat_kind = QtWidgets.QComboBox()
        self.new_cat_name = QtWidgets.QLineEdit()
        btn_create_cat = QtWidgets.QPushButton("Create category")
        btn_create_cat.clicked.connect(self._create_category)
        self.lbl_cat_type = QtWidgets.QLabel("Type")
        cat_layout.addWidget(self._fixed_label_row(self.lbl_cat_type))
        cat_layout.addWidget(self.new_cat_kind)
        self.lbl_cat_name = QtWidgets.QLabel("Category name")
        cat_layout.addWidget(self._fixed_label_row(self.lbl_cat_name))
        cat_layout.addWidget(self.new_cat_name)
        cat_layout.addWidget(btn_create_cat)
        cat_layout.addStretch(1)

        tab_prompt = QtWidgets.QWidget()
        tab_prompt.setObjectName("card")
        p_layout = QtWidgets.QVBoxLayout(tab_prompt)
        p_layout.setContentsMargins(8, 8, 8, 8)
        p_layout.setSpacing(8)
        self.new_prompt_kind = QtWidgets.QComboBox()
        self.new_prompt_folder = QtWidgets.QComboBox()
        self.new_prompt_filename = QtWidgets.QLineEdit()
        self.new_prompt_filename.setPlaceholderText("Optional filename (.md/.txt)")
        self.new_prompt_text = AutoResizeText(min_lines=4, max_lines=16, max_chars=1000)
        self.new_prompt_text.setObjectName("slot")
        self.new_prompt_media_frame = QtWidgets.QFrame()
        self.new_prompt_media_frame.setObjectName("slot")
        self.new_prompt_media_frame.setMinimumHeight(140)
        self.new_prompt_media_frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        media_layout = QtWidgets.QVBoxLayout(self.new_prompt_media_frame)
        media_layout.setContentsMargins(6, 6, 6, 6)
        media_layout.setSpacing(0)
        self.new_prompt_image_preview = QtWidgets.QLabel("No media selected")
        self.new_prompt_image_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.new_prompt_image_preview.setWordWrap(True)
        self.new_prompt_image_preview.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        media_layout.addWidget(self.new_prompt_image_preview, 1)
        self.new_prompt_video_widget = None
        if QtMultimediaWidgets is not None:
            try:
                self.new_prompt_video_widget = QtMultimediaWidgets.QVideoWidget(self.new_prompt_media_frame)
                self.new_prompt_video_widget.setSizePolicy(
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
                )
                try:
                    self.new_prompt_video_widget.setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
                except Exception:
                    pass
                self.new_prompt_video_widget.setVisible(False)
                media_layout.addWidget(self.new_prompt_video_widget, 1)
            except Exception:
                self.new_prompt_video_widget = None
        self.btn_prompt_image_browse = QtWidgets.QPushButton("Browse media...")
        self.btn_prompt_image_clear = QtWidgets.QPushButton("Clear media")
        self.btn_prompt_image_browse.clicked.connect(self._browse_prompt_image)
        self.btn_prompt_image_clear.clicked.connect(self._clear_prompt_image)
        btn_save_prompt = QtWidgets.QPushButton("Save prompt (.md/.txt)")
        btn_save_prompt.clicked.connect(self._create_prompt)
        self.lbl_prompt_type = QtWidgets.QLabel("Type")
        self.lbl_prompt_category = QtWidgets.QLabel("Category")
        self.lbl_prompt_filename = QtWidgets.QLabel("Filename (optional)")
        self.lbl_prompt_text = QtWidgets.QLabel("Prompt text")
        self.lbl_prompt_image = QtWidgets.QLabel("Optional media (image/video, Ctrl+V supported)")
        p_layout.addWidget(self._fixed_label_row(self.lbl_prompt_type))
        p_layout.addWidget(self.new_prompt_kind)
        p_layout.addWidget(self._fixed_label_row(self.lbl_prompt_category))
        p_layout.addWidget(self.new_prompt_folder)
        p_layout.addWidget(self._fixed_label_row(self.lbl_prompt_filename))
        p_layout.addWidget(self.new_prompt_filename)
        p_layout.addWidget(self._fixed_label_row(self.lbl_prompt_text))
        p_layout.addWidget(self.new_prompt_text)
        p_layout.addWidget(self._fixed_label_row(self.lbl_prompt_image))
        p_layout.addWidget(self.new_prompt_media_frame)
        img_btn_row = QtWidgets.QHBoxLayout()
        img_btn_row.setContentsMargins(0, 0, 0, 0)
        img_btn_row.setSpacing(8)
        img_btn_row.addWidget(self.btn_prompt_image_browse)
        img_btn_row.addWidget(self.btn_prompt_image_clear)
        img_btn_row.addStretch(1)
        p_layout.addLayout(img_btn_row)
        p_layout.addWidget(btn_save_prompt)
        p_layout.addStretch(1)
        # QVBoxLayout uses setStretch on items; no row stretches needed here.

        tabs.addTab(tab_cat, "New Category")
        tabs.addTab(tab_prompt, "New Prompt")
        tab_tag = QtWidgets.QWidget()
        tab_tag.setObjectName("card")
        tag_layout = QtWidgets.QVBoxLayout(tab_tag)
        tag_layout.setContentsMargins(8, 8, 8, 8)
        tag_layout.setSpacing(8)
        self.lbl_tag_name = QtWidgets.QLabel("Tag name")
        self.new_tag_name = QtWidgets.QLineEdit()
        btn_create_tag = QtWidgets.QPushButton("Create tag")
        btn_create_tag.clicked.connect(self._create_tag)
        tag_layout.addWidget(self._fixed_label_row(self.lbl_tag_name))
        tag_layout.addWidget(self.new_tag_name)
        tag_layout.addWidget(btn_create_tag)
        tag_layout.addStretch(1)
        tabs.addTab(tab_tag, "New Tag")

        self._populate_kind_combos()
        self.new_prompt_kind.currentTextChanged.connect(self._refresh_prompt_folders)
        self._refresh_prompt_folders()
        self._apply_label_metrics()
        self._finalize_size()
        self.finished.connect(lambda _: _save_popup_geometry(self, "create_dialog"))
        self.finished.connect(lambda _: self._stop_prompt_video_preview())

    def _populate_kind_combos(self):
        self.new_cat_kind.clear()
        self.new_prompt_kind.clear()
        items: list[tuple[str, str]] = []
        for slot in self.app.core.get_slots():
            label = str(slot.get("label") or slot.get("id") or "").strip()
            prefix = str(slot.get("prefix") or "").strip()
            if not label or not prefix:
                continue
            items.append((label.upper(), prefix))
        if not items:
            for slot in DEFAULT_SLOTS:
                items.append((str(slot.get("label", "")).upper(), str(slot.get("prefix", ""))))
        for label, prefix in items:
            self.new_cat_kind.addItem(label, prefix)
            self.new_prompt_kind.addItem(label, prefix)

    def _finalize_size(self):
        self.adjustSize()
        hint = self.sizeHint()
        fallback = hint if hint.isValid() else QtCore.QSize(760, 620)
        _restore_popup_geometry(self, "create_dialog", fallback)

    def _apply_label_metrics(self):
        label_font = QtGui.QFont("Roboto", 12)
        for lbl in [
            getattr(self, "lbl_cat_type", None),
            getattr(self, "lbl_cat_name", None),
            getattr(self, "lbl_prompt_type", None),
            getattr(self, "lbl_prompt_category", None),
            getattr(self, "lbl_prompt_filename", None),
            getattr(self, "lbl_prompt_text", None),
            getattr(self, "lbl_prompt_image", None),
            getattr(self, "lbl_tag_name", None),
        ]:
            if lbl is None:
                continue
            lbl.setFont(label_font)
            lbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            lbl.setContentsMargins(0, 0, 0, 0)
            lbl.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            lbl.setMinimumHeight(18)
            lbl.setMaximumHeight(18)

    def _fixed_label_row(self, label: QtWidgets.QLabel) -> QtWidgets.QWidget:
        wrapper = QtWidgets.QFrame()
        wrapper.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        wrapper.setFixedHeight(16)
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)
        layout.addStretch(1)
        return wrapper

    def _fixed_input_row(self, widget: QtWidgets.QWidget, height: int) -> QtWidgets.QWidget:
        wrapper = QtWidgets.QFrame()
        wrapper.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        wrapper.setFixedHeight(height)
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        return wrapper

    def _section_divider(self) -> QtWidgets.QFrame:
        line = QtWidgets.QFrame()
        line.setObjectName("sectionDivider")
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Plain)
        line.setFixedHeight(2)
        line.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        return line

    def _refresh_prompt_folders(self):
        prefix = str(self.new_prompt_kind.currentData() or "").strip()
        vals = [p.name for p in self.app.core.folders_by_prefix(prefix)] if prefix else []
        self.new_prompt_folder.clear()
        if not vals:
            vals = ["(none)"]
        self.new_prompt_folder.addItems(vals)

    def _create_category(self):
        kind = str(self.new_cat_kind.currentData() or "").strip()
        name = self.new_cat_name.text().strip()
        if not name:
            self.app._status("Category name is empty.")
            return
        try:
            created = self.app.core.create_category(kind, name)
        except Exception as e:
            self.app._status(str(e))
            return
        self.new_cat_name.setText("")
        self.app._refresh_library_ui()
        self.app._status(f"Created category: {created}")

    def _create_prompt(self):
        kind = str(self.new_prompt_kind.currentData() or "").strip()
        folder = self.new_prompt_folder.currentText()
        text = self.new_prompt_text.toPlainText().strip()
        filename = self.new_prompt_filename.text().strip()
        if folder == "(none)":
            self.app._status("No category available.")
            return
        if not text:
            self.app._status("Prompt text is empty.")
            return
        overwrite = False
        if filename:
            if "/" in filename or "\\" in filename:
                self.app._status("Filename must not include folders.")
                return
            if not filename.lower().endswith(PROMPT_TEXT_EXTENSIONS):
                filename = filename + ".md"
            path = self.app.core.library_dir / folder / filename
            if path.exists():
                res = QtWidgets.QMessageBox.question(
                    self,
                    "Overwrite file?",
                    f"\"{filename}\" already exists. Overwrite it?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.No,
                )
                if res != QtWidgets.QMessageBox.Yes:
                    return
                overwrite = True
        try:
            path = self.app.core.create_prompt_file(kind, folder, text, filename or None, overwrite)
        except Exception as e:
            self.app._status(str(e))
            return
        media_msg = ""
        if self.new_prompt_image is not None:
            ext = (self.new_prompt_image_ext or ".png").lower()
            if ext == ".jpeg":
                ext = ".jpg"
            if ext not in IMAGE_PREVIEW_EXTENSIONS:
                ext = ".png"
            media_path = path.with_suffix(ext)
            media_ok = self.new_prompt_image.save(str(media_path))
            if media_ok:
                media_msg = f" + media {media_path.name}"
            else:
                self.app._status("Prompt saved, but media save failed.")
        elif self.new_prompt_media_path is not None and self.new_prompt_media_path.exists():
            ext = (self.new_prompt_media_ext or self.new_prompt_media_path.suffix.lower() or ".png").lower()
            if ext == ".jpeg":
                ext = ".jpg"
            if ext not in MEDIA_PREVIEW_EXTENSIONS:
                ext = ".png"
            media_path = path.with_suffix(ext)
            try:
                shutil.copy2(self.new_prompt_media_path, media_path)
                media_msg = f" + media {media_path.name}"
            except Exception:
                self.app._status("Prompt saved, but media copy failed.")
        self.new_prompt_filename.clear()
        self.new_prompt_text.clear()
        self._clear_prompt_image()
        self.app._refresh_library_ui()
        self.app._status(f"Saved prompt: {path.parent.name}/{path.name}{media_msg}")

    def _set_prompt_media_file(self, media_path: Path):
        if not media_path.exists() or not media_path.is_file():
            return
        ext = media_path.suffix.lower()
        if ext == ".jpeg":
            ext = ".jpg"
        if ext not in MEDIA_PREVIEW_EXTENSIONS:
            self.app._status("Unsupported media file.")
            return
        self.new_prompt_image = None
        self.new_prompt_media_path = media_path
        self.new_prompt_media_ext = ext
        self.new_prompt_image_ext = ext if ext in IMAGE_PREVIEW_EXTENSIONS else ".png"
        self._update_prompt_image_preview()

    def _set_prompt_image(self, img: QtGui.QImage, ext: str = ".png"):
        if img.isNull():
            return
        self.new_prompt_image = img
        self.new_prompt_media_path = None
        e = (ext or ".png").lower().strip()
        if not e.startswith("."):
            e = "." + e
        if e == ".jpeg":
            e = ".jpg"
        self.new_prompt_image_ext = e if e in IMAGE_PREVIEW_EXTENSIONS else ".png"
        self.new_prompt_media_ext = self.new_prompt_image_ext
        self._update_prompt_image_preview()

    def _stop_prompt_video_preview(self):
        if self._create_media_player is not None:
            try:
                self._create_media_player.stop()
            except Exception:
                pass
        if self.new_prompt_video_widget is not None:
            self.new_prompt_video_widget.setVisible(False)

    def _prompt_media_target_size(self) -> QtCore.QSize:
        margins = self.new_prompt_media_frame.contentsMargins()
        size = self.new_prompt_media_frame.size() - QtCore.QSize(
            margins.left() + margins.right(), margins.top() + margins.bottom()
        )
        if size.width() < 32 or size.height() < 32:
            size = QtCore.QSize(320, 160)
        return size

    def _update_prompt_image_preview(self):
        self._stop_prompt_video_preview()
        self.new_prompt_image_preview.setVisible(True)
        self.new_prompt_image_preview.setPixmap(QtGui.QPixmap())
        if self.new_prompt_media_path is not None and self.new_prompt_media_path.exists():
            ext = self.new_prompt_media_path.suffix.lower()
            if ext == ".jpeg":
                ext = ".jpg"
            if ext in VIDEO_PREVIEW_EXTENSIONS:
                if QtMultimedia is None or self.new_prompt_video_widget is None:
                    self.new_prompt_image_preview.setText(f"Video selected: {self.new_prompt_media_path.name}")
                    return
                try:
                    if self._create_media_player is None:
                        self._create_media_player = QtMultimedia.QMediaPlayer(self)
                        self._create_media_audio = QtMultimedia.QAudioOutput(self)
                        self._create_media_audio.setMuted(True)
                        self._create_media_player.setAudioOutput(self._create_media_audio)
                        self._create_media_player.setVideoOutput(self.new_prompt_video_widget)
                        _enable_media_player_loop(self._create_media_player)
                    self.new_prompt_image_preview.setVisible(False)
                    self.new_prompt_video_widget.setVisible(True)
                    self._create_media_player.setSource(QtCore.QUrl.fromLocalFile(str(self.new_prompt_media_path)))
                    self._create_media_player.play()
                    return
                except Exception:
                    self.new_prompt_image_preview.setVisible(True)
                    self.new_prompt_image_preview.setText(f"Video selected: {self.new_prompt_media_path.name}")
                    return

            pix = QtGui.QPixmap(str(self.new_prompt_media_path))
            if pix.isNull():
                self.new_prompt_image_preview.setText(f"Media selected: {self.new_prompt_media_path.name}")
                return
            target = self._prompt_media_target_size()
            scaled = pix.scaled(target, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.new_prompt_image_preview.setText("")
            self.new_prompt_image_preview.setPixmap(scaled)
            return

        if self.new_prompt_image is None or self.new_prompt_image.isNull():
            self.new_prompt_image_preview.setText("No media selected")
            return
        target = self._prompt_media_target_size()
        pix = QtGui.QPixmap.fromImage(self.new_prompt_image)
        scaled = pix.scaled(target, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.new_prompt_image_preview.setText("")
        self.new_prompt_image_preview.setPixmap(scaled)

    def _clear_prompt_image(self):
        self.new_prompt_image = None
        self.new_prompt_media_path = None
        self.new_prompt_image_ext = ".png"
        self.new_prompt_media_ext = ".png"
        self._update_prompt_image_preview()

    def _browse_prompt_image(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select media",
            str(self.app.core.library_dir),
            "Media (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.webm *.mp4 *.m4v *.mov *.avi *.mkv *.wmv *.mpg *.mpeg);;All files (*.*)",
        )
        if not path:
            return
        p = Path(path)
        ext = p.suffix.lower()
        if ext == ".jpeg":
            ext = ".jpg"
        if ext not in MEDIA_PREVIEW_EXTENSIONS:
            self.app._status("Unsupported media file.")
            return
        self._set_prompt_media_file(p)
        self.app._status(f"Media loaded: {p.name}")

    def _paste_prompt_image(self):
        cb = QtWidgets.QApplication.clipboard()
        mime = cb.mimeData()
        if mime is None:
            return False
        img = cb.image()
        if img is not None and not img.isNull():
            self._set_prompt_image(img, ".png")
            self.app._status("Image pasted from clipboard.")
            return True
        if mime.hasUrls():
            for url in mime.urls():
                if not url.isLocalFile():
                    continue
                p = Path(url.toLocalFile())
                ext = p.suffix.lower()
                if ext == ".jpeg":
                    ext = ".jpg"
                if ext not in MEDIA_PREVIEW_EXTENSIONS:
                    continue
                self._set_prompt_media_file(p)
                self.app._status(f"Media pasted: {p.name}")
                return True
        return False

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.matches(QtGui.QKeySequence.Paste):
            if self._paste_prompt_image():
                event.accept()
                return
        super().keyPressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_prompt_image_preview()

    def _create_tag(self):
        name = self.new_tag_name.text().strip()
        if not name:
            self.app._status("Tag name is empty.")
            return
        try:
            created = self.app.core.add_tag(name)
        except Exception as e:
            self.app._status(str(e))
            return
        self.new_tag_name.setText("")
        self.app._refresh_tag_pref_options()
        self.app._status(f"Created tag: {created}")


class AssignTagDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        if parent:
            self.setStyleSheet(parent.styleSheet())
        self.setAutoFillBackground(True)
        self.setWindowTitle("Assign Tag")
        if parent and hasattr(parent, "_apply_titlebar_to"):
            parent._apply_titlebar_to(self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        form = QtWidgets.QGridLayout()
        form.setHorizontalSpacing(8)
        form.setVerticalSpacing(8)
        lbl = QtWidgets.QLabel("Category type")
        self.kind_combo = QtWidgets.QComboBox()
        self.folder_combo = QtWidgets.QComboBox()
        self.folder_combo.setEditable(True)
        self.folder_combo.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        completer = self.folder_combo.completer()
        if completer is not None:
            completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            completer.setFilterMode(QtCore.Qt.MatchContains)
        if self.folder_combo.lineEdit():
            self.folder_combo.lineEdit().setPlaceholderText("Search category...")
        form.addWidget(lbl, 0, 0)
        form.addWidget(self.kind_combo, 0, 1)
        form.addWidget(QtWidgets.QLabel("Category"), 1, 0)
        form.addWidget(self.folder_combo, 1, 1)
        layout.addLayout(form)

        self.tags_area = QtWidgets.QScrollArea()
        self.tags_area.setObjectName("listArea")
        self.tags_area.setWidgetResizable(True)
        self.tags_frame = QtWidgets.QWidget()
        self.tags_frame.setObjectName("listContainer")
        self.tags_layout = QtWidgets.QVBoxLayout(self.tags_frame)
        self.tags_layout.setContentsMargins(8, 8, 8, 8)
        self.tags_layout.setSpacing(4)
        self.tags_area.setWidget(self.tags_frame)
        layout.addWidget(self.tags_area, 1)
        self.tag_checks = {}

        btns = QtWidgets.QHBoxLayout()
        btns.addStretch(1)
        self.btn_save = QtWidgets.QPushButton("Save")
        self.btn_cancel = QtWidgets.QPushButton("Cancel")
        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_save.clicked.connect(self._save)
        self.btn_cancel.clicked.connect(self.reject)
        self.kind_combo.currentIndexChanged.connect(self._refresh_folders)
        self.folder_combo.currentIndexChanged.connect(self._load_tags)

        self._populate_kind_combo()
        self._build_tag_list()
        self._refresh_folders()
        self._load_tags()
        self._finalize_size()
        self.finished.connect(lambda _: _save_popup_geometry(self, "assign_tag_dialog"))

    def _finalize_size(self):
        self.adjustSize()
        hint = self.sizeHint()
        fallback = hint if hint.isValid() else QtCore.QSize(620, 520)
        _restore_popup_geometry(self, "assign_tag_dialog", fallback)

    def _build_tag_list(self):
        while self.tags_layout.count():
            item = self.tags_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self.tag_checks = {}
        tags = self.app.core.all_tags()
        for tag in tags:
            cb = QtWidgets.QCheckBox(tag)
            cb.setObjectName("list_item")
            self.tag_checks[tag] = cb
            self.tags_layout.addWidget(cb)
        self.tags_layout.addStretch(1)

    def _load_tags(self):
        if not hasattr(self, "tag_checks"):
            return
        folder = self.folder_combo.currentText()
        if not folder or folder == "(none)":
            for cb in self.tag_checks.values():
                cb.setChecked(False)
            return
        active = set(self.app.core.get_folder_tags(folder))
        for tag, cb in self.tag_checks.items():
            cb.setChecked(tag in active)

    def _save(self):
        folder = self.folder_combo.currentText()
        if not folder or folder == "(none)":
            self.app._status("No category available.")
            return
        tags = [tag for tag, cb in self.tag_checks.items() if cb.isChecked()]
        try:
            self.app.core.set_folder_tags(folder, tags)
        except Exception as e:
            self.app._status(str(e))
            return
        self.app._refresh_tag_pref_options()
        self.app._status(f"Tags updated: {folder}")
        self.accept()

    def _populate_kind_combo(self):
        self.kind_combo.clear()
        items: list[tuple[str, str]] = []
        for slot in self.app.core.get_slots():
            label = str(slot.get("label") or slot.get("id") or "").strip()
            prefix = str(slot.get("prefix") or "").strip()
            if not label or not prefix:
                continue
            items.append((label.upper(), prefix))
        if not items:
            for slot in DEFAULT_SLOTS:
                items.append((str(slot.get("label", "")).upper(), str(slot.get("prefix", ""))))
        for label, prefix in items:
            self.kind_combo.addItem(label, prefix)

    def _refresh_folders(self):
        prefix = str(self.kind_combo.currentData() or "").strip()
        vals = [p.name for p in self.app.core.folders_by_prefix(prefix)] if prefix else []
        self.folder_combo.blockSignals(True)
        self.folder_combo.clear()
        if not vals:
            vals = ["(none)"]
        self.folder_combo.addItems(vals)
        self.folder_combo.blockSignals(False)
        if vals:
            self.folder_combo.setCurrentIndex(0)
        self._load_tags()
class PromptZoneWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.core = PromptZoneCore(app_root())
        self.use_qdarktheme = False
        self._drag_exclude_active = False
        self._drag_exclude_value = False
        self._drag_exclude_hovered = None
        self._exclude_search_cache = {"ACTIONSTYLE": {}, "CLOTHES": {}, "COMPOSITION": {}, "I2V": {}}
        self.excluded_tags = set(self.core.settings.get("excluded_tags", []) or [])

        self.colors = dict(DEFAULT_THEME_COLORS)
        stored_preset = self.core.settings.get("theme_preset")
        stored_colors = self.core.settings.get("theme_colors")
        custom_presets = self.core.settings.get("custom_presets", {})
        if isinstance(custom_presets, dict):
            for name, preset in custom_presets.items():
                if isinstance(preset, dict):
                    THEME_PRESETS[name] = preset
        if isinstance(stored_preset, str) and stored_preset in THEME_PRESETS:
            self.colors.update(THEME_PRESETS[stored_preset])
            self.core.settings["theme_colors"] = dict(self.colors)
            self.core.save_settings()
        elif isinstance(stored_colors, dict):
            self.colors.update(stored_colors)

        self._ensure_slot_settings()

        self._load_custom_fonts()
        QtWidgets.QApplication.instance().setFont(QtGui.QFont("Roboto", 12))
        self.setWindowTitle(APP_TITLE)
        self._set_window_icon()
        self._geometry_restored = False
        self.resize(1200, 820)

        self.icon_dir = app_root() / "assets" / "icons"
        self._icons = {"black": {}, "white": {}}
        self._load_icons()
        self._icon_color = "white"

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        root = QtWidgets.QGridLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setHorizontalSpacing(12)
        root.setVerticalSpacing(12)
        root.setRowStretch(0, 0)
        root.setRowStretch(1, 1)

        # Top bar
        top = QtWidgets.QFrame()
        top.setObjectName("topbar")
        top.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        top_layout = QtWidgets.QVBoxLayout(top)
        top_layout.setContentsMargins(12, 10, 12, 8)
        top_layout.setSpacing(6)
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(10)
        self.brand = QtWidgets.QLabel("PromptZone - Prompt Library / Manager / Randomizer")
        self.brand.setObjectName("brand")
        try:
            self.brand.setFont(QtGui.QFont("Titillium Web", 16, QtGui.QFont.Bold))
        except Exception:
            pass
        row.addWidget(self.brand, 0, QtCore.Qt.AlignVCenter)
        self.status_line = QtWidgets.QLabel("Ready")
        self.status_line.setObjectName("status")
        row.addWidget(self.status_line, 0, QtCore.Qt.AlignVCenter)
        self._status_effect = QtWidgets.QGraphicsOpacityEffect(self.status_line)
        self._status_effect.setOpacity(1.0)
        self.status_line.setGraphicsEffect(self._status_effect)
        self._status_anim = None
        self._status_timer = QtCore.QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self._fade_status)
        row.addStretch(1)
        self.btn_copy = QtWidgets.QPushButton("Copy Output")
        self.btn_save = QtWidgets.QPushButton("Save TXT")
        self.btn_create = QtWidgets.QPushButton("Create")
        self.btn_assign_tag = QtWidgets.QPushButton("Assign tag")
        self.btn_reload = QtWidgets.QPushButton("Reload")
        self.btn_manage_slots = QtWidgets.QPushButton("Manage Slots")
        self.btn_customize = QtWidgets.QPushButton("Customise")
        for b in [
            self.btn_copy,
            self.btn_save,
            self.btn_create,
            self.btn_assign_tag,
            self.btn_reload,
            self.btn_manage_slots,
            self.btn_customize,
        ]:
            b.setMinimumHeight(30)
            row.addWidget(b, 0, QtCore.Qt.AlignVCenter)

        self.preset_combo = QtWidgets.QComboBox()
        self.preset_combo.addItems(list(THEME_PRESETS.keys()))
        self.preset_combo.setFixedWidth(140)
        row.addWidget(self.preset_combo, 0, QtCore.Qt.AlignVCenter)
        top_layout.addLayout(row)

        root.addWidget(top, 0, 0, 1, 3)

        # Left panel
        self.left = self._card("Randomize Settings")
        left_layout = self.left.layout()

        form_widget = QtWidgets.QWidget()
        form_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        form = QtWidgets.QGridLayout(form_widget)
        form.setHorizontalSpacing(8)
        form.setVerticalSpacing(8)

        self.n_sets = QtWidgets.QLineEdit()
        self.btn_n_sets_minus = QtWidgets.QPushButton("-")
        self.btn_n_sets_plus = QtWidgets.QPushButton("+")
        for b in [self.btn_n_sets_minus, self.btn_n_sets_plus]:
            b.setObjectName("iconSquare")
            b.setFixedSize(26, 26)
        self.n_sets_wrap = QtWidgets.QWidget()
        n_sets_layout = QtWidgets.QHBoxLayout(self.n_sets_wrap)
        n_sets_layout.setContentsMargins(0, 0, 0, 0)
        n_sets_layout.setSpacing(6)
        n_sets_layout.addWidget(self.n_sets, 1)
        n_sets_layout.addWidget(self.btn_n_sets_minus)
        n_sets_layout.addWidget(self.btn_n_sets_plus)
        self.btn_generate = QtWidgets.QPushButton("Randomize")
        self.btn_generate.setObjectName("primary")
        self.tag_pref = QtWidgets.QPushButton()
        self.tag_pref.setObjectName("dropdownButton")
        self.tag_pref.setCheckable(True)
        self.tag_pref.setAutoDefault(False)
        self.tag_pref.setDefault(False)
        self.tag_pref_menu = QtWidgets.QMenu(self)
        self.tag_pref_menu.aboutToHide.connect(
            lambda m=self.tag_pref_menu, b=self.tag_pref: self._on_menu_about_to_hide(m, b)
        )
        self.tag_pref_list = QtWidgets.QListWidget(self.tag_pref_menu)
        self._attach_menu_list(self.tag_pref_menu, self.tag_pref_list)
        self.tag_pref.clicked.connect(lambda: self._toggle_menu(self.tag_pref_menu, self.tag_pref))
        self.tag_pref_list.itemChanged.connect(self._on_tag_pref_item_changed)
        self.btn_excl_tag = QtWidgets.QPushButton()
        self.btn_excl_tag.setToolTip("Exclude tags from random generation")
        self.btn_excl_tag.setFixedSize(28, 28)
        self.btn_excl_tag.setObjectName("iconSquare")
        self.excl_tag_menu = QtWidgets.QMenu(self)
        self.btn_excl_tag.setCheckable(True)
        self.btn_excl_tag.setAutoDefault(False)
        self.btn_excl_tag.setDefault(False)
        self.excl_tag_menu.aboutToHide.connect(self._on_excl_tag_menu_hide)
        self.btn_excl_tag.clicked.connect(self._toggle_exclude_tag_menu)
        self.weight_strength = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.weight_strength.setRange(0, 100)
        self.weight_strength.setValue(65)

        self.lbl_sets = QtWidgets.QLabel("How many sets")
        self.lbl_tag = QtWidgets.QLabel("Preferred tag")
        self.lbl_excl_tag = QtWidgets.QLabel("Exclude tag")
        form.addWidget(self.lbl_sets, 0, 0)
        form.addWidget(self.lbl_tag, 0, 1)
        form.addWidget(self.lbl_excl_tag, 0, 2)
        form.addWidget(self.n_sets_wrap, 1, 0)
        form.addWidget(self.tag_pref, 1, 1)
        form.addWidget(self.btn_excl_tag, 1, 2, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        left_layout.addWidget(form_widget)

        self.lbl_weight = QtWidgets.QLabel("Weight strength")
        left_layout.addWidget(self.lbl_weight)
        self.weight_strength.setFixedHeight(22)
        self.lbl_weight_value = QtWidgets.QLabel("65%")
        self.lbl_weight_value.setObjectName("muted")
        self.lbl_weight_value.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.lbl_weight_value.setFixedWidth(44)
        weight_row = QtWidgets.QWidget()
        weight_row_layout = QtWidgets.QHBoxLayout(weight_row)
        weight_row_layout.setContentsMargins(0, 0, 0, 0)
        weight_row_layout.setSpacing(8)
        weight_row_layout.addWidget(self.weight_strength, 1)
        weight_row_layout.addWidget(self.lbl_weight_value, 0, QtCore.Qt.AlignRight)
        left_layout.addWidget(weight_row)
        self._update_weight_strength_preview(self.weight_strength.value())
        left_layout.addWidget(self._section_divider())

        self.action_cat = QtWidgets.QPushButton()
        self.clothes_cat = QtWidgets.QPushButton()
        self.composition_cat = QtWidgets.QPushButton()
        self.i2v_cat = QtWidgets.QPushButton()
        for btn in [self.action_cat, self.clothes_cat, self.composition_cat, self.i2v_cat]:
            btn.setObjectName("dropdownButton")
            btn.setCheckable(True)
            btn.setAutoDefault(False)
            btn.setDefault(False)
        self.action_cat_menu = QtWidgets.QMenu(self)
        self.clothes_cat_menu = QtWidgets.QMenu(self)
        self.composition_cat_menu = QtWidgets.QMenu(self)
        self.i2v_cat_menu = QtWidgets.QMenu(self)
        self.action_cat_menu.aboutToHide.connect(
            lambda m=self.action_cat_menu, b=self.action_cat: self._on_menu_about_to_hide(m, b)
        )
        self.clothes_cat_menu.aboutToHide.connect(
            lambda m=self.clothes_cat_menu, b=self.clothes_cat: self._on_menu_about_to_hide(m, b)
        )
        self.composition_cat_menu.aboutToHide.connect(
            lambda m=self.composition_cat_menu, b=self.composition_cat: self._on_menu_about_to_hide(m, b)
        )
        self.i2v_cat_menu.aboutToHide.connect(
            lambda m=self.i2v_cat_menu, b=self.i2v_cat: self._on_menu_about_to_hide(m, b)
        )
        self.action_cat_list = QtWidgets.QListWidget(self.action_cat_menu)
        self.clothes_cat_list = QtWidgets.QListWidget(self.clothes_cat_menu)
        self.composition_cat_list = QtWidgets.QListWidget(self.composition_cat_menu)
        self.i2v_cat_list = QtWidgets.QListWidget(self.i2v_cat_menu)
        self._attach_menu_list(self.action_cat_menu, self.action_cat_list)
        self._attach_menu_list(self.clothes_cat_menu, self.clothes_cat_list)
        self._attach_menu_list(self.composition_cat_menu, self.composition_cat_list)
        self._attach_menu_list(self.i2v_cat_menu, self.i2v_cat_list)
        self.action_cat.clicked.connect(lambda: self._toggle_menu(self.action_cat_menu, self.action_cat))
        self.clothes_cat.clicked.connect(lambda: self._toggle_menu(self.clothes_cat_menu, self.clothes_cat))
        self.composition_cat.clicked.connect(lambda: self._toggle_menu(self.composition_cat_menu, self.composition_cat))
        self.i2v_cat.clicked.connect(lambda: self._toggle_menu(self.i2v_cat_menu, self.i2v_cat))
        self.action_cat_list.itemChanged.connect(lambda item: self._on_category_item_changed("action", item))
        self.clothes_cat_list.itemChanged.connect(lambda item: self._on_category_item_changed("clothes", item))
        self.composition_cat_list.itemChanged.connect(lambda item: self._on_category_item_changed("composition", item))
        self.i2v_cat_list.itemChanged.connect(lambda item: self._on_category_item_changed("i2v", item))
        self.tag_pref_selected = set()
        self.action_cat_selected = set()
        self.clothes_cat_selected = set()
        self.composition_cat_selected = set()
        self.i2v_cat_selected = set()
        self.lbl_action_cat = QtWidgets.QLabel("ACTIONSTYLE category")
        left_layout.addWidget(self.lbl_action_cat)
        left_layout.addWidget(self.action_cat)
        self.lbl_clothes_cat = QtWidgets.QLabel("CLOTHES category")
        left_layout.addWidget(self.lbl_clothes_cat)
        left_layout.addWidget(self.clothes_cat)
        self.lbl_composition_cat = QtWidgets.QLabel("COMPOSITION category")
        left_layout.addWidget(self.lbl_composition_cat)
        left_layout.addWidget(self.composition_cat)
        self.lbl_i2v_cat = QtWidgets.QLabel("I2V category")
        left_layout.addWidget(self.lbl_i2v_cat)
        left_layout.addWidget(self.i2v_cat)
        self.dynamic_category_frame = QtWidgets.QWidget()
        self.dynamic_category_layout = QtWidgets.QVBoxLayout(self.dynamic_category_frame)
        self.dynamic_category_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_category_layout.setSpacing(6)
        left_layout.addWidget(self.dynamic_category_frame)
        self.dynamic_category_labels = {}
        left_layout.addWidget(self._section_divider())

        self.lock_action = QtWidgets.QCheckBox("Lock ACTIONSTYLE")
        self.lock_clothes = QtWidgets.QCheckBox("Lock CLOTHES")
        self.lock_composition = QtWidgets.QCheckBox("Lock COMPOSITION")
        self.lock_i2v = QtWidgets.QCheckBox("Lock I2V")
        self.skip_minimized = QtWidgets.QCheckBox("Skip minimized prompts")
        self.append_output = QtWidgets.QCheckBox("Append output")
        self.avoid_repeats = QtWidgets.QCheckBox("Avoid repeats (session)")
        self.one_per_folder = QtWidgets.QCheckBox("Only one per folder (per batch)")

        self.dynamic_lock_frame = QtWidgets.QWidget()
        self.dynamic_lock_layout = QtWidgets.QVBoxLayout(self.dynamic_lock_frame)
        self.dynamic_lock_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_lock_layout.setSpacing(4)
        left_layout.addWidget(self.dynamic_lock_frame, 0, QtCore.Qt.AlignHCenter)
        left_layout.addWidget(self._section_divider())

        self._checkbox_frame = QtWidgets.QWidget()
        checkbox_layout = QtWidgets.QVBoxLayout(self._checkbox_frame)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setSpacing(4)
        for w in [
            self.lock_action,
            self.lock_clothes,
            self.lock_composition,
            self.lock_i2v,
            self.skip_minimized,
            self.append_output,
            self.avoid_repeats,
            self.one_per_folder,
        ]:
            w.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            checkbox_layout.addWidget(w, 0, QtCore.Qt.AlignLeft)
        left_layout.addWidget(self._checkbox_frame, 0, QtCore.Qt.AlignHCenter)
        left_layout.addWidget(self._section_divider())

        self.btn_browse_action = QtWidgets.QPushButton("Browse ACTIONSTYLE...")
        self.btn_browse_clothes = QtWidgets.QPushButton("Browse CLOTHES...")
        self.btn_browse_composition = QtWidgets.QPushButton("Browse COMPOSITION...")
        self.btn_browse_i2v = QtWidgets.QPushButton("Browse I2V...")
        left_layout.addWidget(self.btn_browse_action, 0, QtCore.Qt.AlignHCenter)
        left_layout.addWidget(self.btn_browse_clothes, 0, QtCore.Qt.AlignHCenter)
        left_layout.addWidget(self.btn_browse_composition, 0, QtCore.Qt.AlignHCenter)
        left_layout.addWidget(self.btn_browse_i2v, 0, QtCore.Qt.AlignHCenter)
        self.dynamic_browse_frame = QtWidgets.QWidget()
        self.dynamic_browse_layout = QtWidgets.QVBoxLayout(self.dynamic_browse_frame)
        self.dynamic_browse_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_browse_layout.setSpacing(4)
        left_layout.addWidget(self.dynamic_browse_frame, 0, QtCore.Qt.AlignHCenter)
        self.dynamic_browse_buttons = {}
        left_layout.addStretch(1)
        left_layout.addWidget(self._section_divider())

        self.gen_action = QtWidgets.QCheckBox("Randomize ACTIONSTYLE")
        self.gen_clothes = QtWidgets.QCheckBox("Randomize CLOTHES")
        self.gen_composition = QtWidgets.QCheckBox("Randomize COMPOSITION")
        self.gen_i2v = QtWidgets.QCheckBox("Randomize I2V")
        self.btn_clear_action = QtWidgets.QPushButton("Clear")
        self.btn_clear_clothes = QtWidgets.QPushButton("Clear")
        self.btn_clear_composition = QtWidgets.QPushButton("Clear")
        self.btn_clear_i2v = QtWidgets.QPushButton("Clear")
        self.btn_rand_action = QtWidgets.QPushButton()
        self.btn_rand_clothes = QtWidgets.QPushButton()
        self.btn_rand_composition = QtWidgets.QPushButton()
        self.btn_rand_i2v = QtWidgets.QPushButton()
        self.btn_rand_action.setToolTip("Randomize ACTIONSTYLE")
        self.btn_rand_clothes.setToolTip("Randomize CLOTHES")
        self.btn_rand_composition.setToolTip("Randomize COMPOSITION")
        self.btn_rand_i2v.setToolTip("Randomize I2V")
        for b in [self.btn_rand_action, self.btn_rand_clothes, self.btn_rand_composition, self.btn_rand_i2v]:
            b.setObjectName("iconSquare")
            b.setFixedSize(26, 26)
        for b in [self.btn_clear_action, self.btn_clear_clothes, self.btn_clear_composition, self.btn_clear_i2v]:
            b.setMinimumHeight(26)
            b.setMinimumWidth(72)
        self.gen_action.setChecked(True)
        self.gen_clothes.setChecked(True)
        self.gen_composition.setChecked(True)
        self.gen_i2v.setChecked(True)
        self._gen_frame = QtWidgets.QWidget()
        gen_layout = QtWidgets.QVBoxLayout(self._gen_frame)
        gen_layout.setContentsMargins(0, 0, 0, 0)
        gen_layout.setSpacing(6)

        def add_gen_row(cb: QtWidgets.QCheckBox, rand_btn: QtWidgets.QPushButton, clear_btn: QtWidgets.QPushButton):
            row = QtWidgets.QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(8)
            cb.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            row.addWidget(cb, 0, QtCore.Qt.AlignLeft)
            row.addStretch(1)
            row.addWidget(rand_btn)
            row.addWidget(clear_btn)
            gen_layout.addLayout(row)

        add_gen_row(self.gen_action, self.btn_rand_action, self.btn_clear_action)
        add_gen_row(self.gen_clothes, self.btn_rand_clothes, self.btn_clear_clothes)
        add_gen_row(self.gen_composition, self.btn_rand_composition, self.btn_clear_composition)
        add_gen_row(self.gen_i2v, self.btn_rand_i2v, self.btn_clear_i2v)
        left_layout.addWidget(self._gen_frame, 0, QtCore.Qt.AlignHCenter)

        self.dynamic_gen_frame = QtWidgets.QWidget()
        self.dynamic_gen_layout = QtWidgets.QVBoxLayout(self.dynamic_gen_frame)
        self.dynamic_gen_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_gen_layout.setSpacing(6)
        left_layout.addWidget(self.dynamic_gen_frame, 0, QtCore.Qt.AlignHCenter)

        self.dynamic_slot_controls = {}
        self.btn_generate.setMinimumHeight(32)
        left_layout.addWidget(self.btn_generate)

        # Center panel
        self.center = self._card("Slots")
        center_layout = self.center.layout()
        self.kpi = QtWidgets.QLabel("ACTIONSTYLE: 0 / CLOTHES: 0 / COMPOSITION: 0 / I2V: 0")
        self.kpi.setObjectName("muted")
        center_layout.addWidget(self.kpi)

        self.action_box = self._slot_text()
        self.clothes_box = self._slot_text()
        self.composition_box = self._slot_text()
        self.i2v_box = self._slot_text()
        self.output_box = QtWidgets.QTextEdit()
        self.output_box.setObjectName("slot")
        self.output_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.output_box.setAcceptRichText(False)
        self.output_box.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.FixedColumnWidth)
        self.output_box.setLineWrapColumnOrWidth(165)
        self.output_box.setWordWrapMode(QtGui.QTextOption.WordWrap)

        self.lbl_action_slot = QtWidgets.QLabel("ACTIONSTYLE slot")
        self.lbl_action_src = QtWidgets.QLabel("")
        self.lbl_action_src.setObjectName("muted")
        self.action_header = self._slot_header(self.lbl_action_slot, self.lbl_action_src)
        center_layout.addWidget(self.action_header)
        center_layout.addWidget(self.action_box)
        self.lbl_clothes_slot = QtWidgets.QLabel("CLOTHES slot")
        self.lbl_clothes_src = QtWidgets.QLabel("")
        self.lbl_clothes_src.setObjectName("muted")
        self.clothes_header = self._slot_header(self.lbl_clothes_slot, self.lbl_clothes_src)
        center_layout.addWidget(self.clothes_header)
        center_layout.addWidget(self.clothes_box)
        self.lbl_composition_slot = QtWidgets.QLabel("COMPOSITION slot")
        self.lbl_composition_src = QtWidgets.QLabel("")
        self.lbl_composition_src.setObjectName("muted")
        self.composition_header = self._slot_header(self.lbl_composition_slot, self.lbl_composition_src)
        center_layout.addWidget(self.composition_header)
        center_layout.addWidget(self.composition_box)
        self.lbl_i2v_slot = QtWidgets.QLabel("I2V slot")
        self.lbl_i2v_src = QtWidgets.QLabel("")
        self.lbl_i2v_src.setObjectName("muted")
        self.i2v_header = self._slot_header(self.lbl_i2v_slot, self.lbl_i2v_src)
        center_layout.addWidget(self.i2v_header)
        center_layout.addWidget(self.i2v_box)

        self.dynamic_slots_frame = QtWidgets.QWidget()
        self.dynamic_slots_layout = QtWidgets.QVBoxLayout(self.dynamic_slots_frame)
        self.dynamic_slots_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_slots_layout.setSpacing(8)
        center_layout.addWidget(self.dynamic_slots_frame)
        self.dynamic_slot_boxes = {}
        self.dynamic_slot_labels = {}
        self.dynamic_slot_sources = {}
        self.lbl_output = QtWidgets.QLabel("Output")
        self.lbl_output_src = QtWidgets.QLabel("")
        self.lbl_output_src.setObjectName("muted")
        self.lbl_output_src.setVisible(False)
        center_layout.addWidget(self._slot_header(self.lbl_output, self.lbl_output_src))
        center_layout.addWidget(self.output_box)

        # center panel added via splitter below

        # Right panel
        self.right = self._card("Exclude Categories")
        right_layout = self.right.layout()
        self.lbl_excl_all = QtWidgets.QLabel("Filter all excludes")
        right_layout.addWidget(self.lbl_excl_all)
        self.excl_all_filter = QtWidgets.QLineEdit()
        self.excl_all_filter.setPlaceholderText("Filter filename + content...")
        right_layout.addWidget(self.excl_all_filter)
        self.lbl_excl_action = QtWidgets.QLabel("Exclude ACTIONSTYLE")
        right_layout.addWidget(self.lbl_excl_action)
        self.excl_action_filter = QtWidgets.QLineEdit()
        self.excl_action_filter.setPlaceholderText("Filter filename + content...")
        right_layout.addWidget(self.excl_action_filter)
        self.excl_action = QtWidgets.QScrollArea()
        self.excl_action.setObjectName("listArea")
        self.excl_action.setWidgetResizable(True)
        self.excl_action_frame = QtWidgets.QWidget()
        self.excl_action_frame.setObjectName("listContainer")
        self.excl_action_layout = QtWidgets.QVBoxLayout(self.excl_action_frame)
        self.excl_action_layout.setContentsMargins(8, 8, 8, 8)
        self.excl_action_layout.setSpacing(4)
        self.excl_action.setWidget(self.excl_action_frame)
        right_layout.addWidget(self.excl_action, 1)
        self.excl_action.viewport().setMouseTracking(True)
        self.excl_action.viewport().installEventFilter(self)

        self.lbl_excl_clothes = QtWidgets.QLabel("Exclude CLOTHES")
        right_layout.addWidget(self.lbl_excl_clothes)
        self.excl_clothes_filter = QtWidgets.QLineEdit()
        self.excl_clothes_filter.setPlaceholderText("Filter filename + content...")
        right_layout.addWidget(self.excl_clothes_filter)
        self.excl_clothes = QtWidgets.QScrollArea()
        self.excl_clothes.setObjectName("listArea")
        self.excl_clothes.setWidgetResizable(True)
        self.excl_clothes_frame = QtWidgets.QWidget()
        self.excl_clothes_frame.setObjectName("listContainer")
        self.excl_clothes_layout = QtWidgets.QVBoxLayout(self.excl_clothes_frame)
        self.excl_clothes_layout.setContentsMargins(8, 8, 8, 8)
        self.excl_clothes_layout.setSpacing(4)
        self.excl_clothes.setWidget(self.excl_clothes_frame)
        right_layout.addWidget(self.excl_clothes, 1)
        self.excl_clothes.viewport().setMouseTracking(True)
        self.excl_clothes.viewport().installEventFilter(self)

        self.lbl_excl_composition = QtWidgets.QLabel("Exclude COMPOSITION")
        right_layout.addWidget(self.lbl_excl_composition)
        self.excl_composition_filter = QtWidgets.QLineEdit()
        self.excl_composition_filter.setPlaceholderText("Filter filename + content...")
        right_layout.addWidget(self.excl_composition_filter)
        self.excl_composition = QtWidgets.QScrollArea()
        self.excl_composition.setObjectName("listArea")
        self.excl_composition.setWidgetResizable(True)
        self.excl_composition_frame = QtWidgets.QWidget()
        self.excl_composition_frame.setObjectName("listContainer")
        self.excl_composition_layout = QtWidgets.QVBoxLayout(self.excl_composition_frame)
        self.excl_composition_layout.setContentsMargins(8, 8, 8, 8)
        self.excl_composition_layout.setSpacing(4)
        self.excl_composition.setWidget(self.excl_composition_frame)
        right_layout.addWidget(self.excl_composition, 1)
        self.excl_composition.viewport().setMouseTracking(True)
        self.excl_composition.viewport().installEventFilter(self)

        self.lbl_excl_i2v = QtWidgets.QLabel("Exclude I2V")
        right_layout.addWidget(self.lbl_excl_i2v)
        self.excl_i2v_filter = QtWidgets.QLineEdit()
        self.excl_i2v_filter.setPlaceholderText("Filter filename + content...")
        right_layout.addWidget(self.excl_i2v_filter)
        self.excl_i2v = QtWidgets.QScrollArea()
        self.excl_i2v.setObjectName("listArea")
        self.excl_i2v.setWidgetResizable(True)
        self.excl_i2v_frame = QtWidgets.QWidget()
        self.excl_i2v_frame.setObjectName("listContainer")
        self.excl_i2v_layout = QtWidgets.QVBoxLayout(self.excl_i2v_frame)
        self.excl_i2v_layout.setContentsMargins(8, 8, 8, 8)
        self.excl_i2v_layout.setSpacing(4)
        self.excl_i2v.setWidget(self.excl_i2v_frame)
        right_layout.addWidget(self.excl_i2v, 1)
        self.excl_i2v.viewport().setMouseTracking(True)
        self.excl_i2v.viewport().installEventFilter(self)

        self.dynamic_excl_frame = QtWidgets.QWidget()
        self.dynamic_excl_layout = QtWidgets.QVBoxLayout(self.dynamic_excl_frame)
        self.dynamic_excl_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_excl_layout.setSpacing(10)
        right_layout.addWidget(self.dynamic_excl_frame)
        self.dynamic_excl_vars = {}
        self.dynamic_excl_filters = {}

        btns = QtWidgets.QHBoxLayout()
        self.btn_clear_excludes = QtWidgets.QPushButton("Clear excludes")
        self.btn_reset_repeats = QtWidgets.QPushButton("Reset repeats")
        btns.addWidget(self.btn_clear_excludes)
        btns.addWidget(self.btn_reset_repeats)
        right_layout.addLayout(btns)

        # Center/Right splitter
        self.center_right_split = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.center_right_split.setChildrenCollapsible(False)
        self.center_right_split.setHandleWidth(6)
        self.center_right_split.addWidget(self.center)
        self.center_right_split.addWidget(self.right)
        self.center_right_split.setStretchFactor(0, 3)
        self.center_right_split.setStretchFactor(1, 2)

        # Left | (Center | Right) splitter with draggable vertical handles.
        self.main_split = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.main_split.setChildrenCollapsible(False)
        self.main_split.setHandleWidth(6)
        self.main_split.addWidget(self.left)
        self.main_split.addWidget(self.center_right_split)
        self.main_split.setStretchFactor(0, 0)
        self.main_split.setStretchFactor(1, 1)

        root.addWidget(self.main_split, 1, 0, 1, 3)

        # auto-resize handled by AutoResizeText

        self._wire_actions()
        self._refresh_tag_pref_options()
        self._load_from_settings()
        self._update_slot_sources()
        self._refresh_library_ui()
        self._set_legacy_controls_visible(False)
        self._apply_theme()
        self._resize_all_text_slots()
        self._apply_label_metrics()
        self._apply_left_panel_width()
        self._apply_max_window_size()
        QtCore.QTimer.singleShot(0, self._restore_window_geometry_once)
        app = QtWidgets.QApplication.instance()
        if app is not None:
            app.installEventFilter(self)

    def _apply_max_window_size(self):
        screen = self.screen()
        if screen is None:
            screen = QtWidgets.QApplication.primaryScreen()
        if screen is None:
            return
        geom = screen.availableGeometry()
        self.setMaximumSize(geom.size())

    def _section_divider(self) -> QtWidgets.QFrame:
        line = QtWidgets.QFrame()
        line.setObjectName("sectionDivider")
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Plain)
        line.setFixedHeight(2)
        line.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        return line

    def _restore_window_geometry_once(self):
        if self._geometry_restored:
            return
        self._geometry_restored = True
        s = self.core.settings
        restored = False

        encoded = s.get("window_geometry_qt")
        if isinstance(encoded, str) and encoded.strip():
            try:
                data = QtCore.QByteArray.fromBase64(encoded.encode("ascii"))
                if not data.isEmpty():
                    restored = bool(self.restoreGeometry(data))
            except Exception:
                restored = False

        if not restored:
            geom = s.get("window_geometry")
            if isinstance(geom, str) and "x" in geom:
                try:
                    w, h = geom.lower().split("x", 1)
                    self.resize(int(w), int(h))
                    restored = True
                except Exception:
                    restored = False

        if not restored:
            self.resize(1200, 820)
        state = str(s.get("window_state", "normal")).lower()
        if state == "maximized":
            self.showMaximized()

    def showEvent(self, event):
        super().showEvent(event)
        self._apply_max_window_size()
        self._apply_left_panel_width()

    def _apply_left_panel_width(self):
        # Keep left panel readable while allowing manual splitter resize.
        try:
            max_text = self._max_category_text_width()
            if max_text <= 0:
                max_text = 250
            pref_width = max_text + 90
            self.left.setMinimumWidth(0)
            max_limit = getattr(QtWidgets, "QWIDGETSIZE_MAX", 16777215)
            self.left.setMaximumWidth(max_limit)
            if hasattr(self, "main_split"):
                sizes = self.main_split.sizes()
                if not sizes or len(sizes) < 2 or sizes[0] < 80:
                    total = max(self.width(), pref_width + 700)
                    left_w = max(220, min(420, pref_width))
                    self.main_split.setSizes([left_w, max(300, total - left_w)])
        except Exception:
            pass

    def _set_legacy_controls_visible(self, visible: bool):
        widgets = [
            getattr(self, "lbl_action_cat", None),
            getattr(self, "lbl_clothes_cat", None),
            getattr(self, "lbl_composition_cat", None),
            getattr(self, "lbl_i2v_cat", None),
            getattr(self, "action_cat", None),
            getattr(self, "clothes_cat", None),
            getattr(self, "composition_cat", None),
            getattr(self, "i2v_cat", None),
            getattr(self, "lock_action", None),
            getattr(self, "lock_clothes", None),
            getattr(self, "lock_composition", None),
            getattr(self, "lock_i2v", None),
            getattr(self, "_gen_frame", None),
            getattr(self, "lbl_excl_action", None),
            getattr(self, "excl_action_filter", None),
            getattr(self, "excl_action", None),
            getattr(self, "lbl_excl_clothes", None),
            getattr(self, "excl_clothes_filter", None),
            getattr(self, "excl_clothes", None),
            getattr(self, "lbl_excl_composition", None),
            getattr(self, "excl_composition_filter", None),
            getattr(self, "excl_composition", None),
            getattr(self, "lbl_excl_i2v", None),
            getattr(self, "excl_i2v_filter", None),
            getattr(self, "excl_i2v", None),
        ]
        for w in widgets:
            if w is not None:
                w.setVisible(visible)

    def _max_category_text_width(self) -> int:
        width = 0
        for ctrl in (self.dynamic_slot_controls or {}).values():
            btn = ctrl.get("cat_btn")
            list_widget = ctrl.get("cat_list")
            if not btn or not list_widget:
                continue
            fm = btn.fontMetrics()
            for i in range(list_widget.count()):
                item = list_widget.item(i)
                if item is not None:
                    text = item.text()
                    if text:
                        width = max(width, fm.horizontalAdvance(text))
        return width

    def _ensure_slot_settings(self):
        slots = self.core.settings.get("slots")
        if not isinstance(slots, list) or not slots:
            self.core.settings["slots"] = [dict(s) for s in DEFAULT_SLOTS]
            self.core.save_settings()

    @staticmethod
    def _attach_menu_list(menu: QtWidgets.QMenu, list_widget: QtWidgets.QListWidget):
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        list_widget.setUniformItemSizes(True)
        list_widget.setAlternatingRowColors(False)
        list_widget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        container = QtWidgets.QWidget(menu)
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        layout.addWidget(list_widget)
        action = QtWidgets.QWidgetAction(menu)
        action.setDefaultWidget(container)
        menu.addAction(action)

    @staticmethod
    def _on_menu_about_to_hide(menu: QtWidgets.QMenu, button: QtWidgets.QPushButton):
        if button is None:
            return
        button.setChecked(False)
        try:
            pos = button.mapFromGlobal(QtGui.QCursor.pos())
            over_button = button.rect().contains(pos)
        except Exception:
            over_button = False
        # If the menu hid because user clicked the same button, suppress immediate reopen.
        if over_button:
            button.setProperty("_suppress_next_menu_toggle", True)

    @staticmethod
    def _toggle_menu(menu: QtWidgets.QMenu, button: QtWidgets.QPushButton):
        if bool(button.property("_suppress_next_menu_toggle")):
            button.setProperty("_suppress_next_menu_toggle", False)
            button.setChecked(False)
            return
        if menu.isVisible():
            menu.close()
            button.setChecked(False)
            return
        button.setChecked(True)
        pos = button.mapToGlobal(QtCore.QPoint(0, button.height()))
        menu.popup(pos)

    @staticmethod
    def _coerce_list(value, default: str) -> list[str]:
        if isinstance(value, list):
            out = [str(v) for v in value if str(v)]
            return out or [default]
        if isinstance(value, str) and value.strip():
            return [value]
        return [default]

    @staticmethod
    def _selected_list(list_widget: QtWidgets.QListWidget) -> list[str]:
        out = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                out.append(item.text())
        return out

    @staticmethod
    def _set_list_items(list_widget: QtWidgets.QListWidget, items: list[str], selected: set[str]):
        blocker = QtCore.QSignalBlocker(list_widget)
        try:
            list_widget.clear()
            for text in items:
                item = QtWidgets.QListWidgetItem(text, list_widget)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Checked if text in selected else QtCore.Qt.Unchecked)
        finally:
            del blocker

    def _update_tag_pref_button(self):
        if not self.tag_pref_selected or "All" in self.tag_pref_selected:
            self.tag_pref.setText("All")
            return
        vals = sorted(self.tag_pref_selected)
        if len(vals) <= 2:
            self.tag_pref.setText(", ".join(vals))
        else:
            self.tag_pref.setText(f"{len(vals)} selected")

    def _update_category_button(self, kind: str):
        if kind == "action":
            btn = self.action_cat
            selected = self.action_cat_selected
        elif kind == "clothes":
            btn = self.clothes_cat
            selected = self.clothes_cat_selected
        elif kind == "composition":
            btn = self.composition_cat
            selected = self.composition_cat_selected
        else:
            btn = self.i2v_cat
            selected = self.i2v_cat_selected

        if not selected or "Any" in selected:
            btn.setText("Any")
            return
        if "None" in selected:
            btn.setText("None")
            return
        vals = sorted(selected)
        if len(vals) <= 2:
            btn.setText(", ".join(vals))
        else:
            btn.setText(f"{len(vals)} selected")

    def _on_tag_pref_item_changed(self, item: QtWidgets.QListWidgetItem):
        if item is None:
            return
        list_widget = self.tag_pref_list
        text = item.text()
        checked = item.checkState() == QtCore.Qt.Checked
        blocker = QtCore.QSignalBlocker(list_widget)
        try:
            if text == "All":
                if checked:
                    for i in range(list_widget.count()):
                        other = list_widget.item(i)
                        if other.text() != "All":
                            other.setCheckState(QtCore.Qt.Unchecked)
                else:
                    if not any(
                        list_widget.item(i).checkState() == QtCore.Qt.Checked
                        for i in range(list_widget.count())
                        if list_widget.item(i).text() != "All"
                    ):
                        item.setCheckState(QtCore.Qt.Checked)
            else:
                if checked:
                    for i in range(list_widget.count()):
                        other = list_widget.item(i)
                        if other.text() == "All":
                            other.setCheckState(QtCore.Qt.Unchecked)
                else:
                    if not any(
                        list_widget.item(i).checkState() == QtCore.Qt.Checked
                        for i in range(list_widget.count())
                        if list_widget.item(i).text() != "All"
                    ):
                        for i in range(list_widget.count()):
                            other = list_widget.item(i)
                            if other.text() == "All":
                                other.setCheckState(QtCore.Qt.Checked)
        finally:
            del blocker

        self.tag_pref_selected = set(self._selected_list(list_widget))
        if not self.tag_pref_selected:
            self.tag_pref_selected = {"All"}
        self._update_tag_pref_button()
        self._write_to_settings()

    def _on_category_item_changed(self, kind: str, item: QtWidgets.QListWidgetItem):
        if item is None:
            return
        if kind == "action":
            list_widget = self.action_cat_list
            selected = self.action_cat_selected
        elif kind == "clothes":
            list_widget = self.clothes_cat_list
            selected = self.clothes_cat_selected
        elif kind == "composition":
            list_widget = self.composition_cat_list
            selected = self.composition_cat_selected
        else:
            list_widget = self.i2v_cat_list
            selected = self.i2v_cat_selected

        text = item.text()
        checked = item.checkState() == QtCore.Qt.Checked
        blocker = QtCore.QSignalBlocker(list_widget)
        try:
            if text in ("Any", "None"):
                if checked:
                    for i in range(list_widget.count()):
                        other = list_widget.item(i)
                        if other.text() != text:
                            other.setCheckState(QtCore.Qt.Unchecked)
                else:
                    if not any(
                        list_widget.item(i).checkState() == QtCore.Qt.Checked
                        for i in range(list_widget.count())
                        if list_widget.item(i).text() not in ("Any", "None")
                    ):
                        for i in range(list_widget.count()):
                            other = list_widget.item(i)
                            if other.text() == "Any":
                                other.setCheckState(QtCore.Qt.Checked)
            else:
                if checked:
                    for i in range(list_widget.count()):
                        other = list_widget.item(i)
                        if other.text() in ("Any", "None"):
                            other.setCheckState(QtCore.Qt.Unchecked)
                else:
                    if not any(
                        list_widget.item(i).checkState() == QtCore.Qt.Checked
                        for i in range(list_widget.count())
                        if list_widget.item(i).text() not in ("Any", "None")
                    ):
                        for i in range(list_widget.count()):
                            other = list_widget.item(i)
                            if other.text() == "Any":
                                other.setCheckState(QtCore.Qt.Checked)
        finally:
            del blocker

        selected.clear()
        selected.update(self._selected_list(list_widget))
        if not selected:
            selected.add("Any")
        self._update_category_button(kind)
        self._write_to_settings()

    def _change_n_sets(self, delta: int):
        current = self._safe_int(self.n_sets.text(), 1, 50, 3)
        value = max(1, min(50, current + delta))
        self.n_sets.setText(str(value))
        self._write_to_settings()

    def _update_weight_strength_preview(self, value: int):
        try:
            v = int(value)
        except Exception:
            v = int(self.weight_strength.value()) if hasattr(self, "weight_strength") else 0
        if hasattr(self, "lbl_weight_value") and self.lbl_weight_value is not None:
            self.lbl_weight_value.setText(f"{v}%")

    def _wire_actions(self):
        self.btn_generate.clicked.connect(self.on_generate)
        self.btn_copy.clicked.connect(self.copy_output)
        self.btn_save.clicked.connect(self.save_txt)
        self.btn_create.clicked.connect(self.open_create)
        self.btn_assign_tag.clicked.connect(self.open_assign_tag)
        self.btn_reload.clicked.connect(self.on_reload)
        self.btn_manage_slots.clicked.connect(self.open_manage_slots)
        self.btn_customize.clicked.connect(self.open_customise)
        self.btn_clear_action.clicked.connect(lambda: self._clear_slot("ACTIONSTYLE"))
        self.btn_clear_clothes.clicked.connect(lambda: self._clear_slot("CLOTHES"))
        self.btn_clear_composition.clicked.connect(lambda: self._clear_slot("COMPOSITION"))
        self.btn_clear_i2v.clicked.connect(lambda: self._clear_slot("I2V"))

        self.btn_browse_action.clicked.connect(lambda: self.open_browse_slot("actionstyle"))
        self.btn_browse_clothes.clicked.connect(lambda: self.open_browse_slot("clothes"))
        self.btn_browse_composition.clicked.connect(lambda: self.open_browse_slot("composition"))
        self.btn_browse_i2v.clicked.connect(lambda: self.open_browse_slot("i2v"))

        self.btn_clear_excludes.clicked.connect(self.clear_excludes)
        self.btn_reset_repeats.clicked.connect(self.reset_repeats)
        self.btn_n_sets_minus.clicked.connect(lambda: self._change_n_sets(-1))
        self.btn_n_sets_plus.clicked.connect(lambda: self._change_n_sets(1))
        self.btn_rand_action.clicked.connect(lambda: self._randomize_dynamic_slot("actionstyle"))
        self.btn_rand_clothes.clicked.connect(lambda: self._randomize_dynamic_slot("clothes"))
        self.btn_rand_composition.clicked.connect(lambda: self._randomize_dynamic_slot("composition"))
        self.btn_rand_i2v.clicked.connect(lambda: self._randomize_dynamic_slot("i2v"))
        self.weight_strength.valueChanged.connect(self._update_weight_strength_preview)

        self.preset_combo.currentTextChanged.connect(self.apply_preset)

        self.excl_all_filter.textChanged.connect(self._apply_exclude_filter_all)
        self.excl_action_filter.textChanged.connect(lambda: self._apply_exclude_filter("ACTIONSTYLE"))
        self.excl_clothes_filter.textChanged.connect(lambda: self._apply_exclude_filter("CLOTHES"))
        self.excl_composition_filter.textChanged.connect(lambda: self._apply_exclude_filter("COMPOSITION"))
        self.excl_i2v_filter.textChanged.connect(lambda: self._apply_exclude_filter("I2V"))
        for box in [self.action_box, self.clothes_box, self.composition_box, self.i2v_box]:
            box.textChanged.connect(self._on_slot_text_changed)

    def _card(self, title: str) -> QtWidgets.QWidget:
        card = QtWidgets.QGroupBox(title)
        card.setObjectName("card")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        return card

    def _slot_text(self) -> QtWidgets.QPlainTextEdit:
        box = AutoResizeText(min_lines=3, max_lines=10, max_chars=1000)
        box.setObjectName("slot")
        return box

    def _slot_header(self, title_label: QtWidgets.QLabel, src_label: QtWidgets.QLabel) -> QtWidgets.QWidget:
        row = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(title_label)
        layout.addStretch(1)
        src_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        src_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(src_label)
        return row

    def _apply_theme(self):
        c = self.colors
        self._apply_icons()
        self._set_titlebar_color(c.get("topbar", "#111111"), c.get("text", "#ffffff"))

        if self.use_qdarktheme and qdarktheme is not None:
            theme_mode = "light" if self._luma(c.get("panel", "#111111")) > 0.6 else "dark"
            custom_colors = {
                "background": c["panel"],
                "foreground": c["text"],
                "border": c["border"],
                "primary": c["accent"],
                "input.background": c["panel"],
                "list.alternateBackground": c["list_bg"],
                "list.hoverBackground": c["list_select"],
                "primary>selection.background": c["list_select"],
                "primary>list.selectionBackground": c["list_select"],
                "primary>list.inactiveSelectionBackground": c["list_select"],
                "tab.hoverBackground": c["button_hover"],
                "toolbar.background": c["topbar"],
                "toolbar.hoverBackground": c["button_hover"],
                "statusBar.background": c["topbar"],
                "tableSectionHeader.background": c["panel_2"],
                "scrollbar.background": c["panel_2"],
                "scrollbarSlider.background": c["border"],
                "scrollbarSlider.hoverBackground": c["accent"],
                "scrollbarSlider.activeBackground": c["accent"],
                "popupItem.selectionBackground": c["list_select"],
                "popupItem.checkbox.background": c["panel_2"],
                "menubar.selectionBackground": c["button_hover"],
            }
            extra_qss = f"""
            QDialog {{ background: {c['panel_2']}; }}
            QFrame#topbar {{ background: {c['topbar']}; border: 1px solid {c['border']}; border-radius: 10px; }}
            QGroupBox#card {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {c['panel_2']}, stop:1 {c['panel']});
                border: 1px solid {c['border']};
                border-radius: 10px;
                margin-top: 8px;
            }}
            QGroupBox#card::title {{ subcontrol-origin: margin; left: 12px; padding: 0 4px; color: {c['text']}; font-weight: 600; font-size: 14pt; }}
              QLabel#brand {{ color: {c['accent']}; font-family: 'Titillium Web'; font-size: 16pt; font-weight: 700; }}
            QPlainTextEdit#slot, QTextEdit#slot {{ background: {c['panel']}; font-family: 'Consolas'; font-size: 12pt; }}
            QScrollArea#listArea {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 6px; }}
            QWidget#listContainer {{ background: {c['panel']}; }}
            QCheckBox#list_item {{ background: {c['panel']}; }}
            QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus, QTextEdit:focus {{ border: 1px solid {c['accent']}; }}
            QLineEdit:hover, QComboBox:hover, QPlainTextEdit:hover, QTextEdit:hover {{ border: 1px solid {c['accent_2']}; }}
            QPushButton#primary {{ border-radius: 14px; padding: 8px 16px; font-weight: 600; }}
            QPushButton#primary:hover {{ background: {c['button_hover']}; }}
            QPushButton:pressed {{ background: {c['accent']}; }}
              QPushButton#iconSquare {{ border-radius: 6px; padding: 0; min-width: 28px; max-width: 28px; min-height: 28px; max-height: 28px; }}
            QMenu {{ background: {c['panel']}; border: 1px solid {c['border']}; color: {c['text']}; }}
            QMenu::item {{ padding: 6px 12px; background: transparent; }}
            QMenu::item:selected {{ background: {c['list_select']}; }}
            QSplitter::handle {{ background: {c['border']}; }}
            QSplitter::handle:hover {{ background: {c['accent']}; }}
            QFrame#sectionDivider {{ background: {c['border']}; border: none; min-height: 2px; max-height: 2px; }}
            """
            try:
                qdarktheme.setup_theme(
                    theme=theme_mode,
                    corner_shape="rounded",
                    custom_colors=custom_colors,
                    additional_qss=extra_qss,
                )
            except Exception:
                self.use_qdarktheme = False

        if not self.use_qdarktheme:
            style = (
                f"""
                QMainWindow {{ background: {c['panel']}; }}
                QWidget {{ color: {c['text']}; font-family: 'Roboto'; font-size: 12pt; }}
                QFrame#topbar {{ background: {c['topbar']}; border: 1px solid {c['border']}; border-radius: 10px; }}
                QGroupBox#card {{
                    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {c['panel_2']}, stop:1 {c['panel']});
                    border: 1px solid {c['border']};
                    border-radius: 10px;
                    margin-top: 8px;
                }}
                QGroupBox#card::title {{ subcontrol-origin: margin; left: 12px; padding: 0 4px; color: {c['text']}; font-size: 14pt; font-weight: 600; }}
                  QLabel#brand {{ font-size: 16pt; font-weight: 700; color: {c['accent']}; font-family: 'Titillium Web'; }}
                QLabel#muted {{ color: {c['muted']}; font-size: 10pt; }}
                QLabel#status {{ color: {c['muted']}; font-size: 10pt; }}
                QLabel {{ font-size: 11pt; background: transparent; }}
                QPushButton {{ background: {c['button']}; border-radius: 12px; padding: 6px 12px; font-size: 11pt; }}
                QPushButton:hover {{ background: {c['button_hover']}; }}
                QPushButton:pressed {{ background: {c['accent']}; }}
              QPushButton#iconSquare {{ border-radius: 6px; padding: 0; min-width: 28px; max-width: 28px; min-height: 28px; max-height: 28px; }}
                QPushButton#primary {{ border-radius: 14px; padding: 8px 16px; font-weight: 600; }}
                QPushButton#primary:hover {{ background: {c['button_hover']}; }}
                QLineEdit, QComboBox, QPlainTextEdit, QTextEdit {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 6px; font-size: 12pt; }}
                QComboBox {{ padding-left: 6px; }}
                QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus, QTextEdit:focus {{ border: 1px solid {c['accent']}; }}
                QLineEdit:hover, QComboBox:hover, QPlainTextEdit:hover, QTextEdit:hover {{ border: 1px solid {c['accent_2']}; }}
                QPlainTextEdit#slot, QTextEdit#slot {{ background: {c['panel']}; font-family: 'Consolas'; font-size: 12pt; }}
                QListWidget {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 6px; }}
                QListWidget::item:selected {{ background: {c['list_select']}; }}
                QComboBox QAbstractItemView {{ background: {c['panel']}; color: {c['text']}; selection-background-color: {c['list_select']}; }}
                QScrollArea {{ border: none; }}
                QScrollArea#listArea {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 6px; }}
                QScrollArea#listArea QWidget {{ background: {c['panel']}; }}
                QWidget#listContainer {{ background: {c['panel']}; }}
                QCheckBox {{ font-size: 12pt; }}
                QCheckBox#list_item {{ background: {c['panel']}; font-size: 12pt; }}
                QCheckBox::indicator {{ width: 14px; height: 14px; }}
                QCheckBox::indicator:unchecked {{ border: 1px solid {c['border']}; background: {c['panel']}; border-radius: 3px; }}
                QCheckBox::indicator:checked {{ border: 1px solid {c['checkbox_on']}; background: {c['checkbox_on']}; border-radius: 3px; }}
                QMenu {{ background: {c['panel']}; border: 1px solid {c['border']}; color: {c['text']}; }}
                QMenu::item {{ padding: 6px 12px; background: transparent; }}
                QMenu::item:selected {{ background: {c['list_select']}; }}
                QSplitter::handle {{ background: {c['border']}; }}
                QSplitter::handle:hover {{ background: {c['accent']}; }}
                QFrame#sectionDivider {{ background: {c['border']}; border: none; min-height: 2px; max-height: 2px; }}
                QSlider::groove:horizontal {{ background: {c['panel_2']}; height: 6px; border-radius: 3px; }}
                QSlider::sub-page:horizontal {{ background: {c['accent']}; border-radius: 3px; }}
                QSlider::add-page:horizontal {{ background: {c['panel_2']}; border-radius: 3px; }}
                QSlider::handle:horizontal {{ background: {c['accent']}; width: 14px; height: 14px; margin: -6px 0; border-radius: 7px; }}
                QTabWidget::pane {{ border: 1px solid {c['border']}; border-radius: 8px; }}
                QTabBar::tab {{ background: {c['button']}; padding: 6px 12px; border-top-left-radius: 6px; border-top-right-radius: 6px; font-size: 12pt; }}
                QTabBar::tab:selected {{ background: {c['accent']}; color: {c['text']}; }}
                QDialog {{ background: {c['panel_2']}; }}
                QTabWidget {{ background: {c['panel_2']}; }}
                """
            )
            self.setStyleSheet(style)
        self.preset_combo.setCurrentText(self._current_preset_name())
        self._apply_label_metrics()

    def _set_titlebar_color(self, bg_hex: str, text_hex: str):
        self._set_titlebar_color_for(self, bg_hex, text_hex)

    def _apply_titlebar_to(self, widget: QtWidgets.QWidget):
        c = self.colors
        self._set_titlebar_color_for(widget, c.get("topbar", "#111111"), c.get("text", "#ffffff"))

    @staticmethod
    def _set_titlebar_color_for(widget: QtWidgets.QWidget, bg_hex: str, text_hex: str):
        if not sys.platform.startswith("win"):
            return
        try:
            hwnd = int(widget.winId())
        except Exception:
            return
        try:
            color = PromptZoneWindow._hex_to_colorref(bg_hex)
            text = PromptZoneWindow._hex_to_colorref(text_hex)
        except Exception:
            return
        # Try Windows 11+ caption/text color attributes. Fail silently on older OS.
        try:
            DWMWA_CAPTION_COLOR = 35
            DWMWA_TEXT_COLOR = 36
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                wintypes.HWND(hwnd),
                wintypes.DWORD(DWMWA_CAPTION_COLOR),
                ctypes.byref(wintypes.DWORD(color)),
                ctypes.sizeof(wintypes.DWORD),
            )
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                wintypes.HWND(hwnd),
                wintypes.DWORD(DWMWA_TEXT_COLOR),
                ctypes.byref(wintypes.DWORD(text)),
                ctypes.sizeof(wintypes.DWORD),
            )
        except Exception:
            pass

    @staticmethod
    def _hex_to_colorref(hex_color: str) -> int:
        h = hex_color.lstrip("#")
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return (b << 16) | (g << 8) | r

    def _apply_label_metrics(self):
        label_font = QtGui.QFont("Roboto", 11)
        bold_label_font = QtGui.QFont("Roboto", 11, QtGui.QFont.Bold)
        labels = [
            getattr(self, "lbl_sets", None),
            getattr(self, "lbl_tag", None),
            getattr(self, "lbl_excl_tag", None),
            getattr(self, "lbl_weight", None),
            getattr(self, "lbl_action_cat", None),
            getattr(self, "lbl_clothes_cat", None),
            getattr(self, "lbl_composition_cat", None),
            getattr(self, "lbl_i2v_cat", None),
            getattr(self, "lbl_action_slot", None),
            getattr(self, "lbl_clothes_slot", None),
            getattr(self, "lbl_composition_slot", None),
            getattr(self, "lbl_i2v_slot", None),
            getattr(self, "lbl_output", None),
            getattr(self, "lbl_excl_action", None),
            getattr(self, "lbl_excl_clothes", None),
            getattr(self, "lbl_excl_composition", None),
            getattr(self, "lbl_excl_i2v", None),
            getattr(self, "lbl_excl_all", None),
            getattr(self, "kpi", None),
        ]
        for lbl in labels:
            if lbl is None:
                continue
            lbl.setFont(label_font)
            lbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            lbl.setContentsMargins(0, 0, 0, 0)
            lbl.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            lbl.setFixedHeight(18)

        for lbl in [
            getattr(self, "lbl_sets", None),
            getattr(self, "lbl_tag", None),
            getattr(self, "lbl_excl_tag", None),
            getattr(self, "lbl_weight", None),
            getattr(self, "lbl_action_cat", None),
            getattr(self, "lbl_clothes_cat", None),
            getattr(self, "lbl_composition_cat", None),
            getattr(self, "lbl_i2v_cat", None),
            getattr(self, "lbl_action_slot", None),
            getattr(self, "lbl_clothes_slot", None),
            getattr(self, "lbl_composition_slot", None),
            getattr(self, "lbl_i2v_slot", None),
            getattr(self, "lbl_output", None),
            getattr(self, "lbl_excl_action", None),
            getattr(self, "lbl_excl_clothes", None),
            getattr(self, "lbl_excl_composition", None),
            getattr(self, "lbl_excl_i2v", None),
            getattr(self, "lbl_excl_all", None),
        ]:
            if lbl is not None:
                lbl.setFont(bold_label_font)
        for lbl in (getattr(self, "dynamic_category_labels", {}) or {}).values():
            if lbl is not None:
                lbl.setFont(bold_label_font)
        for lbl in (getattr(self, "dynamic_slot_labels", {}) or {}).values():
            if lbl is not None:
                lbl.setFont(bold_label_font)

    def _load_from_settings(self):
        s = self.core.settings
        self.n_sets.setText(str(s.get("n_sets", 3)))
        self.weight_strength.setValue(int(float(s.get("weight_strength", 0.65)) * 100))

        self.lock_action.setChecked(bool(s.get("lock_action", False)))
        self.lock_clothes.setChecked(bool(s.get("lock_clothes", False)))
        self.lock_composition.setChecked(bool(s.get("lock_composition", False)))
        self.lock_i2v.setChecked(bool(s.get("lock_i2v", False)))
        self.skip_minimized.setChecked(bool(s.get("skip_minimized", False)))
        self.append_output.setChecked(bool(s.get("append_output", False)))
        self.avoid_repeats.setChecked(bool(s.get("avoid_repeats", True)))
        self.one_per_folder.setChecked(bool(s.get("only_one_per_folder", False)))

        preset = s.get("theme_preset")
        if isinstance(preset, str) and preset in THEME_PRESETS:
            self.preset_combo.setCurrentText(preset)

        self.gen_action.setChecked(bool(s.get("gen_action", True)))
        self.gen_clothes.setChecked(bool(s.get("gen_clothes", True)))
        self.gen_composition.setChecked(bool(s.get("gen_composition", True)))
        self.gen_i2v.setChecked(bool(s.get("gen_i2v", True)))

        last_output = s.get("last_output_text", "")
        if last_output:
            self.output_box.setPlainText(last_output)

        last_texts = s.get("last_slot_texts")
        if not isinstance(last_texts, dict):
            last_texts = {}
        legacy_text_keys = {
            "actionstyle": "last_action_text",
            "clothes": "last_clothes_text",
            "composition": "last_composition_text",
            "i2v": "last_i2v_text",
        }
        for slot_id, key in legacy_text_keys.items():
            legacy_text = s.get(key, "")
            if legacy_text and slot_id not in last_texts:
                last_texts[slot_id] = legacy_text
        s["last_slot_texts"] = last_texts

        last_sources = s.get("last_slot_sources")
        if not isinstance(last_sources, dict):
            last_sources = {}
        legacy_source_keys = {
            "actionstyle": "last_action_source",
            "clothes": "last_clothes_source",
            "composition": "last_composition_source",
            "i2v": "last_i2v_source",
        }
        for slot_id, key in legacy_source_keys.items():
            legacy_src = s.get(key, "")
            if legacy_src and slot_id not in last_sources:
                last_sources[slot_id] = legacy_src
        self.last_dynamic_sources = dict(last_sources)
        s["last_slot_sources"] = dict(last_sources)

    def _write_to_settings(self):
        s = self.core.settings
        s["n_sets"] = self._safe_int(self.n_sets.text(), 1, 50, 3)
        tag_sel = self._selected_list(self.tag_pref_list)
        s["tag_pref"] = tag_sel if tag_sel else ["All"]
        s["weight_strength"] = float(self.weight_strength.value()) / 100.0
        s["skip_minimized"] = self.skip_minimized.isChecked()
        s["append_output"] = self.append_output.isChecked()
        s["avoid_repeats"] = self.avoid_repeats.isChecked()
        s["only_one_per_folder"] = self.one_per_folder.isChecked()
        s["excluded_tags"] = sorted(self.excluded_tags)
        slot_settings = {}
        for slot_id, ctrl in (self.dynamic_slot_controls or {}).items():
            list_widget = ctrl.get("cat_list")
            cat_sel = self._selected_list(list_widget) if list_widget else ["Any"]
            slot_settings[slot_id] = {
                "category": cat_sel if cat_sel else ["Any"],
                "excluded": [
                    name
                    for name, cb in self.dynamic_excl_vars.get(slot_id, {}).get("items", {}).items()
                    if cb.isChecked()
                ],
                "lock": ctrl.get("lock").isChecked() if ctrl.get("lock") else False,
                "gen": ctrl.get("gen").isChecked() if ctrl.get("gen") else True,
            }
        s["slot_settings"] = slot_settings
        for k in self._legacy_slot_setting_keys():
            s.pop(k, None)
        s["theme_colors"] = dict(self.colors)
        s["theme_preset"] = self._current_preset_name()
        s["window_geometry"] = f"{self.width()}x{self.height()}"
        try:
            s["window_geometry_qt"] = bytes(self.saveGeometry().toBase64()).decode("ascii")
        except Exception:
            pass
        s["window_state"] = "maximized" if self.isMaximized() else "normal"
        self.core.save_settings()

    def _refresh_library_ui(self):
        self._refresh_tag_pref_options()
        self._refresh_excluded_tags()
        self._build_exclude_search_cache()
        self._set_legacy_controls_visible(False)
        self._rebuild_dynamic_slots()
        self._apply_label_metrics()
        self._apply_left_panel_width()
        self._apply_icons()
        if hasattr(self, "excl_all_filter"):
            self._apply_exclude_filter_all()

        parts = []
        for slot in self.core.get_slots():
            label = str(slot.get("label") or slot.get("id") or "Slot").upper()
            prefix = str(slot.get("prefix") or "").strip()
            folders = self.core.folders_by_prefix(prefix) if prefix else []
            files = sum(
                1
                for folder in folders
                for f in folder.iterdir()
                if f.is_file() and f.suffix.lower() in PROMPT_TEXT_EXTENSIONS
            )
            parts.append(f"{label}: {len(folders)} folders / {files} files")
        kpi = "    |    ".join(parts) if parts else "No slots configured."
        self.kpi.setText(kpi)
        self._status("Library refreshed.")

    def open_browse(self, kind: str):
        kind = (kind or "").upper().strip()
        slot_map = {
            "ACTIONSTYLE": "actionstyle",
            "CLOTHES": "clothes",
            "COMPOSITION": "composition",
            "I2V": "i2v",
        }
        slot_id = slot_map.get(kind, "")
        if not slot_id:
            return
        self.open_browse_slot(slot_id)

    def open_browse_slot(self, slot_id: str):
        self._write_to_settings()
        slot = next((s for s in self.core.get_slots() if s.get("id") == slot_id), None)
        if not slot:
            return
        prefix = str(slot.get("prefix") or "").strip()
        if not prefix:
            self._status(f"{slot.get('label', slot_id)} has no prefix.")
            return
        label = str(slot.get("label") or slot_id).strip() or slot_id
        dlg = BrowseDialog(self, self.core, label, prefix=prefix)
        res = dlg.exec()
        if res not in (1, 2):
            return
        text = dlg.selected_text
        lock = res == 2
        if not slot_id:
            return
        ctrl = self.dynamic_slot_controls.get(slot_id, {})
        lock_cb = ctrl.get("lock")
        if lock_cb is not None and lock_cb.isChecked():
            self._status(f"{label} is locked.")
            return
        box = self.dynamic_slot_boxes.get(slot_id)
        if box is not None:
            box.setPlainText(text)
            self._queue_resize_text()
        if lock and lock_cb is not None:
            lock_cb.setChecked(True)
        self._write_to_settings()

    def on_generate(self):
        self._write_to_settings()
        s = self.core.settings
        prev_sources = dict(getattr(self, "last_dynamic_sources", {}) or {})
        try:
            slots = self.core.get_slots()
            slot_texts = {slot_id: box.toPlainText().strip() for slot_id, box in self.dynamic_slot_boxes.items()}
            new_map, sources_map, out = self.core.generate_slots(
                slots, slot_texts, skip_minimized=bool(s.get("skip_minimized", False))
            )
        except Exception as e:
            self._status(str(e))
            return
        for slot_id, box in self.dynamic_slot_boxes.items():
            if slot_id in new_map:
                box.setPlainText(new_map[slot_id])

        merged_sources = {}
        for slot_id in self.dynamic_slot_boxes.keys():
            src = sources_map.get(slot_id, "")
            if not src:
                src = prev_sources.get(slot_id, "")
            merged_sources[slot_id] = src
        self.last_dynamic_sources = merged_sources

        display_out = self._rebuild_output_from_fields()
        self.output_box.setPlainText(display_out)
        self._update_slot_sources()
        s = self.core.settings
        s["last_output_text"] = display_out
        s["last_slot_texts"] = {slot_id: box.toPlainText() for slot_id, box in self.dynamic_slot_boxes.items()}
        s["last_slot_sources"] = dict(self.last_dynamic_sources)
        self.core.save_settings()
        self._refresh_library_ui()
        self._status("Randomized new prompt set.")
        QtCore.QTimer.singleShot(0, self._resize_all_text_slots)

    def copy_output(self):
        txt = self.output_box.toPlainText().strip()
        if not txt:
            return
        QtWidgets.QApplication.clipboard().setText(txt)
        self._status("Output copied.")

    def save_txt(self):
        self._write_to_settings()
        txt = self.output_box.toPlainText().strip()
        if not txt:
            return
        try:
            self.core.output_path.write_text(txt, encoding="utf-8")
            self._status(f"Saved: {self.core.output_path.name}")
        except Exception as e:
            self._status(f"Save failed: {e}")

    def on_reload(self):
        self._write_to_settings()
        self.core.reload_library()
        self._refresh_library_ui()
        self._status("Folders reloaded.")

    def clear_excludes(self):
        for data in (self.dynamic_excl_vars or {}).values():
            for cb in data.get("items", {}).values():
                cb.setChecked(False)
        self._clear_excluded_tags(silent=True)
        self._write_to_settings()
        self._refresh_library_ui()
        self._status("Excludes cleared.")

    def reset_repeats(self):
        self.core.used_action_files.clear()
        self.core.used_clothes_files.clear()
        self.core.used_composition_files.clear()
        self.core.used_i2v_files.clear()
        self._refresh_library_ui()
        self._status("Repeat history cleared.")

    def open_create(self):
        dlg = CreateDialog(self)
        dlg.exec()

    def open_assign_tag(self):
        dlg = AssignTagDialog(self)
        dlg.exec()

    def open_manage_slots(self):
        dlg = ManageSlotsDialog(self)
        dlg.exec()
        self._refresh_library_ui()
        self._status("Slots updated.")

    def _refresh_tag_pref_options(self):
        tags = self.core.all_tags()
        items = ["All"] + tags
        current = self._coerce_list(self.core.settings.get("tag_pref", "All"), "All")
        selected = set([c for c in current if c in items])
        if not selected or "All" in selected:
            selected = {"All"}
        self.tag_pref_selected = set(selected)
        self._set_list_items(self.tag_pref_list, items, self.tag_pref_selected)
        self._update_tag_pref_button()

    def _update_exclude_tag_tooltip(self):
        if not hasattr(self, "btn_excl_tag"):
            return
        if not self.excluded_tags:
            self.btn_excl_tag.setToolTip("Exclude tags from random generation")
        else:
            tags = ", ".join(sorted(self.excluded_tags))
            self.btn_excl_tag.setToolTip(f"Excluded tags: {tags}")

    def _refresh_excluded_tags(self):
        tags = set(self.core.all_tags())
        if tags:
            self.excluded_tags = {t for t in self.excluded_tags if t in tags}
        else:
            self.excluded_tags = set()
        self._update_exclude_tag_tooltip()

    def _toggle_exclude_tag_menu(self):
        if bool(self.btn_excl_tag.property("_suppress_next_menu_toggle")):
            self.btn_excl_tag.setProperty("_suppress_next_menu_toggle", False)
            self.btn_excl_tag.setChecked(False)
            return
        if self.excl_tag_menu.isVisible():
            self.excl_tag_menu.close()
            self.btn_excl_tag.setChecked(False)
            return
        self._refresh_exclude_tag_menu()
        self.btn_excl_tag.setChecked(True)
        pos = self.btn_excl_tag.mapToGlobal(QtCore.QPoint(0, self.btn_excl_tag.height()))
        self.excl_tag_menu.popup(pos)

    def _on_excl_tag_menu_hide(self):
        if hasattr(self, "btn_excl_tag") and hasattr(self, "excl_tag_menu"):
            self._on_menu_about_to_hide(self.excl_tag_menu, self.btn_excl_tag)

    def _refresh_exclude_tag_menu(self):
        self.excl_tag_menu.clear()
        tags = self.core.all_tags()
        if not tags:
            act = self.excl_tag_menu.addAction("No tags available")
            act.setEnabled(False)
            return
        container = QtWidgets.QWidget(self.excl_tag_menu)
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        list_widget = QtWidgets.QListWidget(container)
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        list_widget.setUniformItemSizes(True)
        list_widget.setAlternatingRowColors(False)
        list_widget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        for tag in tags:
            item = QtWidgets.QListWidgetItem(tag, list_widget)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked if tag in self.excluded_tags else QtCore.Qt.Unchecked)

        def on_item_changed(item: QtWidgets.QListWidgetItem):
            checked = item.checkState() == QtCore.Qt.Checked
            self._toggle_excluded_tag(item.text(), checked)

        list_widget.itemChanged.connect(on_item_changed)

        btn_clear = QtWidgets.QPushButton("Clear tag excludes", container)
        btn_clear.clicked.connect(self._clear_excluded_tags)

        layout.addWidget(list_widget)
        layout.addWidget(btn_clear)

        # Size hint: show up to ~10 rows without growing too tall
        row_h = list_widget.sizeHintForRow(0) if list_widget.count() else 20
        max_h = max(160, min(360, row_h * min(10, list_widget.count()) + 6))
        list_widget.setMinimumWidth(220)
        list_widget.setMaximumHeight(max_h)

        action = QtWidgets.QWidgetAction(self.excl_tag_menu)
        action.setDefaultWidget(container)
        self.excl_tag_menu.addAction(action)

    def _toggle_excluded_tag(self, tag: str, checked: bool):
        if checked:
            self.excluded_tags.add(tag)
        else:
            self.excluded_tags.discard(tag)
        self._update_exclude_tag_tooltip()
        self._write_to_settings()

    def _clear_excluded_tags(self, silent: bool = False):
        if not self.excluded_tags:
            return
        self.excluded_tags.clear()
        self._update_exclude_tag_tooltip()
        self._write_to_settings()
        if not silent:
            self._status("Tag excludes cleared.")

    def open_customise(self):
        def apply_colors(new_colors: dict):
            self.colors.update(new_colors)
            self.core.settings["theme_colors"] = dict(self.colors)
            self.core.save_settings()
            self._apply_theme()

        dlg = ThemeDialog(self, self.colors, apply_colors, self._current_preset_name())
        dlg.exec()
        self._status("Theme updated.")

    def apply_preset(self, name: str):
        preset = THEME_PRESETS.get(name)
        if not preset:
            return
        self.colors.update(preset)
        self.core.settings["theme_colors"] = dict(self.colors)
        self.core.settings["theme_preset"] = name
        self.core.save_settings()
        self._apply_theme()

    def closeEvent(self, event: QtGui.QCloseEvent):
        self._write_to_settings()
        super().closeEvent(event)

    def _status(self, msg: str):
        if self.status_line:
            self.status_line.setText(msg)
            if self._status_timer is not None:
                self._status_timer.stop()
            if self._status_anim is not None:
                self._status_anim.stop()
            if self._status_effect is not None:
                self._status_effect.setOpacity(1.0)
            if self._status_timer is not None:
                self._status_timer.start(2500)

    def _fade_status(self):
        if self._status_effect is None:
            return
        self._status_anim = QtCore.QPropertyAnimation(self._status_effect, b"opacity", self)
        self._status_anim.setDuration(500)
        self._status_anim.setStartValue(self._status_effect.opacity())
        self._status_anim.setEndValue(0.35)
        self._status_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self._status_anim.start()

    @staticmethod
    def _safe_int(v, lo, hi, fallback):
        try:
            x = int(v)
            return max(lo, min(hi, x))
        except Exception:
            return fallback

    @staticmethod
    def _legacy_slot_setting_keys() -> list[str]:
        return [
            "action_category",
            "clothes_category",
            "composition_category",
            "i2v_category",
            "excluded_action",
            "excluded_clothes",
            "excluded_composition",
            "excluded_i2v",
            "lock_action",
            "lock_clothes",
            "lock_composition",
            "lock_i2v",
            "gen_action",
            "gen_clothes",
            "gen_composition",
            "gen_i2v",
            "last_action_text",
            "last_clothes_text",
            "last_composition_text",
            "last_i2v_text",
            "last_action_source",
            "last_clothes_source",
            "last_composition_source",
            "last_i2v_source",
        ]

    def _queue_resize_text(self, *args):
        return

    def _resize_text_widget(self, widget: QtWidgets.QPlainTextEdit, min_lines=3, max_lines=24):
        return

    def _resize_all_text_slots(self):
        return

    def _on_slot_text_changed(self):
        if getattr(self, "_updating_output", False):
            return
        self._updating_output = True
        try:
            out = self._rebuild_output_from_fields()
            if self.output_box.toPlainText() != out:
                self.output_box.setPlainText(out)
        finally:
            self._updating_output = False

    def _compact_source(self, text: str) -> str:
        parts = [p.strip() for p in (text or "").split(DIVIDER) if p.strip()]
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0]
        return f"{parts[0]} (+{len(parts) - 1})"

    def _update_slot_sources(self):
        sources = dict(getattr(self, "last_dynamic_sources", {}) or {})

        for slot_id, lbl in self.dynamic_slot_sources.items():
            lbl.setText(self._compact_source(sources.get(slot_id, "")))

        # Output source label is hidden; skip composing the status text.

    def _clear_slot(self, kind: str):
        kind = kind.upper()
        slot_map = {
            "ACTIONSTYLE": "actionstyle",
            "CLOTHES": "clothes",
            "COMPOSITION": "composition",
            "I2V": "i2v",
        }
        slot_id = slot_map.get(kind)
        if not slot_id:
            return
        box = self.dynamic_slot_boxes.get(slot_id)
        if box:
            box.clear()
        if slot_id == "actionstyle":
            self.core.last_action_sources = ""
        elif slot_id == "clothes":
            self.core.last_clothes_sources = ""
        elif slot_id == "composition":
            self.core.last_composition_sources = ""
        elif slot_id == "i2v":
            self.core.last_i2v_sources = ""
        if hasattr(self, "last_dynamic_sources"):
            self.last_dynamic_sources[slot_id] = ""
        self._update_slot_sources()
        out = self._rebuild_output_from_fields()
        self.output_box.setPlainText(out)
        s = self.core.settings
        s["last_output_text"] = self.output_box.toPlainText()
        s["last_slot_texts"] = {sid: box.toPlainText() for sid, box in self.dynamic_slot_boxes.items()}
        s["last_slot_sources"] = dict(getattr(self, "last_dynamic_sources", {}) or {})
        self.core.save_settings()

    def _randomize_slot(self, kind: str):
        kind = kind.upper()
        slot_map = {
            "ACTIONSTYLE": "actionstyle",
            "CLOTHES": "clothes",
            "COMPOSITION": "composition",
            "I2V": "i2v",
        }
        slot_id = slot_map.get(kind)
        if not slot_id:
            return
        self._randomize_dynamic_slot(slot_id)
        self._status(f"{kind} randomized.")

    def _rebuild_output_from_fields(self) -> str:
        try:
            n = max(1, int(self.core.settings.get("n_sets", 3)))
        except Exception:
            n = 1
        skip_minimized = bool(self.core.settings.get("skip_minimized", False))

        def split_sets(text: str) -> list[str]:
            t = (text or "").strip()
            if not t:
                return [""] * n
            parts = [p.strip() for p in t.split(DIVIDER) if p.strip()]
            if len(parts) == 1:
                return [parts[0]] * n
            if len(parts) < n:
                parts = parts + [parts[-1]] * (n - len(parts))
            return parts[:n]

        def join_sets(arr: list[str]) -> str:
            if n == 1:
                return arr[0] if arr else ""
            return DIVIDER.join([a.strip() for a in arr])

        slots = self.core.get_slots()
        slot_sets = {slot_id: split_sets(box.toPlainText()) for slot_id, box in self.dynamic_slot_boxes.items()}

        out_sets = []
        for idx in range(n):
            parts = []
            for slot in slots:
                if not slot.get("enabled", True):
                    continue
                if skip_minimized and slot.get("minimized", False):
                    continue
                slot_id = slot["id"]
                sets = slot_sets.get(slot_id, [])
                if idx < len(sets) and sets[idx].strip():
                    parts.append(sets[idx])
            out_sets.append("\n".join(parts).strip())
        return join_sets(out_sets)

    def _rebuild_dynamic_slots(self):
        was_updating = getattr(self, "_updating_output", False)
        self._updating_output = True
        try:
            slots = self.core.get_slots()
            self._refresh_browse_buttons(slots)
            default_ids = {"actionstyle", "clothes", "composition", "i2v"}
            default_map = {
                "actionstyle": (self.action_box, self.lbl_action_slot, self.lbl_action_src, self.action_header),
                "clothes": (self.clothes_box, self.lbl_clothes_slot, self.lbl_clothes_src, self.clothes_header),
                "composition": (self.composition_box, self.lbl_composition_slot, self.lbl_composition_src, self.composition_header),
                "i2v": (self.i2v_box, self.lbl_i2v_slot, self.lbl_i2v_src, self.i2v_header),
            }
            last_texts = self.core.settings.get("last_slot_texts", {})
            if not isinstance(last_texts, dict):
                last_texts = {}
            for box, _, _, header in default_map.values():
                box.setVisible(False)
                header.setVisible(False)
            # clear existing
            while self.dynamic_slots_layout.count():
                item = self.dynamic_slots_layout.takeAt(0)
                w = item.widget()
                if w:
                    w.deleteLater()
            self.dynamic_slot_boxes = {}
            self.dynamic_slot_labels = {}
            self.dynamic_slot_sources = {}
            self.last_dynamic_sources = getattr(self, "last_dynamic_sources", {})

            for slot in slots:
                slot_id = slot["id"]
                if slot_id in default_ids:
                    box, label, src, header = default_map.get(slot_id)
                    label.setText(f"{slot['label']} slot")
                    header.setVisible(True)
                    if slot_id in last_texts:
                        box.setPlainText(str(last_texts.get(slot_id, "")))
                else:
                    label = QtWidgets.QLabel(f"{slot['label']} slot")
                    src = QtWidgets.QLabel("")
                    src.setObjectName("muted")
                    header = self._slot_header(label, src)
                    box = self._slot_text()
                    box.textChanged.connect(self._on_slot_text_changed)
                    if slot_id in last_texts:
                        box.setPlainText(str(last_texts.get(slot_id, "")))
                    self.dynamic_slots_layout.addWidget(header)
                    self.dynamic_slots_layout.addWidget(box)
                if slot.get("minimized", False):
                    box.setVisible(False)
                else:
                    box.setVisible(True)
                self.dynamic_slot_boxes[slot_id] = box
                self.dynamic_slot_labels[slot_id] = label
                self.dynamic_slot_sources[slot_id] = src

            self._apply_default_slot_order(slots, default_map)
            self._rebuild_dynamic_left_controls(slots)
            self._rebuild_dynamic_excludes(slots)
        finally:
            self._updating_output = was_updating
        out = self._rebuild_output_from_fields()
        if self.output_box.toPlainText() != out:
            self.output_box.setPlainText(out)

    def _apply_default_slot_order(self, slots: list[dict], default_map: dict):
        center_layout = self.center.layout()
        default_order = ["actionstyle", "clothes", "composition", "i2v"]
        ordered = [s["id"] for s in slots if s.get("id") in default_map]
        for slot_id in default_order:
            if slot_id not in ordered and slot_id in default_map:
                ordered.append(slot_id)

        for slot_id in default_order:
            pair = default_map.get(slot_id)
            if not pair:
                continue
            box, _, _, header = pair
            center_layout.removeWidget(header)
            center_layout.removeWidget(box)

        insert_at = 1  # keep KPI at index 0
        for slot_id in ordered:
            pair = default_map.get(slot_id)
            if not pair:
                continue
            box, _, _, header = pair
            center_layout.insertWidget(insert_at, header)
            insert_at += 1
            center_layout.insertWidget(insert_at, box)
            insert_at += 1

    def _refresh_browse_buttons(self, slots: list[dict]):
        slots_by_id = {s.get("id"): s for s in slots if isinstance(s, dict)}
        mapping = {
            "actionstyle": (self.btn_browse_action, "ACTIONSTYLE"),
            "clothes": (self.btn_browse_clothes, "CLOTHES"),
            "composition": (self.btn_browse_composition, "COMPOSITION"),
            "i2v": (self.btn_browse_i2v, "I2V"),
        }
        for slot_id, (btn, default_label) in mapping.items():
            slot = slots_by_id.get(slot_id)
            if not slot:
                btn.setVisible(False)
                continue
            label = str(slot.get("label") or default_label).strip() or default_label
            btn.setText(f"Browse {label}...")
            btn.setVisible(True)

        while self.dynamic_browse_layout.count():
            item = self.dynamic_browse_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self.dynamic_browse_buttons = {}

        for slot in slots:
            slot_id = str(slot.get("id") or "").strip()
            if not slot_id or slot_id in mapping:
                continue
            label = str(slot.get("label") or slot_id).strip() or slot_id
            btn = QtWidgets.QPushButton(f"Browse {label}...")
            btn.clicked.connect(lambda _, sid=slot_id: self.open_browse_slot(sid))
            icon_color = getattr(
                self,
                "_icon_color",
                "black" if self._luma(self.colors.get("panel", "#111111")) > 0.6 else "white",
            )
            ico = self._icons.get(icon_color, {}).get("browse")
            if ico:
                btn.setIcon(ico)
                btn.setIconSize(QtCore.QSize(16, 16))
            self.dynamic_browse_layout.addWidget(btn, 0, QtCore.Qt.AlignHCenter)
            self.dynamic_browse_buttons[slot_id] = btn

        # Normalize browse button widths to the widest label.
        browse_buttons = [
            self.btn_browse_action,
            self.btn_browse_clothes,
            self.btn_browse_composition,
            self.btn_browse_i2v,
        ] + list((self.dynamic_browse_buttons or {}).values())
        self._normalize_browse_button_widths()
        QtCore.QTimer.singleShot(0, self._normalize_browse_button_widths)

    def _normalize_browse_button_widths(self):
        browse_buttons = [
            self.btn_browse_action,
            self.btn_browse_clothes,
            self.btn_browse_composition,
            self.btn_browse_i2v,
        ] + list((self.dynamic_browse_buttons or {}).values())
        visible = [b for b in browse_buttons if b is not None and b.isVisible()]
        if not visible:
            return
        max_limit = getattr(QtWidgets, "QWIDGETSIZE_MAX", 16777215)
        for b in visible:
            b.setMinimumWidth(0)
            b.setMaximumWidth(max_limit)
            b.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            b.ensurePolished()
            b.adjustSize()
        max_w = max(max(b.minimumSizeHint().width(), b.sizeHint().width()) for b in visible)
        if max_w < 40:
            return
        for b in visible:
            b.setMinimumWidth(max_w)
            b.setMaximumWidth(max_w)
            b.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

    def _rebuild_dynamic_left_controls(self, slots: list[dict]):
        def clear_layout(layout: QtWidgets.QLayout):
            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w:
                    w.deleteLater()
                child_layout = item.layout()
                if child_layout:
                    while child_layout.count():
                        child_item = child_layout.takeAt(0)
                        child_widget = child_item.widget()
                        if child_widget:
                            child_widget.deleteLater()
                    child_layout.deleteLater()

        clear_layout(self.dynamic_category_layout)
        clear_layout(self.dynamic_lock_layout)
        clear_layout(self.dynamic_gen_layout)

        self.dynamic_slot_controls = {}
        self.dynamic_category_labels = {}

        for slot in slots:
            slot_id = slot["id"]
            gen_cb = QtWidgets.QCheckBox(f"Randomize {slot['label']}")
            lock_cb = QtWidgets.QCheckBox(f"Lock {slot['label']}")
            lock_cb.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.dynamic_lock_layout.addWidget(lock_cb, 0, QtCore.Qt.AlignLeft)

            cat_lbl = QtWidgets.QLabel(f"{slot['label']} category")
            cat_lbl.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            self.dynamic_category_layout.addWidget(cat_lbl)
            self.dynamic_category_labels[slot_id] = cat_lbl

            cat_btn = QtWidgets.QPushButton()
            cat_btn.setObjectName("dropdownButton")
            cat_btn.setCheckable(True)
            cat_btn.setAutoDefault(False)
            cat_btn.setDefault(False)
            cat_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            cat_menu = QtWidgets.QMenu(self)
            cat_menu.aboutToHide.connect(lambda m=cat_menu, b=cat_btn: self._on_menu_about_to_hide(m, b))
            cat_list = QtWidgets.QListWidget(cat_menu)
            self._attach_menu_list(cat_menu, cat_list)
            cat_btn.clicked.connect(lambda _, m=cat_menu, b=cat_btn: self._toggle_menu(m, b))
            cat_list.itemChanged.connect(lambda item, sid=slot_id: self._on_dynamic_category_changed(sid, item))
            self.dynamic_category_layout.addWidget(cat_btn)

            rand_btn = QtWidgets.QPushButton()
            rand_btn.setObjectName("iconSquare")
            rand_btn.setFixedSize(26, 26)
            rand_btn.setToolTip(f"Randomize {slot['label']}")
            rand_btn.clicked.connect(lambda _, sid=slot_id: self._randomize_dynamic_slot(sid))

            clear_btn = QtWidgets.QPushButton("Clear")
            clear_btn.setMinimumHeight(26)
            clear_btn.setMinimumWidth(72)
            clear_btn.clicked.connect(lambda _, sid=slot_id: self._clear_dynamic_slot(sid))

            row = QtWidgets.QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(8)
            row.addWidget(gen_cb, 0, QtCore.Qt.AlignLeft)
            row.addStretch(1)
            row.addWidget(rand_btn)
            row.addWidget(clear_btn)
            self.dynamic_gen_layout.addLayout(row)

            self.dynamic_slot_controls[slot_id] = {
                "label": cat_lbl,
                "gen": gen_cb,
                "lock": lock_cb,
                "cat_btn": cat_btn,
                "cat_menu": cat_menu,
                "cat_list": cat_list,
                "rand_btn": rand_btn,
                "clear_btn": clear_btn,
            }

        self._refresh_dynamic_controls()

    def _rebuild_dynamic_excludes(self, slots: list[dict]):
        while self.dynamic_excl_layout.count():
            item = self.dynamic_excl_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self.dynamic_excl_vars = {}
        self.dynamic_excl_filters = {}

        for slot in slots:
            slot_id = slot["id"]
            lbl = QtWidgets.QLabel(f"Exclude {slot['label']}")
            self.dynamic_excl_layout.addWidget(lbl)
            filt = QtWidgets.QLineEdit()
            filt.setPlaceholderText("Filter name...")
            self.dynamic_excl_layout.addWidget(filt)

            area = QtWidgets.QScrollArea()
            area.setObjectName("listArea")
            area.setWidgetResizable(True)
            frame = QtWidgets.QWidget()
            frame.setObjectName("listContainer")
            layout = QtWidgets.QVBoxLayout(frame)
            layout.setContentsMargins(8, 8, 8, 8)
            layout.setSpacing(4)
            area.setWidget(frame)
            area.viewport().setMouseTracking(True)
            area.viewport().installEventFilter(self)
            self.dynamic_excl_layout.addWidget(area, 1)

            self.dynamic_excl_vars[slot_id] = {"layout": layout, "items": {}, "area": area}
            self.dynamic_excl_filters[slot_id] = filt
            filt.textChanged.connect(lambda _, sid=slot_id: self._apply_dynamic_exclude_filter(sid))

        self._refresh_dynamic_excludes()

    def _refresh_dynamic_controls(self):
        slots = {s["id"]: s for s in self.core.get_slots()}
        settings = self.core.settings.get("slot_settings", {})
        for slot_id, ctrl in self.dynamic_slot_controls.items():
            st = settings.get(slot_id, {})
            ctrl["gen"].setChecked(bool(st.get("gen", True)))
            ctrl["lock"].setChecked(bool(st.get("lock", False)))
            # categories
            slot = slots.get(slot_id, {})
            prefix = slot.get("prefix", "")
            items = ["None", "Any"] + [p.name for p in self.core.folders_by_prefix(prefix)]
            selected = set(self._coerce_list(st.get("category", "Any"), "Any"))
            if "None" in selected:
                selected = {"None"}
            elif "Any" in selected or not selected:
                selected = {"Any"}
            self._set_list_items(ctrl["cat_list"], items, selected)
            self._update_category_button_text(ctrl["cat_btn"], selected)

    def _refresh_dynamic_excludes(self):
        settings = self.core.settings.get("slot_settings", {})
        slots = {s["id"]: s for s in self.core.get_slots()}
        for slot_id, data in self.dynamic_excl_vars.items():
            layout = data["layout"]
            items_map = data["items"]
            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w:
                    w.deleteLater()
            items_map.clear()
            slot = slots.get(slot_id, {})
            prefix = slot.get("prefix", "")
            excluded = set(settings.get(slot_id, {}).get("excluded", []) or [])
            for folder in self.core.folders_by_prefix(prefix):
                name = folder.name
                cb = QtWidgets.QCheckBox(name)
                cb.setObjectName("list_item")
                cb.setChecked(name in excluded)
                self._install_exclude_drag(cb)
                items_map[name] = cb
                layout.addWidget(cb)
            layout.addStretch(1)

    def _apply_dynamic_exclude_filter(self, slot_id: str):
        data = self.dynamic_excl_vars.get(slot_id)
        filt = self.dynamic_excl_filters.get(slot_id)
        if not data or not filt:
            return
        query = (filt.text() or "").strip().lower()
        for name, cb in data["items"].items():
            cb.setVisible(query in name.lower())

    def _update_category_button_text(self, btn: QtWidgets.QPushButton, selected: set[str]):
        if not selected or "Any" in selected:
            btn.setText("Any")
            return
        if "None" in selected:
            btn.setText("None")
            return
        vals = sorted(selected)
        if len(vals) <= 2:
            btn.setText(", ".join(vals))
        else:
            btn.setText(f"{len(vals)} selected")

    def _on_dynamic_category_changed(self, slot_id: str, item: QtWidgets.QListWidgetItem):
        ctrl = self.dynamic_slot_controls.get(slot_id)
        if not ctrl:
            return
        list_widget = ctrl["cat_list"]
        text = item.text()
        checked = item.checkState() == QtCore.Qt.Checked
        blocker = QtCore.QSignalBlocker(list_widget)
        try:
            if text in ("Any", "None"):
                if checked:
                    for i in range(list_widget.count()):
                        other = list_widget.item(i)
                        if other.text() != text:
                            other.setCheckState(QtCore.Qt.Unchecked)
                else:
                    if not any(
                        list_widget.item(i).checkState() == QtCore.Qt.Checked
                        for i in range(list_widget.count())
                        if list_widget.item(i).text() not in ("Any", "None")
                    ):
                        for i in range(list_widget.count()):
                            other = list_widget.item(i)
                            if other.text() == "Any":
                                other.setCheckState(QtCore.Qt.Checked)
            else:
                if checked:
                    for i in range(list_widget.count()):
                        other = list_widget.item(i)
                        if other.text() in ("Any", "None"):
                            other.setCheckState(QtCore.Qt.Unchecked)
                else:
                    if not any(
                        list_widget.item(i).checkState() == QtCore.Qt.Checked
                        for i in range(list_widget.count())
                        if list_widget.item(i).text() not in ("Any", "None")
                    ):
                        for i in range(list_widget.count()):
                            other = list_widget.item(i)
                            if other.text() == "Any":
                                other.setCheckState(QtCore.Qt.Checked)
        finally:
            del blocker

        selected = set(self._selected_list(list_widget))
        if not selected:
            selected = {"Any"}
        self._update_category_button_text(ctrl["cat_btn"], selected)
        self._write_to_settings()

    def _clear_dynamic_slot(self, slot_id: str):
        box = self.dynamic_slot_boxes.get(slot_id)
        if box:
            box.clear()
        self._update_slot_sources()
        self._write_to_settings()

    def _randomize_dynamic_slot(self, slot_id: str):
        box = self.dynamic_slot_boxes.get(slot_id)
        if box is None:
            return
        self._write_to_settings()
        slots = self.core.get_slots()
        slot_texts = {sid: b.toPlainText().strip() for sid, b in self.dynamic_slot_boxes.items()}
        s = self.core.settings
        settings = s.get("slot_settings", {})
        saved = {k: dict(v) for k, v in settings.items()} if isinstance(settings, dict) else {}
        temp = {k: dict(v) for k, v in settings.items()} if isinstance(settings, dict) else {}
        for k, st in temp.items():
            if k == slot_id:
                continue
            st["lock"] = True
            if not slot_texts.get(k, "").strip():
                st["gen"] = False
        s["slot_settings"] = temp
        try:
            new_map, sources_map, out = self.core.generate_slots(
                slots, slot_texts, skip_minimized=bool(s.get("skip_minimized", False))
            )
        except Exception as e:
            self._status(str(e))
            return
        finally:
            s["slot_settings"] = saved
        if slot_id in new_map:
            box.setPlainText(new_map[slot_id])
        prev_sources = dict(getattr(self, "last_dynamic_sources", {}) or {})
        prev_sources[slot_id] = sources_map.get(slot_id, "") or prev_sources.get(slot_id, "")
        self.last_dynamic_sources = prev_sources
        display_out = self._rebuild_output_from_fields()
        self.output_box.setPlainText(display_out)
        self._update_slot_sources()
        s = self.core.settings
        s["last_output_text"] = display_out
        s["last_slot_texts"] = {sid: box.toPlainText() for sid, box in self.dynamic_slot_boxes.items()}
        s["last_slot_sources"] = dict(self.last_dynamic_sources)
        self._write_to_settings()

    def _install_exclude_drag(self, cb: QtWidgets.QCheckBox):
        cb.setMouseTracking(True)
        cb.setProperty("exclude_item", True)
        cb.installEventFilter(self)

    def _start_exclude_drag(self, cb: QtWidgets.QCheckBox):
        self._drag_exclude_active = True
        self._drag_exclude_value = not cb.isChecked()
        cb.setChecked(self._drag_exclude_value)

    def _stop_exclude_drag(self):
        self._drag_exclude_active = False
        self._drag_exclude_hovered = None

    def _drag_enter_checkbox(self, cb: QtWidgets.QCheckBox):
        if self._drag_exclude_active:
            cb.setChecked(self._drag_exclude_value)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.ContextMenu:
            if not isinstance(event, QtGui.QContextMenuEvent):
                return False
            target = None
            if isinstance(obj, (QtWidgets.QLineEdit, QtWidgets.QPlainTextEdit, QtWidgets.QTextEdit)):
                target = obj
            else:
                parent = getattr(obj, "parent", None)
                if parent and isinstance(parent, (QtWidgets.QPlainTextEdit, QtWidgets.QTextEdit)):
                    target = parent
            if target is not None:
                # Only customize menus for widgets in the main window (avoid popup crashes).
                try:
                    if target.window() is not self:
                        return False
                except Exception:
                    return False
                try:
                    menu = target.createStandardContextMenu()
                except Exception:
                    menu = None
                if menu is not None:
                    self._theme_menu_icons(menu)
                    try:
                        pos = event.globalPos()
                    except Exception:
                        pos = QtGui.QCursor.pos()
                    if not pos:
                        pos = QtGui.QCursor.pos()
                    try:
                        menu.exec(pos)
                        return True
                    except Exception:
                        # Fall back to default Qt handling if our menu fails
                        return False
        if isinstance(obj, QtWidgets.QCheckBox) and obj.property("exclude_item"):
            if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
                if self._checkbox_text_hit(obj, event.position().toPoint()):
                    self._start_exclude_drag(obj)
                    return True
                return False
            if event.type() == QtCore.QEvent.MouseMove and self._drag_exclude_active:
                if self._checkbox_text_hit(obj, event.position().toPoint()):
                    if obj is not self._drag_exclude_hovered:
                        self._drag_exclude_hovered = obj
                        obj.setChecked(self._drag_exclude_value)
                    return True
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                self._stop_exclude_drag()
                return False
        dynamic_viewports = []
        for data in (self.dynamic_excl_vars or {}).values():
            area = data.get("area")
            if area is not None:
                dynamic_viewports.append(area.viewport())
        legacy_viewports = [
            getattr(self, "excl_action", None),
            getattr(self, "excl_clothes", None),
            getattr(self, "excl_composition", None),
            getattr(self, "excl_i2v", None),
        ]
        legacy_viewports = [w.viewport() for w in legacy_viewports if w is not None]
        if obj in legacy_viewports or obj in dynamic_viewports:
            if event.type() == QtCore.QEvent.MouseMove and self._drag_exclude_active:
                pos = event.position().toPoint()
                child = obj.childAt(pos)
                cb = self._find_checkbox(child)
                if cb and cb is not self._drag_exclude_hovered:
                    if not self._checkbox_text_hit(cb, cb.mapFrom(obj, pos)):
                        return True
                    self._drag_exclude_hovered = cb
                    cb.setChecked(self._drag_exclude_value)
                return True
            if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
                pos = event.position().toPoint()
                child = obj.childAt(pos)
                cb = self._find_checkbox(child)
                if cb:
                    if not self._checkbox_text_hit(cb, cb.mapFrom(obj, pos)):
                        return False
                    self._start_exclude_drag(cb)
                    return True
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                self._stop_exclude_drag()
        return super().eventFilter(obj, event)

    def _find_checkbox(self, widget):
        w = widget
        while w is not None:
            if isinstance(w, QtWidgets.QCheckBox):
                return w
            w = w.parent()
        return None

    def _theme_menu_icons(self, menu: QtWidgets.QMenu):
        menu.setStyle(self._menu_style(QtGui.QColor(self.colors.get("text", "#ffffff"))))
        color = QtGui.QColor(self.colors.get("text", "#ffffff"))
        for action in menu.actions():
            label = action.text().replace("&", "").strip().lower()
            if label in {"select all", "select_all"}:
                action.setIcon(self._make_menu_icon("select_all", color))
                continue
            icon = action.icon()
            if icon is None or icon.isNull():
                continue
            tinted = self._tint_icon(icon, color)
            action.setIcon(tinted)

    @staticmethod
    def _tint_icon(icon: QtGui.QIcon, color: QtGui.QColor) -> QtGui.QIcon:
        size = QtCore.QSize(16, 16)
        pix = icon.pixmap(size)
        if pix.isNull():
            return icon
        img = pix.toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
        r, g, b = color.red(), color.green(), color.blue()
        for y in range(img.height()):
            for x in range(img.width()):
                c = img.pixelColor(x, y)
                if c.alpha() == 0:
                    continue
                alpha = 255 if c.alpha() > 200 else 200
                img.setPixelColor(x, y, QtGui.QColor(r, g, b, alpha))
        tinted = QtGui.QPixmap.fromImage(img)
        out = QtGui.QIcon()
        for state in (
            QtGui.QIcon.Normal,
            QtGui.QIcon.Active,
            QtGui.QIcon.Selected,
            QtGui.QIcon.Disabled,
        ):
            out.addPixmap(tinted, state)
        return out

    @staticmethod
    def _make_menu_icon(kind: str, color: QtGui.QColor) -> QtGui.QIcon:
        size = 16
        pix = QtGui.QPixmap(size, size)
        pix.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pix)
        pen = QtGui.QPen(color)
        pen.setWidth(1)
        painter.setPen(pen)
        if kind == "paste":
            painter.drawRect(3, 4, 10, 9)
            painter.drawRect(5, 2, 6, 3)
            painter.drawLine(5, 7, 11, 7)
            painter.drawLine(5, 9, 11, 9)
        else:
            painter.drawRect(2, 2, 11, 11)
            painter.drawLine(4, 5, 12, 5)
            painter.drawLine(4, 8, 12, 8)
            painter.drawLine(4, 11, 12, 11)
        painter.end()
        return QtGui.QIcon(pix)

    @staticmethod
    def _menu_style(color: QtGui.QColor) -> QtWidgets.QStyle:
        class MenuStyle(QtWidgets.QProxyStyle):
            def __init__(self, icon_color: QtGui.QColor):
                super().__init__()
                self._icon_color = icon_color

            def drawControl(self, element, option, painter, widget=None):
                if element == QtWidgets.QStyle.CE_MenuItem:
                    opt = QtWidgets.QStyleOptionMenuItem(option)
                    icon = opt.icon
                    if icon is not None and not icon.isNull():
                        # Draw item without icon, then paint icon at full opacity.
                        opt.icon = QtGui.QIcon()
                        super().drawControl(element, opt, painter, widget)
                        size = QtCore.QSize(16, 16)
                        tinted = PromptZoneWindow._tint_icon(icon, self._icon_color)
                        pix = tinted.pixmap(size, QtGui.QIcon.Normal)
                        x = opt.rect.left() + 4
                        y = opt.rect.top() + (opt.rect.height() - size.height()) // 2
                        painter.save()
                        painter.setOpacity(1.0)
                        painter.drawPixmap(QtCore.QPoint(x, y), pix)
                        painter.restore()
                        return
                super().drawControl(element, option, painter, widget)

        return MenuStyle(color)

    def _checkbox_text_hit(self, cb: QtWidgets.QCheckBox, pos: QtCore.QPoint) -> bool:
        opt = QtWidgets.QStyleOptionButton()
        cb.initStyleOption(opt)
        indicator = cb.style().subElementRect(QtWidgets.QStyle.SE_CheckBoxIndicator, opt, cb)
        spacing = cb.style().pixelMetric(QtWidgets.QStyle.PM_CheckBoxLabelSpacing, None, cb)
        text_rect = cb.rect()
        text_rect.setLeft(indicator.right() + spacing)
        return text_rect.contains(pos)

    def _current_preset_name(self) -> str:
        stored = self.core.settings.get("theme_preset")
        if isinstance(stored, str) and stored in THEME_PRESETS:
            return stored
        for name, preset in THEME_PRESETS.items():
            if all(self.colors.get(k) == v for k, v in preset.items()):
                return name
        return "Dark"

    def _build_exclude_search_cache(self):
        def folder_text(folder_path: Path) -> str:
            parts = []
            files = sorted(
                [
                    f
                    for f in folder_path.iterdir()
                    if f.is_file() and f.suffix.lower() in PROMPT_TEXT_EXTENSIONS
                ],
                key=lambda p: p.name.lower(),
            )
            for f in files:
                try:
                    text = f.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                if text.strip():
                    parts.append(f.name)
                    parts.append(text)
            return "\n".join(parts)

        self._exclude_search_cache = {"ACTIONSTYLE": {}, "CLOTHES": {}, "COMPOSITION": {}, "I2V": {}}
        for kind, names in (
            ("ACTIONSTYLE", self.core.action_folder_names()),
            ("CLOTHES", self.core.clothes_folder_names()),
            ("COMPOSITION", self.core.composition_folder_names()),
            ("I2V", self.core.i2v_folder_names()),
        ):
            for name in names:
                folder = self.core.library_dir / name
                text = folder_text(folder)
                self._exclude_search_cache[kind][name] = f"{name}\n{text}".lower()

    def _apply_exclude_filter(self, kind: str):
        kind = kind.upper()
        if kind == "ACTIONSTYLE":
            query = (self.excl_action_filter.text() or "").strip().lower()
            mapping = getattr(self, "excl_action_vars", {})
        elif kind == "CLOTHES":
            query = (self.excl_clothes_filter.text() or "").strip().lower()
            mapping = getattr(self, "excl_clothes_vars", {})
        elif kind == "COMPOSITION":
            query = (self.excl_composition_filter.text() or "").strip().lower()
            mapping = getattr(self, "excl_composition_vars", {})
        else:
            query = (self.excl_i2v_filter.text() or "").strip().lower()
            mapping = getattr(self, "excl_i2v_vars", {})

        if not query:
            for cb in mapping.values():
                cb.setVisible(True)
            return

        cache = self._exclude_search_cache.get(kind, {})
        for name, cb in mapping.items():
            hay = cache.get(name, name.lower())
            cb.setVisible(query in hay)

    def _apply_exclude_filter_all(self):
        query = (self.excl_all_filter.text() or "").strip().lower()
        targets = [
            self.excl_action_filter,
            self.excl_clothes_filter,
            self.excl_composition_filter,
            self.excl_i2v_filter,
        ]
        for t in targets:
            t.blockSignals(True)
            t.setText(query)
            t.blockSignals(False)
        self._apply_exclude_filter("ACTIONSTYLE")
        self._apply_exclude_filter("CLOTHES")
        self._apply_exclude_filter("COMPOSITION")
        self._apply_exclude_filter("I2V")
        for slot_id, filt in (self.dynamic_excl_filters or {}).items():
            filt.blockSignals(True)
            filt.setText(query)
            filt.blockSignals(False)
            self._apply_dynamic_exclude_filter(slot_id)

    def _load_custom_fonts(self):
        font_dir = app_root() / FONT_DIR
        if not font_dir.exists():
            font_dir = None
        if font_dir:
            for ttf in font_dir.glob("*.ttf"):
                try:
                    QtGui.QFontDatabase.addApplicationFont(str(ttf))
                except Exception:
                    pass
        roboto_dir = app_root() / ROBOTO_DIR
        if roboto_dir.exists():
            for ttf in roboto_dir.glob("*.ttf"):
                try:
                    QtGui.QFontDatabase.addApplicationFont(str(ttf))
                except Exception:
                    pass

    def _set_window_icon(self):
        ico = app_root() / BRAND_ICON_ICO
        png = app_root() / BRAND_ICON_PATH
        if ico.exists():
            self.setWindowIcon(QtGui.QIcon(str(ico)))
        elif png.exists():
            self.setWindowIcon(QtGui.QIcon(str(png)))

    def _load_icons(self):
        for color in ("black", "white"):
            for key, name in ICON_FILES.items():
                path = self.icon_dir / color / f"{name}.png"
                if not path.exists():
                    continue
                icon = QtGui.QIcon(str(path))
                self._icons[color][key] = icon

    def _apply_icons(self):
        self._icon_color = "black" if self._luma(self.colors.get("panel", "#111111")) > 0.6 else "white"
        icons = self._icons.get(self._icon_color, {})

        def set_btn(btn, key, fallback_key=None):
            ico = icons.get(key)
            if not ico and fallback_key:
                ico = icons.get(fallback_key)
            if ico:
                btn.setIcon(ico)
                btn.setIconSize(QtCore.QSize(16, 16))

        set_btn(self.btn_generate, "generate")
        set_btn(self.btn_copy, "copy")
        set_btn(self.btn_save, "save")
        set_btn(self.btn_create, "create")
        set_btn(self.btn_assign_tag, "assign_tag")
        set_btn(self.btn_manage_slots, "manage_slots", fallback_key="customise")
        set_btn(self.btn_reload, "reload")
        set_btn(self.btn_customize, "customise")
        set_btn(self.btn_browse_action, "browse")
        set_btn(self.btn_browse_clothes, "browse")
        set_btn(self.btn_browse_composition, "browse")
        set_btn(self.btn_browse_i2v, "browse")
        for btn in (getattr(self, "dynamic_browse_buttons", {}) or {}).values():
            set_btn(btn, "browse")
        self._normalize_browse_button_widths()
        set_btn(self.btn_rand_action, "generate")
        set_btn(self.btn_rand_clothes, "generate")
        set_btn(self.btn_rand_composition, "generate")
        set_btn(self.btn_rand_i2v, "generate")
        for ctrl in (self.dynamic_slot_controls or {}).values():
            btn = ctrl.get("rand_btn")
            if btn:
                set_btn(btn, "generate")
        set_btn(self.btn_excl_tag, "exclude_tag")
        set_btn(self.btn_clear_excludes, "clear")
        set_btn(self.btn_reset_repeats, "reset")

    @staticmethod
    def _luma(hex_color: str) -> float:
        h = hex_color.lstrip("#")
        try:
            r = int(h[0:2], 16) / 255.0
            g = int(h[2:4], 16) / 255.0
            b = int(h[4:6], 16) / 255.0
        except Exception:
            return 0.0
        return 0.2126 * r + 0.7152 * g + 0.0722 * b


def main():
    app = QtWidgets.QApplication(sys.argv)
    base_font = QtGui.QFont("Roboto")
    base_font.setPointSize(12)
    app.setFont(base_font)
    window = PromptZoneWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
