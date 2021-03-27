'''left hand filter aerea
'''
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QToolButton, QHBoxLayout, QCheckBox, QLabel, 
    QSpacerItem, QSizePolicy, QLineEdit, QCompleter
)
import qtawesome as qta


class FilterWidget(QWidget):
    textFilterAdded = pyqtSignal(str)
    textFilterRemoved = pyqtSignal(str)
    categoryEnabledChanged = pyqtSignal(int, bool)

    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        self.categorywidgets = {}
        self.categories_frame = QFrame()
        self.categories_frame.setLayout(QVBoxLayout())
        self.categories_frame.layout().setSpacing(2)
        layout.addWidget(self.categories_frame)
        layout.setContentsMargins(6, 6, 3, 6)

        tf = QWidget()
        tf.setStyleSheet("background-color: transparent")
        tf.setLayout(QVBoxLayout())
        tf.layout().setContentsMargins(0, 0, 0, 0)
        layout.addWidget(tf)
        self.textfilters_frame = tf
        # line edit
        le = QLineEdit()
        le.setPlaceholderText('enter text filter')
        le.setMinimumHeight(30)
        le.returnPressed.connect(self._addTextFilterBox)
        _change_font(le)
        layout.addWidget(le)
        self.searchedit = le
        # patch layout
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

    def setup(self, categories, keywords):
        layout = self.categories_frame.layout()
        for cat in categories:
            w = _CategoryWidget(cat.shortname, cat.longname)
            w.selectedChanged.connect(self._onCatSelectedChanged)
            w.modelCount = 0  # QtGui.qApp.filterManager.get_category_model_count(cat.id, [])
            self.categorywidgets[cat.id] = w
            layout.addWidget(w)
        # setup keyword completer
        completer = QCompleter(keywords)
        _change_font(completer.popup())
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.searchedit.setCompleter(completer)

    def updateCategoryStatistics(self, catid, count):
        self.categorywidgets[catid].modelCount = count

    def _addTextFilterBox(self):
        text = self.searchedit.text()
        if len(text):
            self.textFilterAdded.emit(text)
            tf = _TextFilterBox(text)
            tf.removeRequested.connect(self._removeTextFilterBox)
            layout = self.textfilters_frame.layout()
            layout.addWidget(tf)
            # workaround strange Qlineedit behaivor
            QTimer.singleShot(100, self.searchedit.clear)

    def _removeTextFilterBox(self, welches):
        self.textFilterRemoved.emit(welches.text)
        layout = self.textfilters_frame.layout()
        layout.removeWidget(welches)
        welches.deleteLater()

    def _onCatSelectedChanged(self, catw, enabled):
        for id in self.categorywidgets.keys():
            if catw == self.categorywidgets[id]:
                self.categoryEnabledChanged.emit(id, enabled)


class _CategoryWidget(QWidget):
    selectedChanged = pyqtSignal(QWidget, bool)

    def __init__(self, shortname, longname):
        super(QWidget, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._btn = QCheckBox(f'{shortname}   {longname}')
        self._btn.setChecked(True)
        self._btn.clicked.connect(self.onClicked)
        _change_font(self._btn)
        layout.addWidget(self._btn)

        self._modelCount = 0
        self._lbl = QLabel('')
        self._lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        _change_font(self._lbl, bold=False)
        layout.addWidget(self._lbl)

    def onClicked(self):
        self.selectedChanged.emit(self, self._btn.isChecked())

    @property
    def selected(self):
        self._btn.checked()

    @property
    def modelCount(self):
        return self._modelCount

    @modelCount.setter
    def modelCount(self, value):
        self._modelCount = value
        self._lbl.setText(str(value))
        style = 'color: gray' if value == 0 else ''
        self._lbl.setStyleSheet(style)


class _TextFilterBox(QFrame):
    removeRequested = pyqtSignal(QWidget)

    def __init__(self, text):
        super(QFrame, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("background-color: #19232D")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        lbl = QLabel(text)
        _change_font(lbl)
        layout.addWidget(lbl)
        self.text = text

        btn = QToolButton()
        btn.clicked.connect(self.onBtnClicked)
        btn.setIcon(qta.icon('fa5s.times', color='gray'))
        layout.addWidget(btn)

    def onBtnClicked(self):
        self.removeRequested.emit(self)


def _change_font(widget, size=10, bold=False):
    font = widget.font()
    font.setPointSize(size)
    font.setBold(bold)
    widget.setFont(font)
