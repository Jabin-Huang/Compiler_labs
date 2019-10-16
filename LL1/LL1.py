import sys

Grammer = dict()  # 文法
FIRST = dict()  # FIRST集
FOLLOW = dict()  # FOLLOW集
Table = dict()  # 分析表
VT = set()  # 终结符
leftRucrFlag = False

def get_VT():
    for key in Grammer.keys():
        for item in Grammer[key]:
            for ch in item:
                if not ch.isupper():
                    VT.add(ch)
    VT.add('#')

def judge_leftRucr(key,A):
    global leftRucrFlag
    if leftRucrFlag is True:
        return
    for item in Grammer[key]:
        if item[0].isupper() and item[0]!=A:
            judge_leftRucr(item[0],A)
        elif item[0]==A:
            leftRucrFlag = True
            return



def judge_LL1():
    # 消除左递归（待完成）
    # 判断FIRST(αi)　& FIRST(aj) =null ； A->α α=》'ε' FIRST(A) & FOLLOW(A) =null
    for key in Grammer.keys():
        for item1 in Grammer[key]:
            for item2 in Grammer[key]:
                if item1 != item2 and len(FIRST[item1] & FIRST[item2]) > 0:
                    return False
            if 'ε' in FIRST[item1]:
                if len(FIRST[key] & FOLLOW[key]) > 0:
                    return False
    return True


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


def get_follow():
    FOLLOW_SIZE = dict()
    for k in Grammer.keys():
        FOLLOW[k] = set()
        FOLLOW_SIZE[k] = 0
    FOLLOW['E'].add('#')
    done = False
    while not done:
        done = True
        for k in Grammer.keys():
            for item in Grammer[k]:
                for index, ch in zip(range(len(item)), item):
                    if ch.isupper():
                        if index + 1 < len(item):
                            get_strFirst(item[index + 1:])
                            #A->αBβ
                            FOLLOW[ch] = FOLLOW[ch].union(FIRST[item[index + 1:]] - set('ε'))
                        #A->αB，或A->αBβ β=》ε
                        if index == len(item) - 1 or 'ε' in FIRST[item[index + 1:]]:
                            FOLLOW[ch] = FOLLOW[ch].union(FOLLOW[k])
                        if len(FOLLOW[ch]) != FOLLOW_SIZE[ch]:
                            FOLLOW_SIZE[ch] = len(FOLLOW[ch])
                            done = False


def get_Table():
    for key in Grammer.keys():
        Table[key] = dict()
        for v in VT - set('ε'):
            Table[key][v] = str()
    for key in Grammer.keys():
        for item in Grammer[key]:
            # 终结符属于first（候选项）时
            for v in FIRST[item]:
                if v != 'ε':
                    Table[key][v] = key + "->" + item
            # first（候选项）中有空字时，考虑follow集
            if 'ε' in FIRST[item]:
                for v in FOLLOW[key]:
                    Table[key][v] = key + "->" + item
    # 无定义的Table{key][v],标上出错标志
    for key in Grammer.keys():
        for v in VT - set('ε'):
            if len(Table[key][v]) == 0:
                Table[key][v] = "error"
