# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(420, 446)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 6, 0, 0)
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(False)
        self.serachTab = QWidget()
        self.serachTab.setObjectName(u"serachTab")
        self.verticalLayout_2 = QVBoxLayout(self.serachTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.serachTab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFlat(False)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.sldrWithImage = QSlider(self.groupBox)
        self.sldrWithImage.setObjectName(u"sldrWithImage")
        self.sldrWithImage.setMinimum(3)
        self.sldrWithImage.setMaximum(100)
        self.sldrWithImage.setValue(25)
        self.sldrWithImage.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.sldrWithImage)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(40, 0))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.sldrWithoutImage = QSlider(self.groupBox)
        self.sldrWithoutImage.setObjectName(u"sldrWithoutImage")
        self.sldrWithoutImage.setMinimum(3)
        self.sldrWithoutImage.setMaximum(100)
        self.sldrWithoutImage.setValue(25)
        self.sldrWithoutImage.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.sldrWithoutImage)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(40, 0))
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.label_9 = QLabel(self.serachTab)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_2.addWidget(self.label_9)

        self.listWidget = QListWidget(self.serachTab)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_2.addWidget(self.listWidget)

        self.tabWidget.addTab(self.serachTab, "")
        self.connectionTab = QWidget()
        self.connectionTab.setObjectName(u"connectionTab")
        self.verticalLayout_5 = QVBoxLayout(self.connectionTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_5 = QLabel(self.connectionTab)
        self.label_5.setObjectName(u"label_5")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.label_5)

        self.editIpAdress = QLineEdit(self.connectionTab)
        self.editIpAdress.setObjectName(u"editIpAdress")

        self.verticalLayout_5.addWidget(self.editIpAdress)

        self.label_6 = QLabel(self.connectionTab)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.label_6)

        self.editPort = QLineEdit(self.connectionTab)
        self.editPort.setObjectName(u"editPort")

        self.verticalLayout_5.addWidget(self.editPort)

        self.btnEnableSsl = QCheckBox(self.connectionTab)
        self.btnEnableSsl.setObjectName(u"btnEnableSsl")
        self.btnEnableSsl.setChecked(True)

        self.verticalLayout_5.addWidget(self.btnEnableSsl)

        self.label_7 = QLabel(self.connectionTab)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.label_7)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetFixedSize)
        self.editCertificate = QLineEdit(self.connectionTab)
        self.editCertificate.setObjectName(u"editCertificate")

        self.horizontalLayout_4.addWidget(self.editCertificate)

        self.btnLoadCertificate = QToolButton(self.connectionTab)
        self.btnLoadCertificate.setObjectName(u"btnLoadCertificate")

        self.horizontalLayout_4.addWidget(self.btnLoadCertificate)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.label_8 = QLabel(self.connectionTab)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.label_8)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetFixedSize)
        self.editKey = QLineEdit(self.connectionTab)
        self.editKey.setObjectName(u"editKey")

        self.horizontalLayout_5.addWidget(self.editKey)

        self.btnLoadKey = QToolButton(self.connectionTab)
        self.btnLoadKey.setObjectName(u"btnLoadKey")

        self.horizontalLayout_5.addWidget(self.btnLoadKey)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.verticalSpacer = QSpacerItem(20, 125, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.connectionTab, "")
        self.cameraTab = QWidget()
        self.cameraTab.setObjectName(u"cameraTab")
        self.verticalLayout_4 = QVBoxLayout(self.cameraTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_10 = QLabel(self.cameraTab)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_6.addWidget(self.label_10)

        self.comboCamera = QComboBox(self.cameraTab)
        self.comboCamera.addItem("")
        self.comboCamera.addItem("")
        self.comboCamera.setObjectName(u"comboCamera")

        self.horizontalLayout_6.addWidget(self.comboCamera)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_2 = QSpacerItem(20, 325, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.cameraTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 6, 9, 9)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnOk = QPushButton(Dialog)
        self.btnOk.setObjectName(u"btnOk")
        self.btnOk.setMinimumSize(QSize(80, 23))

        self.horizontalLayout.addWidget(self.btnOk)

        self.btnCancel = QPushButton(Dialog)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setMinimumSize(QSize(80, 23))

        self.horizontalLayout.addWidget(self.btnCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)
        self.btnOk.clicked.connect(Dialog.accept)
        self.btnCancel.clicked.connect(Dialog.reject)
        self.sldrWithImage.valueChanged.connect(self.label_3.setNum)
        self.sldrWithoutImage.valueChanged.connect(self.label_4.setNum)
        self.btnEnableSsl.toggled.connect(self.editCertificate.setEnabled)
        self.btnEnableSsl.toggled.connect(self.btnLoadCertificate.setEnabled)
        self.btnEnableSsl.toggled.connect(self.editKey.setEnabled)
        self.btnEnableSsl.toggled.connect(self.btnLoadKey.setEnabled)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Settings", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"maximal count result displayed", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"With image", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"2", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Without Image", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"3", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Default Filter Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.serachTab), QCoreApplication.translate("Dialog", u"Serach", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"IP Adress", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Port", None))
        self.btnEnableSsl.setText(QCoreApplication.translate("Dialog", u"Use SSL/TLS", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"certificate", None))
        self.btnLoadCertificate.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"key", None))
        self.btnLoadKey.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.connectionTab), QCoreApplication.translate("Dialog", u"Server Connection", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Camera Type", None))
        self.comboCamera.setItemText(0, QCoreApplication.translate("Dialog", u"No Camera", None))
        self.comboCamera.setItemText(1, QCoreApplication.translate("Dialog", u"IDS Usb", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cameraTab), QCoreApplication.translate("Dialog", u"Camera", None))
        self.btnOk.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.btnCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

