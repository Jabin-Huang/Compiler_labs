
Grammer = dict()  # 文法
VT =set() #终结符
allChar = set() #所有文法符号
FIRST = dict()  # FIRST集
#items = []  # 项  存储五元组（产生式编号，产生式左部，产生式右部，产生式项的给定点位置（即·的位置），展望符）
item_set = set() #项集
CLOSURE = dict()
GO = dict()
ACTION = dict()
GOTO = dict()
C = set() #项目集族
set_id =dict() #状态编号
rule_id = dict() #产生式编号
id_rule = dict() #编号到产生式的映射
s_tot = 0 #状态数
r_tot = 0 #产生式数


class Item:
    def __init__(self,left,right,pos,forward):
        self.left = left
        self.right = right
        self.pos = pos
        self.forward = forward

    def __eq__(self, other):
         return self.left == other.left and self.right == other.right and self.pos == other.pos and \
         self.forward == other.forward

    def  __hash__(self):
        return hash(self.left)^hash(self.right)^hash(self.pos)^hash(self.forward)


def get_allCharAndVT ():
    for key in Grammer.keys():
        allChar.add(key)
        for item in Grammer[key]:
            for ch in item:
                if not ch.isupper():
                    VT.add(ch)
                    allChar.add(ch)
    VT.add('#')
    allChar.add('#')


def get_first():
    FIRST_SIZE = dict()
    # 对每个文法符号求first集
    # 初始化，并对终结符求first集
    for k in Grammer.keys():
        FIRST[k] = set()
        FIRST_SIZE[k] = 0
    for v in VT:
        FIRST[v] = set(v)
        FIRST_SIZE[v] = 1
    # 对非终结符求first集，当fist_size不再增大，停止循环
    done = False
    while not done:
        done = True
        for k in Grammer.keys():
            for item in Grammer[k]:
                # 产生式X->a...的形式
                if not item[0].isupper():
                    FIRST[k].add(item[0])
                # 产生式X->Y1Y2Y3...的形式
                elif item[0].isupper():
                    FIRST[k] = FIRST[k].union(FIRST[item[0]] - set('ε'))
                    for index, ch in zip(range(len(item)), item):
                        if 'ε' in FIRST[ch] and index + 1 < len(item):
                            FIRST[k] = FIRST[k].union(FIRST[item[index + 1]] - set('ε'))
                        else:
                            break
                    # 所有的Y1,Y2,Y3...都包含空字，将空字加到first（X）
                    for ch in item:
                        if 'ε' not in FIRST[ch]:
                            break
                    else:
                        FIRST[k].add('ε')
            # 检查first集大小的变化
            if len(FIRST[k]) != FIRST_SIZE[k]:
                done = False
                FIRST_SIZE[k] = len(FIRST[k])
    # 对候选项（可能是符号串）求first集
    for k in Grammer.keys():
        for item in Grammer[k]:
            get_strFirst(item)
    FIRST['ε'] = set('ε')


# 在单个符号的first集求出后，可调用此函数求任意符号串X1X2X3...的first集,方法与求X->Y1Y2Y3...形式的first（X）一样
def get_strFirst(item):
    if len(item) > 1:
        FIRST[item] = FIRST[item[0]] - set('ε')
        for index, ch in zip(range(len(item)), item):
            if 'ε' in FIRST[ch] and index + 1 < len(item):
                FIRST[item] = FIRST[item].union(FIRST[index + 1] - set('ε'))
            else:
                break
        for ch in item:
            if 'ε' not in FIRST[ch]:
                break
        else:
            FIRST[item].add('ε')


def get_CLOSURE(I):
    if I in CLOSURE:
        return CLOSURE[I]
    tmp_CLOSURE = set(I)
    done = False
    while not done:
        done = True
        pre_size = len(tmp_CLOSURE)
        #I中每个项 A->α·Bβ，a
        tmp = set(tmp_CLOSURE)
        for item in tmp:
            #item: （产生式左部，产生式右部，产生式右部给定点的位置（即·的位置），展望符）
            right = item.right
            pos = item.pos
            #点在最后面，跳过
            if pos >= len(right):
                continue
            forward = item.forward
            # A->α·Bβ，a ，key=B
            key = right[pos]
            # 判断点后面是否非终结符，若是则展开
            if key.isupper():
                # FIRST（βa）
                if pos + 1 < len(right):
                    temStr = right[pos + 1:] + forward
                else:
                    temStr = forward
                get_strFirst(temStr)
                for rule in Grammer[key]:
                    for b in FIRST[temStr]:
                        # B->·γ，b
                        i = Item(key, rule, 0, b)
                        tmp_CLOSURE.add(i)
        if len(tmp_CLOSURE) > pre_size:
            done = False
    CLOSURE[I] = frozenset(tmp_CLOSURE)
    return CLOSURE[I]


def get_GO(I,X):
    if (I,X) in GO:
        return GO[(I,X)]
    J = set()
    for item in I:
        left = item.left
        right = item.right
        pos = item.pos
        forward = item.forward
        #A->α·Xβ，a
        if pos == len(right):
            continue
        if right[pos]==X and pos+1 <= len(right):
            #A->αX·β，a
            i = Item(left,right,pos+1,forward)
            J.add(i)
    fJ = frozenset(J)
    GO[(I,X)] = get_CLOSURE(fJ)
    return GO[(I,X)]


def items():
    #S'->·S，#
    s = {Item('S','E',0,'#')}
    fs = frozenset(s)
    global s_tot
    s_tot = 0
    #C[0]:id,C[1]:set
    C.add(get_CLOSURE(fs))
    set_id[get_CLOSURE(fs)]=s_tot
    s_tot = s_tot + 1
    done = False
    while not done:
        done = True
        tempC = frozenset(C)
        for I in tempC:
            for X in allChar:
                if len(get_GO(I,X))>0 and GO[(I,X)] not in C:
                    C.add(GO[(I,X)])
                    set_id[GO[(I,X)]] = s_tot
                    s_tot = s_tot + 1
                    done = False


def get_table():
    for id in range(s_tot):
        id  = str(id)
        ACTION[id] = dict()
        GOTO[id] = dict()

    for I in C:
        k = str(set_id[I])
        for item in I:
            pos = item.pos
            left = item.left
            right =item.right
            forward = item.forward
            #A->α·aβ，b
            #GO（Ik，a）=Ij
            #ACTION[k,a] = sj
            if pos <len(right) and not right[pos].isupper():
                a = right[pos]
                ACTION[k][a] = 's'+str( set_id[GO[(I,a)]] )
            #A->α·，a
            elif pos ==len(right) and rule_id[(left,right)] !=0:
                a = forward
                ACTION[k][a] = 'r'+str(rule_id[(left,right)])
            #S'-S·，#
            elif pos == len(right) and rule_id[(left,right)] == 0:
                ACTION[k]['#'] = 'acc'
        #GO[Ik][A]
        for A in allChar - VT:
            if len(GO[(I,A)]) >0 :
                GOTO[k][A] = str(set_id[GO[(I,A)]])