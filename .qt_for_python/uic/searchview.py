# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'searchview.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pictureviz import PictureEditor
from filterviz import FilterWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(812, 509)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 3, 6, 3)
        self.btnLoad = QToolButton(Form)
        self.btnLoad.setObjectName(u"btnLoad")
        self.btnLoad.setEnabled(True)
        self.btnLoad.setMinimumSize(QSize(36, 36))
        self.btnLoad.setIconSize(QSize(28, 28))
        self.btnLoad.setCheckable(False)
        self.btnLoad.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout.addWidget(self.btnLoad)

        self.btnClipBoard = QToolButton(Form)
        self.btnClipBoard.setObjectName(u"btnClipBoard")
        self.btnClipBoard.setEnabled(True)
        self.btnClipBoard.setMinimumSize(QSize(36, 36))
        self.btnClipBoard.setIconSize(QSize(28, 28))
        self.btnClipBoard.setCheckable(False)
        self.btnClipBoard.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout.addWidget(self.btnClipBoard)

        self.btnCloseImage = QToolButton(Form)
        self.btnCloseImage.setObjectName(u"btnCloseImage")
        self.btnCloseImage.setMinimumSize(QSize(36, 36))
        self.btnCloseImage.setIconSize(QSize(28, 28))
        self.btnCloseImage.setCheckable(False)

        self.horizontalLayout.addWidget(self.btnCloseImage)

        self.btnCamera = QToolButton(Form)
        self.btnCamera.setObjectName(u"btnCamera")
        self.btnCamera.setMinimumSize(QSize(36, 36))
        self.btnCamera.setIconSize(QSize(28, 28))

        self.horizontalLayout.addWidget(self.btnCamera)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.btnMeasure = QToolButton(Form)
        self.btnMeasure.setObjectName(u"btnMeasure")
        self.btnMeasure.setMinimumSize(QSize(36, 36))
        self.btnMeasure.setIconSize(QSize(28, 28))
        self.btnMeasure.setCheckable(False)

        self.horizontalLayout.addWidget(self.btnMeasure)

        self.btnRegion = QToolButton(Form)
        self.btnRegion.setObjectName(u"btnRegion")
        self.btnRegion.setMinimumSize(QSize(36, 36))
        self.btnRegion.setIconSize(QSize(28, 28))
        self.btnRegion.setCheckable(False)

        self.horizontalLayout.addWidget(self.btnRegion)

        self.btnCutForeground = QToolButton(Form)
        self.btnCutForeground.setObjectName(u"btnCutForeground")
        self.btnCutForeground.setMinimumSize(QSize(36, 36))
        self.btnCutForeground.setIconSize(QSize(28, 28))
        self.btnCutForeground.setCheckable(False)

        self.horizontalLayout.addWidget(self.btnCutForeground)

        self.btnSearch = QToolButton(Form)
        self.btnSearch.setObjectName(u"btnSearch")
        self.btnSearch.setMinimumSize(QSize(0, 36))
        font = QFont()
        font.setPointSize(10)
        self.btnSearch.setFont(font)
        self.btnSearch.setIconSize(QSize(28, 28))
        self.btnSearch.setCheckable(False)
        self.btnSearch.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.btnSearch)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnSettings = QToolButton(Form)
        self.btnSettings.setObjectName(u"btnSettings")
        self.btnSettings.setEnabled(True)
        self.btnSettings.setMinimumSize(QSize(36, 36))
        self.btnSettings.setIconSize(QSize(28, 28))
        self.btnSettings.setCheckable(False)
        self.btnSettings.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout.addWidget(self.btnSettings)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(3)
        self.filterWidget = FilterWidget(self.splitter)
        self.filterWidget.setObjectName(u"filterWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.filterWidget.sizePolicy().hasHeightForWidth())
        self.filterWidget.setSizePolicy(sizePolicy1)
        self.filterWidget.setBaseSize(QSize(200, 0))
        self.verticalLayout = QVBoxLayout(self.filterWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter.addWidget(self.filterWidget)
        self.picEditor = PictureEditor(self.splitter)
        self.picEditor.setObjectName(u"picEditor")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(5)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.picEditor.sizePolicy().hasHeightForWidth())
        self.picEditor.setSizePolicy(sizePolicy2)
        self.picEditor.setMinimumSize(QSize(300, 200))
        self.splitter.addWidget(self.picEditor)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.btnLoad.setToolTip(QCoreApplication.translate("Form", u"load File", None))
#endif // QT_CONFIG(tooltip)
        self.btnLoad.setText(QCoreApplication.translate("Form", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnClipBoard.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>copy from clipboard<br/><span style=\" font-weight:600;\">Ctrl+'V</span>'</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnClipBoard.setText(QCoreApplication.translate("Form", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnCloseImage.setToolTip(QCoreApplication.translate("Form", u"Close Image", None))
#endif // QT_CONFIG(tooltip)
        self.btnCloseImage.setText(QCoreApplication.translate("Form", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnCamera.setToolTip(QCoreApplication.translate("Form", u"Live Video", None))
#endif // QT_CONFIG(tooltip)
        self.btnCamera.setText(QCoreApplication.translate("Form", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnMeasure.setToolTip(QCoreApplication.translate("Form", u"Measure Distance", None))
#endif // QT_CONFIG(tooltip)
        self.btnMeasure.setText(QCoreApplication.translate("Form", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnRegion.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Region of Interest</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnRegion.setText(QCoreApplication.translate("Form", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnCutForeground.setToolTip(QCoreApplication.translate("Form", u"cut foreground", None))
#endif // QT_CONFIG(tooltip)
        self.btnCutForeground.setText(QCoreApplication.translate("Form", u"...", None))
        self.btnSearch.setText(QCoreApplication.translate("Form", u"  Search", None))
#if QT_CONFIG(tooltip)
        self.btnSettings.setToolTip(QCoreApplication.translate("Form", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.btnSettings.setText(QCoreApplication.translate("Form", u"...", None))
    # retranslateUi

