import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QAbstractItemView, QTableWidgetItem, QHeaderView, \
    QMessageBox
from window import Ui_LL1
from childwindow import  Ui_childWindow
from LL1 import Grammer, get_first, get_follow, judge_LL1, get_Table, get_VT, VT, Table, FOLLOW, FIRST, judge_leftRucr
import LL1


class MyWin(QWidget, Ui_LL1):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)
        self.openFileButton.clicked.connect(self.openFile)
        self.analyzeButton.clicked.connect(self.handle_analy)
        self.child = childWindow()

    def openFile(self):
        info = QFileDialog.getOpenFileName(self, '打开文件', './')
        if info[0]:
            fileName = info[0]
            self.readFromFile(fileName)

    def readFromFile(self, fileName):
        with open(fileName, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.rstrip('\n')
                self.GramerList.addItem(line)
                item = line.split("->")
                if item[0] in Grammer:
                    Grammer[item[0]].add(item[1])
                else:
                    Grammer[item[0]] = set()
                    Grammer[item[0]].add(item[1])
        self.process()

    def output_first(self):
        for key in FIRST.keys():
            line = "FIRST( \'%s\' ): { " % key
            start = 1
            for item in FIRST[key]:
                if start:
                    line = line + ' \'%s\' ' % item
                    start = 0
                else:
                    line = line + ' ,\'%s\' ' % item
            line = line + ' }'
            self.FIRSTlist.addItem(line)

    def output_follow(self):
        for key in FOLLOW.keys():
            line = "FOLLOW( \'%s\' ): { " % key
            start = 1
            for item in FOLLOW[key]:
                if start:
                    line = line + ' \'%s\' ' % item
                    start = 0
                else:
                    line = line + ' , \'%s\' ' % item
            line = line + ' }'
            self.FOLLOWlist.addItem(line)

    def output_table(self):
        self.tableWidget.setRowCount(len(Table))
        self.tableWidget.setColumnCount(len(VT-set('ε')))
        self.tableWidget.setVerticalHeaderLabels(Table.keys())
        self.tableWidget.setHorizontalHeaderLabels(VT-set('ε'))
        for i, k in zip(range(len(Table)), Table.keys()):
            for j, v in zip(range(len(VT-set('ε'))), VT-set('ε')):
                if len(Table[k][v]) > 0:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(Table[k][v]))
        # 用户不可编辑表格内容
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 行列大小与内容相匹配
        # self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.resizeRowsToContents()
        # 根据窗口大小改变表格头大小
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def handle_analy(self):
        self.inputStr = self.lineEdit.text()
        if len(self.inputStr)==0:
            QMessageBox.warning(self,"警告","输入为空！")
        elif len(Grammer)==0:
            QMessageBox.warning(self, "警告", "请先导入文法！")
        elif judge_LL1() is False:
            QMessageBox.warning(self, "警告", "该文法不是LL1文法！")
        else:
            self.child.show()
            self.child.analyTable.verticalHeader().hide()
            self.child.analyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.child.analyTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.totalControl()


    def totalControl(self):
        stack = list()
        stack.append('#')
        stack.append('E')
        step = 0
        index = 0
        a = self.inputStr[index]
        self.child.analyTable.setRowCount(step + 1)
        self.child.analyTable.setItem(step, 0, QTableWidgetItem(str(step)))
        self.child.analyTable.setItem(step, 1, QTableWidgetItem(''.join(stack)))
        self.child.analyTable.setItem(step, 2, QTableWidgetItem(self.inputStr))
        flag = True
        while flag:
            X = stack.pop()
            if X in VT-set('#'):
                if X == a:
                    a = self.inputStr[index+1]
                    index = index + 1
                else:
                    self.error()
                    break
                step = step + 1
                self.child.analyTable.setRowCount(step + 1)
                self.child.analyTable.setItem(step, 0, QTableWidgetItem(str(step)))
                self.child.analyTable.setItem(step, 1, QTableWidgetItem("".join(stack)))
                self.child.analyTable.setItem(step, 2, QTableWidgetItem(self.inputStr[index:]))
            elif X == '#':
                if X == a:
                    QMessageBox.warning(self, "提示", "分析成功！")
                    flag = False
                else:
                    self.error()
                    break
            elif a in VT and Table[X][a] != 'error':
                tmp = Table[X][a].split("->")
                item = tmp[1]
                if item !='ε':
                    for i in range(len(item)):
                        stack.append(item[len(item) - 1 - i])
                step = step + 1
                self.child.analyTable.setRowCount(step + 1)
                self.child.analyTable.setItem(step, 0, QTableWidgetItem(str(step)))
                self.child.analyTable.setItem(step, 1, QTableWidgetItem("".join(stack)))
                self.child.analyTable.setItem(step, 2, QTableWidgetItem(self.inputStr[index:]))
                self.child.analyTable.setItem(step, 3, QTableWidgetItem(Table[X][a]))
            else:
                self.error()
                break


    def error(self):
        QMessageBox.warning(self, "警告", "分析失败！")

    def process(self):
        get_VT()
        for A in Grammer.keys():
            judge_leftRucr(A, A)
            if LL1.leftRucrFlag is True:
                QMessageBox.warning(self, "警告", "文法不是LL1文法（含有左递归）！")
                return
        get_first()
        get_follow()
        self.output_first()
        self.output_follow()
        if judge_LL1() is False:
            QMessageBox.warning(self, "警告", "文法不是LL1文法(含有回溯)！")
            return
        get_Table()
        self.output_table()

class childWindow(QWidget,Ui_childWindow):
    def __init__(self):
        super(childWindow, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
