"""About / citation / acknowledgment dialog and the top-right "About" toolbar menu.

Kept out of UI.py so the credits live in one place. Every string here is also what the
website and README say; if one changes, change the others.
"""

from __future__ import annotations

from PyQt6 import QtCore, QtGui, QtWidgets

from app_version import APP_TITLE, APP_VERSION

PROJECT_URL = "https://rayana07.github.io/LinePilot/"
REPO_URL = "https://github.com/RayanA07/LinePilot"
ISSUES_URL = "https://github.com/RayanA07/LinePilot/issues"
PAPER_URL = "https://arxiv.org/abs/2609.19377"
PAPER_PDF_URL = "https://arxiv.org/pdf/2609.19377"
CONTACT_EMAIL = "Fengbo.Ma@uga.edu"

PAPER_TITLE = "LinePilot Digitizer: Line-Plot Recovery with Manual and Automatic Calibration"
AUTHORS = (
    "Fengbo Ma*, Rayan Akhtar*, Aakash Joshi*, Xiaoting Li, Haijian Sun, "
    "Zhen Xiang†, Xianyan Chen†, Yiping Zhao†"
)
AFFILIATIONS = "University of Georgia · University of Pennsylvania"
CITATION_TEXT = (
    "Fengbo Ma, Rayan Akhtar, Aakash Joshi, Xiaoting Li, Haijian Sun, Zhen Xiang, "
    "Xianyan Chen, Yiping Zhao. LinePilot Digitizer: Line-Plot Recovery with Manual and "
    "Automatic Calibration. arXiv:2609.19377, 2026. https://arxiv.org/abs/2609.19377"
)
BIBTEX = """@article{ma2026linepilot,
  title   = {LinePilot Digitizer: Line-Plot Recovery with Manual and Automatic Calibration},
  author  = {Ma, Fengbo and Akhtar, Rayan and Joshi, Aakash and Li, Xiaoting and
             Sun, Haijian and Xiang, Zhen and Chen, Xianyan and Zhao, Yiping},
  journal = {arXiv preprint arXiv:2609.19377},
  year    = {2026},
  doi     = {10.48550/arXiv.2609.19377}
}"""

ACKNOWLEDGMENT = (
    "This work was supported by the National Science Foundation (NSF) through the "
    "Pathways to Open-Source Ecosystems (POSE) program, award No. 2518273. The authors "
    "gratefully acknowledge the support, guidance and collaboration of all members of the "
    "SpectraGuru™ development and stakeholder teams.\n\n"
    "LinePilot Digitizer is part of the open-source ecosystem for Raman and SERS "
    "spectroscopy developed in the Zhao lab at the University of Georgia."
)

THIRD_PARTY = (
    ("Tesseract OCR", "Apache License 2.0", "https://github.com/tesseract-ocr/tesseract"),
    ("RapidOCR (optional)", "Apache License 2.0", "https://github.com/RapidAI/RapidOCR"),
    ("PyQt6", "GPL v3 / commercial", "https://www.riverbankcomputing.com/software/pyqt/"),
    ("NumPy", "BSD 3-Clause", "https://numpy.org"),
    ("Pillow", "MIT-CMU", "https://python-pillow.org"),
    ("pytesseract", "Apache License 2.0", "https://github.com/madmaze/pytesseract"),
    ("openpyxl", "MIT", "https://openpyxl.readthedocs.io"),
    ("PyInstaller (build only)", "GPL v2 with exception", "https://pyinstaller.org"),
)

_RED = "#BA0C2F"


def _open(url: str) -> None:
    QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))


def _link_row(*pairs: tuple[str, str]) -> QtWidgets.QWidget:
    row = QtWidgets.QWidget()
    lay = QtWidgets.QHBoxLayout(row)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(8)
    for label, url in pairs:
        btn = QtWidgets.QPushButton(label)
        btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(
            "QPushButton { padding: 5px 12px; border: 1px solid #c0c4c8; border-radius: 4px;"
            " background: #f8f9fa; }"
            "QPushButton:hover { background: #eef1f3; }"
        )
        btn.clicked.connect(lambda _=False, u=url: _open(u))
        lay.addWidget(btn)
    lay.addStretch(1)
    return row


def _text(html: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(html)
    label.setTextFormat(QtCore.Qt.TextFormat.RichText)
    label.setWordWrap(True)
    label.setOpenExternalLinks(True)
    label.setTextInteractionFlags(
        QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        | QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse
    )
    return label


class AboutDialog(QtWidgets.QDialog):
    """Tabbed About dialog: About, Cite, Acknowledgments, Licenses."""

    def __init__(self, parent: QtWidgets.QWidget | None = None, tab: str = "about") -> None:
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_TITLE}")
        self.setMinimumWidth(560)
        self.setModal(True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 12)
        layout.setSpacing(10)

        header = QtWidgets.QLabel(
            f'<span style="font-size:18pt; font-weight:600; color:#000;">LinePilot Digitizer</span>'
            f'&nbsp;&nbsp;<span style="font-size:11pt; color:#555;">version {APP_VERSION}</span>'
        )
        header.setTextFormat(QtCore.Qt.TextFormat.RichText)
        layout.addWidget(header)
        tagline = QtWidgets.QLabel("Line-plot recovery with manual and automatic calibration")
        tagline.setStyleSheet("color: #444;")
        layout.addWidget(tagline)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setDocumentMode(True)
        layout.addWidget(self.tabs, 1)

        # ---- About -------------------------------------------------------------------
        about = QtWidgets.QWidget()
        about_lay = QtWidgets.QVBoxLayout(about)
        about_lay.setSpacing(10)
        about_lay.addWidget(_text(
            "LinePilot turns a picture of a line plot into numbers. It reads the axes, follows "
            "each colored curve column by column, and exports a CSV plus an overlay image so you "
            "can check its work.<br><br>"
            f"<b>Authors</b><br>{AUTHORS}<br>"
            f'<span style="color:#555;">{AFFILIATIONS}<br>'
            "* equal contribution &nbsp; † corresponding authors</span><br><br>"
            f'<b>Contact</b> &nbsp;<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> '
            "(questions, suggestions, collaborations) &nbsp;·&nbsp; "
            f'<a href="{ISSUES_URL}">GitHub Issues</a> (bug reports, feature requests)'
        ))
        about_lay.addWidget(_link_row(
            ("Project website", PROJECT_URL),
            ("Paper (arXiv)", PAPER_URL),
            ("Source code", REPO_URL),
            ("Report an issue", ISSUES_URL),
        ))
        about_lay.addStretch(1)
        self.tabs.addTab(about, "About")

        # ---- Cite --------------------------------------------------------------------
        cite = QtWidgets.QWidget()
        cite_lay = QtWidgets.QVBoxLayout(cite)
        cite_lay.setSpacing(8)
        cite_lay.addWidget(_text(
            "If LinePilot or DigitizerBench is useful in your work, please cite the paper:"
            f"<br><br><i>{CITATION_TEXT}</i>"
        ))
        self.bibtex = QtWidgets.QPlainTextEdit(BIBTEX)
        self.bibtex.setReadOnly(True)
        self.bibtex.setFont(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont))
        self.bibtex.setMinimumHeight(150)
        cite_lay.addWidget(self.bibtex, 1)
        buttons = QtWidgets.QHBoxLayout()
        self.copy_bibtex = QtWidgets.QPushButton("Copy BibTeX")
        self.copy_bibtex.clicked.connect(self._copy_bibtex)
        copy_text = QtWidgets.QPushButton("Copy plain citation")
        copy_text.clicked.connect(lambda: self._copy(CITATION_TEXT, copy_text, "Copy plain citation"))
        buttons.addWidget(self.copy_bibtex)
        buttons.addWidget(copy_text)
        buttons.addStretch(1)
        cite_lay.addLayout(buttons)
        self.tabs.addTab(cite, "Cite")

        # ---- Acknowledgments ---------------------------------------------------------
        ack = QtWidgets.QWidget()
        ack_lay = QtWidgets.QVBoxLayout(ack)
        ack_lay.addWidget(_text(ACKNOWLEDGMENT.replace("\n\n", "<br><br>")))
        ack_lay.addStretch(1)
        self.tabs.addTab(ack, "Acknowledgments")

        # ---- Licenses ----------------------------------------------------------------
        lic = QtWidgets.QWidget()
        lic_lay = QtWidgets.QVBoxLayout(lic)
        rows = "".join(
            f'<tr><td style="padding:2px 14px 2px 0;"><a href="{url}">{name}</a></td>'
            f'<td style="padding:2px 0; color:#555;">{license_}</td></tr>'
            for name, license_, url in THIRD_PARTY
        )
        lic_lay.addWidget(_text(
            "LinePilot Digitizer is released under the "
            '<a href="https://github.com/RayanA07/LinePilot/blob/main/LICENSE">Apache License 2.0</a>.'
            "<br><br>It builds on these open-source projects:"
            f'<table style="margin-top:6px;">{rows}</table>'
        ))
        lic_lay.addStretch(1)
        self.tabs.addTab(lic, "Licenses")

        close = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Close)
        close.rejected.connect(self.reject)
        layout.addWidget(close)

        index = {"about": 0, "cite": 1, "acknowledgments": 2, "licenses": 3}.get(tab, 0)
        self.tabs.setCurrentIndex(index)

    def _copy(self, text: str, button: QtWidgets.QPushButton, label: str) -> None:
        QtWidgets.QApplication.clipboard().setText(text)
        button.setText("Copied")
        QtCore.QTimer.singleShot(1500, lambda: button.setText(label))

    def _copy_bibtex(self) -> None:
        self._copy(BIBTEX, self.copy_bibtex, "Copy BibTeX")


def build_about_button(window: QtWidgets.QMainWindow, style: str) -> QtWidgets.QToolButton:
    """The 'About ▾' toolbar button for the top-right corner of the main window."""
    button = QtWidgets.QToolButton()
    button.setText("About ▾")
    button.setStyleSheet(style)
    button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
    menu = QtWidgets.QMenu(window)

    def show(tab: str) -> None:
        AboutDialog(window, tab=tab).exec()

    menu.addAction("About LinePilot…").triggered.connect(lambda: show("about"))
    menu.addAction("Cite this software…").triggered.connect(lambda: show("cite"))
    menu.addAction("Acknowledgments…").triggered.connect(lambda: show("acknowledgments"))
    menu.addAction("Third-party licenses…").triggered.connect(lambda: show("licenses"))
    menu.addSeparator()
    menu.addAction("Project website").triggered.connect(lambda: _open(PROJECT_URL))
    menu.addAction("Paper on arXiv").triggered.connect(lambda: _open(PAPER_URL))
    menu.addAction("Source code on GitHub").triggered.connect(lambda: _open(REPO_URL))
    menu.addAction("Report an issue").triggered.connect(lambda: _open(ISSUES_URL))
    menu.addAction("Contact the team (email)").triggered.connect(lambda: _open(f"mailto:{CONTACT_EMAIL}?subject=LinePilot%20Digitizer"))
    button.setMenu(menu)
    window.about_button = button
    window.about_menu = menu
    return button
