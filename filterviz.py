'''left hand filter aerea
'''
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QToolButton, QHBoxLayout, QCheckBox, QLabel,
    QSpacerItem, QSizePolicy, QLineEdit, QCompleter, QMenu
)
from PyQt5 import QtGui
import qtawesome as qta


class FilterWidget(QWidget):
    '''widget auf linken seite mit checkerbocen und text filter'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        self.categoryGroup = _CategoryGroup()
        layout.addWidget(self.categoryGroup)

        self.textfiltergroup = _TextFilterGroup()
        layout.addWidget(self.textfiltergroup)

        self.searchedit = _SearchLineEdit()
        self.searchedit.keywordEntered.connect(self.textfiltergroup.addBox)
        layout.addWidget(self.searchedit)

        # patch layout
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)


class _CategoryGroup(QFrame):
    catEnabledChanged = pyqtSignal()
    '''box mit den checkerboxen'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._showContextMenu)
        manager = QtGui.qApp.filterManager
        manager.changed.connect(self.updateModelCount)
        layout = QVBoxLayout()
        layout.setSpacing(2)
        self.catchilds = {}
        for id, cat in manager.categories.items():
            w = _CategoryCheckbox(cat)
            w.enabledChanged.connect(self._onCheckerEnableChanged)
            self.catchilds[id] = w
            layout.addWidget(w)
        self.setLayout(layout)
        self.layout().setSpacing(2)
        self.updateModelCount()

    def updateModelCount(self):
        manager = QtGui.qApp.filterManager
        for id in self.catchilds.keys():
            count = manager.getFilteredModelCount(id)
            self.catchilds[id].updateCount(count)

    def _onCheckerEnableChanged(self, enabled):
        self.catEnabledChanged.emit()

    def _showContextMenu(self, lpos):
        wunderm = self._childUnderMouse()
        if wunderm is None:
            return
        menu = QMenu(self)
        sa = menu.addAction('Select All')
        sot = menu.addAction('Select Only This')
        sabt = menu.addAction('Select All, But This')
        mres = menu.exec(QtGui.QCursor.pos())
        if mres == sa:
            for cbx in self.catchilds.values():
                cbx.cat.enabled = True
                cbx.btn.setChecked(True)
        elif mres == sot:
            for cbx in self.catchilds.values():
                enabled = cbx == wunderm
                cbx.cat.enabled = enabled
                cbx.btn.setChecked(enabled)
        elif mres == sabt:
            for cbx in self.catchilds.values():
                enabled = cbx != wunderm
                cbx.cat.enabled = enabled
                cbx.btn.setChecked(enabled)
        self.catEnabledChanged.emit()

    def _childUnderMouse(self):
        for w in self.catchilds.values():
            if w.underMouse():
                return w
        return None


class _CategoryCheckbox(QWidget):
    '''einzelne checkerbox mit model count'''
    enabledChanged = pyqtSignal(bool)

    def __init__(self, cat):
        super().__init__()
        self.cat = cat
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.btn = QCheckBox(f'{cat.shortname}   {cat.longname}')
        self.btn.setChecked(cat.enabled)
        self.btn.clicked.connect(self._onClicked)
        _change_font(self.btn)
        layout.addWidget(self.btn)
        self.lbl = QLabel('')
        self.lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        _change_font(self.lbl, bold=False)
        layout.addWidget(self.lbl)

    def updateCount(self, value):
        self.lbl.setText(str(value))
        style = 'color: gray' if value == 0 else ''
        self.lbl.setStyleSheet(style)

    def _onClicked(self):
        checked = self.btn.isChecked()
        self.cat.enabled = checked
        self.enabledChanged.emit(checked)


class _SearchLineEdit(QLineEdit):
    '''suchfenster eingabe'''
    keywordEntered = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText('enter text filter')
        self.setMinimumHeight(30)
        _change_font(self)
        manager = QtGui.qApp.filterManager
        manager.changed.connect(self._clearDelayed)
        completer = QCompleter(manager.keywords)
        _change_font(completer.popup())
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.setCompleter(completer)
        self.returnPressed.connect(self._onReturnPressed)

    def _onReturnPressed(self):
        if len(self.text()) > 0:
            self.keywordEntered.emit(self.text())

    def _clearDelayed(self):
        # workaround strange Qlineedit behaivor with completer
        QTimer.singleShot(100, self.clear)


class _TextFilterGroup(QWidget):
    '''group mit tesxt filter boxes'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("background-color: transparent")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def addBox(self, text):
        tf = _TextFilterBox(text)
        tf.removeRequested.connect(self._remove)
        self.layout.addWidget(tf)
        QtGui.qApp.filterManager.addTextFilter(text)

    def _remove(self, which):
        self.layout.removeWidget(which)
        QtGui.qApp.filterManager.removeTextFilter(which.text)
        which.deleteLater()


class _TextFilterBox(QFrame):
    removeRequested = pyqtSignal(QWidget)

    def __init__(self, text):
        super().__init__()
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
