# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LR1(object):
    def setupUi(self, LR1):
        LR1.setObjectName("LR1")
        LR1.resize(1423, 799)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(LR1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame = QtWidgets.QFrame(LR1)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.openFileButton = QtWidgets.QPushButton(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        self.openFileButton.setFont(font)
        self.openFileButton.setObjectName("openFileButton")
        self.verticalLayout_6.addWidget(self.openFileButton)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.GramerList = QtWidgets.QListWidget(self.frame_3)
        self.GramerList.setObjectName("GramerList")
        self.verticalLayout_6.addWidget(self.GramerList)
        self.horizontalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DFAbutton = QtWidgets.QPushButton(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        self.DFAbutton.setFont(font)
        self.DFAbutton.setObjectName("DFAbutton")
        self.verticalLayout.addWidget(self.DFAbutton)
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.analyzeButton = QtWidgets.QPushButton(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        self.analyzeButton.setFont(font)
        self.analyzeButton.setObjectName("analyzeButton")
        self.horizontalLayout_3.addWidget(self.analyzeButton)
        self.verticalLayout.addWidget(self.frame_6)
        self.horizontalLayout.addWidget(self.frame_4)
        self.verticalLayout_5.addWidget(self.frame)
        self.label_2 = QtWidgets.QLabel(LR1)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.AnalyTable = QtWidgets.QTableWidget(LR1)
        self.AnalyTable.setObjectName("AnalyTable")
        self.AnalyTable.setColumnCount(0)
        self.AnalyTable.setRowCount(0)
        self.verticalLayout_5.addWidget(self.AnalyTable)

        self.retranslateUi(LR1)
        QtCore.QMetaObject.connectSlotsByName(LR1)

    def retranslateUi(self, LR1):
        _translate = QtCore.QCoreApplication.translate
        LR1.setWindowTitle(_translate("LR1", "Form"))
        self.openFileButton.setText(_translate("LR1", "从文件导入文法"))
        self.label_4.setText(_translate("LR1", "文法（已拓广）:"))
        self.DFAbutton.setText(_translate("LR1", "DFA展示"))
        self.label.setText(_translate("LR1", "输入待分析串："))
        self.analyzeButton.setText(_translate("LR1", "分析"))
        self.label_2.setText(_translate("LR1", "LR（1）分析表"))
