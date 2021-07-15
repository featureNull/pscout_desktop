# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mesauredistdialog.ui'
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
        Dialog.resize(263, 100)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnAcc = QRadioButton(Dialog)
        self.btnAcc.setObjectName(u"btnAcc")

        self.horizontalLayout.addWidget(self.btnAcc)

        self.btnLessAcc = QRadioButton(Dialog)
        self.btnLessAcc.setObjectName(u"btnLessAcc")
        self.btnLessAcc.setChecked(True)

        self.horizontalLayout.addWidget(self.btnLessAcc)

        self.btnInAcc = QRadioButton(Dialog)
        self.btnInAcc.setObjectName(u"btnInAcc")

        self.horizontalLayout.addWidget(self.btnInAcc)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Measure Distance", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"length", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"mesurement [mm]", None))
        self.btnAcc.setText(QCoreApplication.translate("Dialog", u"Accurate", None))
        self.btnLessAcc.setText(QCoreApplication.translate("Dialog", u"Less Accurate", None))
        self.btnInAcc.setText(QCoreApplication.translate("Dialog", u"Inaccurate", None))
    # retranslateUi

