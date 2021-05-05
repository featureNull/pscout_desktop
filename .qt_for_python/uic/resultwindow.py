# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resultwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from stl3dviz import StlDetailsView
from pictureviz import PictureView


class Ui_Results(object):
    def setupUi(self, Results):
        if not Results.objectName():
            Results.setObjectName(u"Results")
        Results.resize(911, 667)
        self.centralwidget = QWidget(Results)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.hsplitter = QSplitter(self.centralwidget)
        self.hsplitter.setObjectName(u"hsplitter")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hsplitter.sizePolicy().hasHeightForWidth())
        self.hsplitter.setSizePolicy(sizePolicy)
        self.hsplitter.setOrientation(Qt.Horizontal)
        self.hsplitter.setHandleWidth(3)
        self.vsplitter = QSplitter(self.hsplitter)
        self.vsplitter.setObjectName(u"vsplitter")
        sizePolicy.setHeightForWidth(self.vsplitter.sizePolicy().hasHeightForWidth())
        self.vsplitter.setSizePolicy(sizePolicy)
        self.vsplitter.setMinimumSize(QSize(0, 0))
        self.vsplitter.setOrientation(Qt.Vertical)
        self.vsplitter.setHandleWidth(3)
        self.picView = PictureView(self.vsplitter)
        self.picView.setObjectName(u"picView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.picView.sizePolicy().hasHeightForWidth())
        self.picView.setSizePolicy(sizePolicy1)
        self.picView.setMinimumSize(QSize(0, 256))
        self.vsplitter.addWidget(self.picView)
        self.widget = QWidget(self.vsplitter)
        self.widget.setObjectName(u"widget")
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(9, -1, -1, 9)
        self.stlView = StlDetailsView(self.widget)
        self.stlView.setObjectName(u"stlView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stlView.sizePolicy().hasHeightForWidth())
        self.stlView.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.stlView)

        self.infoText = QLabel(self.widget)
        self.infoText.setObjectName(u"infoText")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.infoText.sizePolicy().hasHeightForWidth())
        self.infoText.setSizePolicy(sizePolicy3)
        self.infoText.setWordWrap(True)

        self.verticalLayout.addWidget(self.infoText)

        self.vsplitter.addWidget(self.widget)
        self.hsplitter.addWidget(self.vsplitter)
        self.scrollArea = QScrollArea(self.hsplitter)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(8)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy4)
        self.scrollArea.setWidgetResizable(True)
        self.contentWidget = QWidget()
        self.contentWidget.setObjectName(u"contentWidget")
        self.contentWidget.setGeometry(QRect(0, 0, 69, 645))
        self.scrollArea.setWidget(self.contentWidget)
        self.hsplitter.addWidget(self.scrollArea)

        self.verticalLayout_2.addWidget(self.hsplitter)

        Results.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(Results)
        self.statusBar.setObjectName(u"statusBar")
        Results.setStatusBar(self.statusBar)

        self.retranslateUi(Results)

        QMetaObject.connectSlotsByName(Results)
    # setupUi

    def retranslateUi(self, Results):
        Results.setWindowTitle(QCoreApplication.translate("Results", u"MainWindow", None))
        self.infoText.setText("")
    # retranslateUi

