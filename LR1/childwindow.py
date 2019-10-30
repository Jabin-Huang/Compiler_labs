# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'childwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_childWindow(object):
    def setupUi(self, childWindow):
        childWindow.setObjectName("childWindow")
        childWindow.resize(1068, 735)
        self.verticalLayout = QtWidgets.QVBoxLayout(childWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.processTable = QtWidgets.QTableWidget(childWindow)
        self.processTable.setAutoFillBackground(False)
        self.processTable.setObjectName("processTable")
        self.processTable.setColumnCount(0)
        self.processTable.setRowCount(0)
        self.verticalLayout.addWidget(self.processTable)

        self.retranslateUi(childWindow)
        QtCore.QMetaObject.connectSlotsByName(childWindow)

    def retranslateUi(self, childWindow):
        _translate = QtCore.QCoreApplication.translate
        childWindow.setWindowTitle(_translate("childWindow", "分析结果"))
