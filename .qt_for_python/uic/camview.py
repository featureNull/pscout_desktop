# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camview.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(691, 510)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 3, 6, 3)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.sldrZoom = QSlider(Form)
        self.sldrZoom.setObjectName(u"sldrZoom")
        self.sldrZoom.setMinimumSize(QSize(250, 0))
        self.sldrZoom.setOrientation(Qt.Horizontal)
        self.sldrZoom.setInvertedAppearance(True)

        self.horizontalLayout.addWidget(self.sldrZoom)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnSnapshot = QToolButton(Form)
        self.btnSnapshot.setObjectName(u"btnSnapshot")
        self.btnSnapshot.setEnabled(True)
        self.btnSnapshot.setMinimumSize(QSize(36, 36))
        self.btnSnapshot.setIconSize(QSize(28, 28))
        self.btnSnapshot.setCheckable(False)
        self.btnSnapshot.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.btnSnapshot)

        self.btnClose = QToolButton(Form)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setEnabled(True)
        self.btnClose.setMinimumSize(QSize(36, 36))
        self.btnClose.setIconSize(QSize(28, 28))
        self.btnClose.setCheckable(False)
        self.btnClose.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout.addWidget(self.btnClose)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.lblCamera = QLabel(Form)
        self.lblCamera.setObjectName(u"lblCamera")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCamera.sizePolicy().hasHeightForWidth())
        self.lblCamera.setSizePolicy(sizePolicy)
        self.lblCamera.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lblCamera)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"zoom", None))
        self.btnSnapshot.setText(QCoreApplication.translate("Form", u"  Snapshot", None))
        self.btnClose.setText(QCoreApplication.translate("Form", u"...", None))
        self.lblCamera.setText(QCoreApplication.translate("Form", u"init camera, please wait.....", None))
    # retranslateUi

