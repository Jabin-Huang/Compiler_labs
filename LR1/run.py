import sys

from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QAbstractItemView, QTableWidgetItem, QHeaderView, \
    QMessageBox

from window import Ui_LR1
from childwindow import  Ui_childWindow
import LR1
import graphDFA

class MyWin(QWidget, Ui_LR1):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)
        self.openFileButton.clicked.connect(self.openFile)
        self.analyzeButton.clicked.connect(self.handle_analy)
        # self.analyzeButton.clicked.connect(self.restart)
        self.DFAbutton.clicked.connect(graphDFA.draw_DFA)
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
                item = line.split("->")
                if item[0] in LR1.Grammer:
                    LR1.Grammer[item[0]].add(item[1])
                else:
                    LR1.Grammer[item[0]] = set()
                    LR1.Grammer[item[0]].add(item[1])
                    if item[0]=='E':
                        LR1.Grammer['S'] = set('E')
                        self.GramerList.addItem('S->E')
                        LR1.rule_id[('S','E')] = LR1.r_tot
                        LR1.id_rule[LR1.r_tot] = (item[0], item[1])
                        LR1.r_tot = LR1.r_tot+1
                self.GramerList.addItem(line)
                LR1.rule_id[(item[0], item[1])] = LR1.r_tot
                LR1.id_rule[LR1.r_tot] = (item[0], item[1])
                LR1.r_tot = LR1.r_tot + 1
        self.process()

    def output_table(self):
        self.AnalyTable.verticalHeader().setVisible(False)
        self.AnalyTable.horizontalHeader().setVisible(False)
        self.AnalyTable.setRowCount(LR1.s_tot+2)
        self.AnalyTable.setColumnCount(1+len(LR1.allChar-set('εS')))
        self.AnalyTable.setItem(0,0,QTableWidgetItem("状态"))
        self.AnalyTable.setSpan(0,0,2,1)
        self.AnalyTable.setItem(0,1,QTableWidgetItem("ACTION"))
        #居中
        self.AnalyTable.item(0,1).setTextAlignment(Qt.AlignCenter)
        boarder = len(LR1.VT - set('ε')) + 1
        self.AnalyTable.setSpan(0, 1, 1, len(LR1.VT))
        self.AnalyTable.setItem(0, boarder, QTableWidgetItem("GOTO"))
        #居中
        self.AnalyTable.item(0, boarder).setTextAlignment(Qt.AlignCenter)
        self.AnalyTable.setSpan(0, boarder, 1, len(LR1.allChar-LR1.VT))
        #输入符
        for i,j in zip(LR1.VT-set('ε'),range(len(LR1.VT-set('ε')))):
            self.AnalyTable.setItem(1,1+j,QTableWidgetItem(i))
        #非终结符
        for i,j in zip(LR1.allChar-LR1.VT-set('S'),range(len(LR1.allChar-LR1.VT-set('S')))):
            self.AnalyTable.setItem(1,boarder+j,QTableWidgetItem(i))
        #填内容
        for i in range(LR1.s_tot):
            self.AnalyTable.setItem(i+2,0,QTableWidgetItem(str(i)))
            #ACTION
            for j,k in zip(range(len(LR1.VT-set('ε'))),LR1.VT-set('ε')):
                if str(i) in LR1.ACTION and k in LR1.ACTION[str(i)]:
                    self.AnalyTable.setItem(i+2,1+j,QTableWidgetItem(LR1.ACTION[str(i)][k]))
            #GOTO
            for j,k in zip(range(len(LR1.allChar-LR1.VT-set('S'))),LR1.allChar-LR1.VT-set('S')):
                if str(i) in LR1.GOTO and k in LR1.GOTO[str(i)]:
                    self.AnalyTable.setItem(i+2,boarder+j,QTableWidgetItem(LR1.GOTO[str(i)][k]))
        # 用户不可编辑表格内容
        self.AnalyTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 行列大小与内容相匹配
        # self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.resizeRowsToContents()
        # 根据窗口大小改变表格头大小
        self.AnalyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.AnalyTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def handle_analy(self):
        self.inputStr = self.lineEdit.text()
        if len(self.inputStr)==0:
            QMessageBox.warning(self,"警告","输入为空！")
        elif len(LR1.Grammer)==0:
            QMessageBox.warning(self, "警告", "请先导入文法！")
        else:
            self.child.show()
            self.child.processTable.verticalHeader().hide()
            self.child.processTable.setColumnCount(5)
            self.child.processTable.setHorizontalHeaderLabels(["步骤", "状态栈", "符号栈", "输入串", "动作说明"])
            self.child.processTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.child.processTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.totalControl()

    def totalControl(self):
        stack_status =['0']
        stack_char=['#']
        ACTION = LR1.ACTION
        GOTO = LR1.GOTO
        id_rule= LR1.id_rule
        cur = 0
        step = 0
        while True:
            top = stack_status[-1]
            a = self.inputStr[cur]
            self.child.processTable.setRowCount(step+1)
            self.child.processTable.setItem(step, 0, QTableWidgetItem(str(step)))
            self.child.processTable.setItem(step, 1, QTableWidgetItem(','.join(stack_status)))
            self.child.processTable.setItem(step, 2, QTableWidgetItem(''.join(stack_char)))
            self.child.processTable.setItem(step, 3, QTableWidgetItem(self.inputStr[cur:]))
            if ACTION[top].get(a) is None:
                info = "ACTION[" + top + ',' + a + ']未定义，分析失败'
                self.child.processTable.setItem(step, 4, QTableWidgetItem(info))
                break
            elif 'acc' in ACTION[top].get(a):
                info = 'acc:分析成功'
                self.child.processTable.setItem(step, 4, QTableWidgetItem(info))
                break
            elif 's' in ACTION[top].get(a):
                #移进
                info = "ACTION[" + top + ',' + a + ']=' + ACTION[top][a]+',状态'+ACTION[top][a][1:]+'入栈'
                self.child.processTable.setItem(step, 4,QTableWidgetItem(info))
                stack_status.append(ACTION[top][a][1:])
                stack_char.append(a)
                cur = cur + 1
                step = step + 1
            elif 'r' in ACTION[top].get(a):
                #用A->β归约
                beta_id = ACTION[top][a][1:]
                left, right = id_rule[int(beta_id)]
                len_beta = len(right)
                info ="r"+beta_id+':'+left+'->'+right+'归约，GOTO('+stack_status[-1-len_beta]+','+left+')='+GOTO[stack_status[-1-len_beta]][left]+'入栈'
                self.child.processTable.setItem(step, 4, QTableWidgetItem(info))
                while(len_beta > 0):
                    stack_status.pop()
                    stack_char.pop()
                    len_beta =  len_beta - 1
                #Sm-r
                s = stack_status[-1]
                stack_status.append(GOTO[s][left])
                stack_char.append(left)
                step = step + 1

    def process(self):
        LR1.get_allCharAndVT()
        LR1.get_first()
        LR1.items()
        LR1.get_table()
        print('get table done')
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
