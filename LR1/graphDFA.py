from graphviz import Digraph
import  LR1


# # 添加圆点A,A的标签是Dot A
# dot.node('A', 'Dot A')

# # 在创建两圆点之间创建一条边
# dot.edge('B', 'C', 'test')

strC = dict()

def convertToStr():
    for I in LR1.C:
        strI = dict()
        for  item in I:
            left=item.left
            right=item.right
            pos=item.pos
            if (left,right,pos) not in strI:
                if pos > 0 and pos < len(right):
                    strI[(left, right, pos)] = '%s' % left + '->' + '%s' % right[:pos - 1] + '·' + '%s,' % right[pos:]
                elif pos == 0:
                    strI[(left, right, pos)] = '%s' % left + '->' + '·%s,' % right
                elif pos == len(right):
                    strI[(left, right, pos)] = '%s' % left + '->' + '%s·,' % right
            forward = item.forward
            strI[(left,right,pos)]+=forward+'/'
        strC[str(LR1.set_id[I])] = [str(LR1.set_id[I]),]
        for item in strI.keys():
            strI[item] = strI[item].strip('/')
            strC[str(LR1.set_id[I])].append(strI[item])
        strC[str(LR1.set_id[I])] = '\l'.join(strC[str(LR1.set_id[I])])
    print('convert done!')


def draw_DFA():
    convertToStr()
    dot = Digraph(comment='DFA')
    dot.attr('node',shape = 'box')
    ACTION = LR1.ACTION
    GOTO = LR1.GOTO
    for v in range(LR1.s_tot):
        v = str(v)
        dot.node(v,strC[v])
    for  v in range(LR1.s_tot):
        v = str(v)
        for e in ACTION[v].keys():
            if 's' in ACTION[v][e]:
                dot.edge(v, ACTION[v][e][1:], e)
        for e in GOTO[v].keys():
            dot.edge(v, GOTO[v][e], e)
    dot.view()
    # # 获取DOT source源码的字符串形式
    print(dot.source)
