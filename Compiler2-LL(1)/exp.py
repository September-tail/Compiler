# coding=utf-8
from prettytable import PrettyTable
import copy

file = open("test/input1.txt")
inputline = file.readline()
# notendchar保存所有的非终结符
notendcharlist = []
for i in range(len(inputline) - 1):
    if inputline[i] != ' ':
        notendcharlist.append(inputline[i])
print("该文法的所有非终结符有:")
print(notendcharlist)
# endcharlist保存所有的终结符
inputline = file.readline()
endcharlist = []
for i in range(len(inputline) - 1):
    if inputline[i] != ' ':
        endcharlist.append(inputline[i])
print("该文法的所有终结符有:")
print(endcharlist)
inputline = file.readline()
# inferdict 保存所有的产生式
inferdict = {}
# 初始化inferdict
for char in notendcharlist:
    inferdict[char] = []
# 读取文法,填入inferdict
print("该文法的所有产生式如下：")
while inputline:
    rs = inputline.replace('\n', '')
    left = rs[0:1]
    right = rs[2:]
    inferdict[left].append(right)
    inputline = file.readline()
file.close()
# 打印文法
for i in range(len(notendcharlist)):
    print("%s -> " % notendcharlist[i], end='')
    print(" | ".join(inferdict[notendcharlist[i]]))



# 维护一个可用大写字母表，用作新的非终结符
letters = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
char_can_use = letters.split()
for item in char_can_use:
    if item in notendcharlist:
        char_can_use.remove(item)


# 判断文法的某个非终结符是否存在直接左递归
def if_has_left_recursion(_left, _inferdict):
    # _left是一个非终结符号
    # _inferdict是该文法的推导字典
    for i in _inferdict[_left]:
        if i[0] == _left:
            return True
    return False


# 消除一个非终结符的所有直接左递归,并返回新的_inferdict
def avoid_straight_left_recursion(_left, _inferdict):
    # 声明以下两个list为全局变量方便相关函数改写
    global char_can_use
    global notendcharlist
    # _left是一个非终结符号
    # _inferdict是该文法的推导字典
    # _group1保存所有有直接左递归的产生式
    _group1 = []
    # _group2保寸其他产生式
    _group2 = []
    for i in _inferdict[_left]:
        if i[0] == _left:
            _group1.append(i)
        else:
            _group2.append(i)
    # 从char_can_use中弹出一个作为新非终结符
    _new_not_end_char = char_can_use.pop()
    notendcharlist.append(_new_not_end_char)
    # 更改产生式
    _inferdict[_left] = []
    for i in _group2:
        i = i + _new_not_end_char
        _inferdict[_left].append(i)
    _inferdict[_new_not_end_char] = []
    for i in _group1:
        i = i.replace(_left, "")
        i = i + _new_not_end_char
        _inferdict[_new_not_end_char].append(i)
    if 'ε' not in _inferdict[_new_not_end_char]:
        _inferdict[_new_not_end_char].append("ε")

    return _inferdict


# 消除一个文法的所有左递归，包括间接左递归,返回处理后的 _inferdict
def avoid_all_left_recursion(_inferdict):
    _inferdict_copy = copy.deepcopy(_inferdict)
    for i in range(len(notendcharlist)):
        for j in range(0, i):
            # 改写文法
            for k in _inferdict_copy[notendcharlist[i]]:
                if k[0] == notendcharlist[j]:
                    _temp_k = k
                    _inferdict_copy[notendcharlist[i]].remove(k)
                    for q in _inferdict_copy[notendcharlist[j]]:
                        _new_right = _temp_k.replace(notendcharlist[j], q)
                        _inferdict_copy[notendcharlist[i]].append(_new_right)
        if if_has_left_recursion(notendcharlist[i], _inferdict_copy) == True:
            _inferdict_copy = avoid_straight_left_recursion(notendcharlist[i], _inferdict_copy)
    return _inferdict_copy


print("消除所有左递归后的文法如下：")
inferdict = avoid_all_left_recursion(inferdict)
for i in range(len(notendcharlist)):
    print("%s -> " % notendcharlist[i], end='')
    print(" | ".join(inferdict[notendcharlist[i]]))


# 求两个字符串的最长公共前缀
def return_longest_prefix(str1, str2):
    _min_lenth = min(len(str1), len(str2))
    _longest_prefix = ""
    for i in range(_min_lenth):
        if str1[i] == str2[i]:
            _longest_prefix = _longest_prefix + str1[i]
        else:
            break
    if len(_longest_prefix) > 0:
        return _longest_prefix
    else:
        return None


# 判断对于某非终结符号的所有产生式，是否有左公共因子
def if_has_left_divisor(_left, _inferdict):
    _perfix_matrix = []
    # 初始化矩阵
    _count = len(_inferdict[_left])
    for i in range(_count):
        _temp = []
        for j in range(_count):
            _temp.append([])
        _perfix_matrix.append(_temp)
    # _all_prefix保存找出的所有可提取前缀，用于之后比较长度
    _all_prefix = []
    # 在矩阵中填入两两之间的最长公共前缀
    for i in range(_count):
        for j in range(i + 1, _count):
            _temp_perfix = return_longest_prefix(_inferdict[_left][i], _inferdict[_left][j])
            if _temp_perfix != None:
                _perfix_matrix[i][j] = _temp_perfix
                if _temp_perfix not in _all_prefix:
                    _all_prefix.append(_temp_perfix)
    # 如果一个可提取前缀也没有
    if len(_all_prefix) == 0:
        return False
    else:
        return True


# 提取左公共因子
def exreact_left_divisor(_left, _inferdict):
    global char_can_use
    global notendcharlist
    # _left是一个非终结符号
    # _inferdict是该文法的推导字典

    # 构造一个"推导式右部公共前缀矩阵"
    _perfix_matrix = []
    # 初始化矩阵
    _count = len(_inferdict[_left])
    for i in range(_count):
        _temp = []
        for j in range(_count):
            _temp.append([])
        _perfix_matrix.append(_temp)
    # _all_prefix保存找出的所有可提取前缀，用于之后比较长度
    _all_prefix = []
    # 在矩阵中填入两两之间的最长公共前缀
    for i in range(_count):
        for j in range(i + 1, _count):
            _temp_perfix = return_longest_prefix(_inferdict[_left][i], _inferdict[_left][j])
            if _temp_perfix != None:
                _perfix_matrix[i][j] = _temp_perfix
                if _temp_perfix not in _all_prefix:
                    _all_prefix.append(_temp_perfix)
    # 找出本次可以提取的最长前缀 _longest_prefix
    _longest_prefix = _all_prefix[0]
    for k in _all_prefix:
        if len(k) > len(_longest_prefix):
            _longest_prefix = k
    # 改写文法
    # ①找出含有该前缀的所有产生式右部,放入_modify_list
    _modify_list = []
    for i in range(_count):
        for j in range(i + 1, _count):
            if _perfix_matrix[i][j] == _longest_prefix:
                if _inferdict[_left][i] not in _modify_list:
                    _modify_list.append(_inferdict[_left][i])
                if _inferdict[_left][j] not in _modify_list:
                    _modify_list.append(_inferdict[_left][j])
    # ②在原推导字典中删去这些表达式
    for q in _modify_list:
        _inferdict[_left].remove(q)
    # ③加入提取公因子后的产生式
    _new_not_end_char = char_can_use.pop()
    notendcharlist.append(_new_not_end_char)
    _new_right = _longest_prefix + _new_not_end_char
    _inferdict[_left].append(_new_right)
    # ④增加新终结符A'及其产生式(注意ε)
    _inferdict[_new_not_end_char] = []
    for p in _modify_list:
        _right = p.replace(_longest_prefix, "")
        if _right == "":
            _inferdict[_new_not_end_char].append("ε")
        else:
            _inferdict[_new_not_end_char].append(_right)
    return _inferdict


for ch in notendcharlist:
    if if_has_left_divisor(ch, inferdict) == True:
        inferdict = exreact_left_divisor(ch, inferdict)

print("提取左公因子后的文法如下：")
for i in range(len(notendcharlist)):
    print("%s -> " % notendcharlist[i], end='')
    print(" | ".join(inferdict[notendcharlist[i]]))

# 判断一个非终结符是否可以推出ε
# chars_can_to_e存放目前可以所有推出ε的所有非终结符
chars_can_to_e = set()
check_break_flag = 1
while True:
    check_break_flag = 1
    _chars_can_to_e = copy.deepcopy(chars_can_to_e)
    # 对于每一个非终结符i
    for i in notendcharlist:
        # 取一条产生式右部j
        for j in inferdict[i]:
            # 如果j中存在一个终结符,则根据这条产生式肯定不能i->ε,取下一条产生式判断
            _if_has_endchar_flag = 0
            for k in range(len(j)):
                if j[k] in endcharlist:
                    _if_has_endchar_flag = 1
            if _if_has_endchar_flag == 1:
                continue
            # 如果该产生式j首字符为ε,则存在i->ε
            if j[0] == 'ε':
                chars_can_to_e.add(i)
            # 如果该产生式j右部全为非终结符
            else:
                # 如果j中每一个非终结符都可以推出ε,则i->ε
                cnt = 0
                for q in range(len(j)):
                    if j[q] in chars_can_to_e:
                        cnt = cnt + 1
                    else:
                        break
                if cnt == len(j):
                    chars_can_to_e.add(i)
    # 检查chars_can_to_e集合是否改变
    if len(_chars_can_to_e) != len(chars_can_to_e):
        check_break_flag = 0
    if check_break_flag == 1:
        break
print(chars_can_to_e)


# 求所有非终结符号的FIRST集
first_set_tbl = {}  # first_set_tbl 是一张保存每个非终结符和对应FIRST集的表
# 初始化，每个非终结符的FIRST集合为空
for k in inferdict.keys():
    first_set_tbl[k] = set()
# 求一个非终结符的FIRST集合
# do...while循环，循环的的终止条件是所有非终结符的FIRST集合（长度）都不再变化
first_break_flag = 1  # flag == 1循环终止
while True:
    first_break_flag = 1
    temp_dict = copy.deepcopy(first_set_tbl)
    # 取一个非终结符i
    for i in inferdict.keys():
        # 取 i 的一条产生式右部j
        for j in inferdict[i]:
            # ① 如果产生式右部j的首字符为终结符或ε，将其加入i的FIRST集,取下一条分析
            if j[0] in endcharlist or j[0] == 'ε':
                first_set_tbl[i].add(j[0])
                continue
            # ② 如果产生式右部j的首字符为非终结符
            else:
                # 按顺序取出该j的一个字符j[k]
                for k in range(len(j)):
                    # 如果当前字符是不能推出ε的非终结符,直接并上,结束
                    if j[k] not in chars_can_to_e:
                        first_set_tbl[i] = first_set_tbl[i] | first_set_tbl[j[k]]
                        break
                    # 如果当前字符是可以推出ε的非终结符,还需要考察下一个符号
                    else:
                        # 先并上当前非终结符的FIRST集
                        first_set_tbl[i] = first_set_tbl[i] | first_set_tbl[j[k]]
                        # 如果后面没有字符了,证明前面都是可以推出ε的非终结符,在FIRST集中加入ε
                        if k == len(j)-1:
                            first_set_tbl[i].add('ε')
                            break
                        # 如果后面还有字符,考察下一个字符
                        else:
                            # 如果下一个字符是终结符,并上该终结符
                            if j[k+1] in endcharlist:
                                first_set_tbl[i].add(j[k+1])
                                break
                            # 如果下一个字符是非终结符,先并上,再取下一个字符分析
                            else:
                                first_set_tbl[i] = first_set_tbl[i] | first_set_tbl[j[k+1]]
                                continue

    # 检查FIRST集合是否改变
    for q in inferdict.keys():
        if len(temp_dict[q]) != len(first_set_tbl[q]):
            first_break_flag = 0
            break
    if first_break_flag == 1:
        break

# 求一个文法符号串的FIRST集合
def get_string_first(_str, _first_set_tbl):
    if len(_str) == 0:
        return set(['ε'])
    elif _str == 'ε':
        return set(['ε'])
    _result = set()
    _cnt = 0
    while _cnt!= len(_str):
        if _str[_cnt] in endcharlist:
            _result.add(_str[_cnt])
            return _result
        elif _str[_cnt] not in chars_can_to_e:
            _result = _result | _first_set_tbl[_str[_cnt]]
            return _result
        elif _str[_cnt] in chars_can_to_e:
            # 如果当前符号可以推出ε,先并入
            _result = _result | (_first_set_tbl[_str[_cnt]] - set(["ε"]) )
            _cnt = _cnt + 1
            continue
    _result = _result | set(["ε"])
    return _result


# 判断一个文法符号串是否一个终结符号也没有
def if_no_endchar (_str ,_endcharlist):
    for _char in _str:
        if _char in _endcharlist:
            return False
    return True

# 求一个非终结符的FOLLOW集合
follow_set_tbl = {}  # follow_set_tbl 是一张保存每个非终结符和对应FOLLOW集的表
# 初始化，每个非终结符的FOLLOW集合为空
for k in inferdict.keys():
    if k == notendcharlist[0]:
        follow_set_tbl[k] = set(['$'])
    else:
        follow_set_tbl[k] = set()
# do...while循环，循环的的终止条件是所有非终结符的FOLLOW集合（长度）都不再变化
follow_break_flag = 1  # flag == 1循环终止
while True:
    follow_break_flag = 1
    temp_dic = copy.deepcopy(follow_set_tbl)
    # 遍历所有产生式
    for i in inferdict.keys():
        for j in inferdict[i]:  # j为某条产生式右部
            for k in range(len(j)):
                # if 是一个非终结符号then:
                if j[k] in notendcharlist:
                    follow_set_tbl[j[k]] = follow_set_tbl[j[k]] | (
                        get_string_first(j[k + 1:], first_set_tbl) - set(['ε']))
                    if 'ε' in get_string_first(j[k + 1:], first_set_tbl) and if_no_endchar (j[k + 1:] ,endcharlist) == True:
                        follow_set_tbl[j[k]] = follow_set_tbl[j[k]] | follow_set_tbl[i]
    # 检查FOLLOW集合是否改变
    for q in inferdict.keys():
        if len(temp_dic[q]) != len(follow_set_tbl[q]):
            follow_break_flag = 0
            break
    if follow_break_flag == 1:
        break

print("该文法的非终结符的FIRST,FOLLW集合表如下：")
table1 = PrettyTable(["非终结符", "FIRST集", "FOLLOW集"])
for i in inferdict.keys():
    _fist_set = first_set_tbl[i]
    _follow_set = follow_set_tbl[i]
    table1.add_row([i, _fist_set, _follow_set])
print(table1)

# 构造每条产生式的SELECT集合
# 格式:{非终结符:{产生式右部:select_set()}}
select_set_dict = {}
for k in inferdict.keys():
    _temp_dict = {}
    for _right in inferdict[k]:
        if _right == "ε":
            _temp_dict[_right] = follow_set_tbl[k]
        else:
            _temp_dict[_right] = get_string_first(_right, first_set_tbl)
    select_set_dict[k] = _temp_dict
print("该文法的SELECT集合如下：")
print(select_set_dict)
print('\n')

# 判断是否是文法
def if_LL_1(select_set_dict):
    _temp_select_dict = copy.deepcopy(select_set_dict)
    for key in select_set_dict.keys():
        if len(select_set_dict[key]) == 1:
            continue
        else:
            (_no_use, _result_set) = _temp_select_dict[key].popitem()
            while len(_temp_select_dict[key]) != 0:
                (_no_use, _t) = _temp_select_dict[key].popitem()
                _result_set = _result_set & _t
                if len(_result_set) != 0:
                    return False
    return True


if if_LL_1(select_set_dict) == True:
    print("该文法是LL(1)文法.")
else:
    print("该文法不是LL(1)文法.")

# 预测分析算法
def predict_analyse(_string, _startchar,_predict_tbl):
    print("要检测的字符串为:%s" % _string)
    table3 = PrettyTable(["栈", "输入", "操作"])
    _state_stack = []
    _state_stack.append('$')
    _state_stack.append(_startchar)
    _input = list(_string)
    _state_stack_copy = copy.deepcopy(_state_stack)
    _input_copy = copy.deepcopy(_input)
    table3.add_row([_state_stack_copy, _input_copy, '开始'])
    while _state_stack != ['$']:
        if _state_stack[-1] == _input[0]:
            _state_stack.pop()
            _input.pop(0)
            _state_stack_copy = copy.deepcopy(_state_stack)
            _input_copy = copy.deepcopy(_input)
            table3.add_row([_state_stack_copy, _input_copy, '删除'])
        elif _state_stack[-1] in endcharlist:
            print("该字符串非法！")
            return False
        elif _predict_tbl[_state_stack[-1]][_input[0]] == "err":
            print("该字符串非法！")
            return False
        else:
            _out = _state_stack.pop()
            _infer = _predict_tbl[_out][_input[0]]
            _split = _infer.split('→')
            _right = _split[1]
            if _right  != "ε":
                _insert = list(_right)
                _insert.reverse()
                _state_stack.extend(_insert)
                _state_stack_copy = copy.deepcopy(_state_stack)
                _input_copy = copy.deepcopy(_input)
                _infer_copy = copy.deepcopy(_infer)
                table3.add_row([_state_stack_copy, _input_copy, _infer_copy])
            else:
                _state_stack_copy = copy.deepcopy(_state_stack)
                _input_copy = copy.deepcopy(_input)
                _infer_copy = copy.deepcopy(_infer)
                table3.add_row([_state_stack_copy, _input_copy, _infer_copy])
    print("该字符串的判断过程如下：")
    print(table3)
    if _state_stack == ['$'] and _input == ['$']:
        print("该字符串合法！")
        return True
    else:
        print("该字符串非法！")
        return False

# 如果该文法是LL(1)文法
if if_LL_1(select_set_dict) == True:
    # 构造预测分析表
    new_endcharlist = copy.deepcopy(endcharlist)
    new_endcharlist.append('$')
    predict_tbl = {}
    # 初始化预测分析表
    for i in notendcharlist:
        _temp_d = {}
        for j in new_endcharlist:
            _temp_d[j] = "err"
        predict_tbl[i] = _temp_d
    # 在预测分析表中插入数据
    for i in select_set_dict.keys():
        for j in select_set_dict[i].keys():
            _temp_infer = i + "→" + j
            for k in select_set_dict[i][j]:
                predict_tbl[i][k] = _temp_infer
    # 打印预测分析表
    print("该文法的预测分析表如下：")
    titlelist = ["非终结符"]
    titlelist.extend(new_endcharlist)
    table2 = PrettyTable(titlelist)
    for i in predict_tbl.keys():
        _insert_line = [i]
        for j in predict_tbl[i].keys():
            _insert_line.append(predict_tbl[i][j])
        table2.add_row(_insert_line)
    print(table2)
    # input1的测试例子
    s0 = "i+i*i"  # 合法
    s1 = "(i*i)+i+i"  # 合法
    s2 = "i+i*((i)+(i))+(i+i)+i"  # 合法
    s3 = "i*i*i*i"  # 合法
    s4 = "*(i+i)*(i)*"  # 不合法
    s5 = "+((i)*(i))+(i+i*i)"  # 不合法
    s6 = "i++" #不合法
    s7 = "i+i+" #不合法

    # input2的测试例子
    a1 = "(a,a)"  # 合法
    a2 = "(a,^,(a))"  # 合法
    a3 = ",(a,a)"  # 不合法
    a4 = "(a,,a）"  # 不合法

    # input4的测试例子
    b1 = "id,d,d"  # 合法
    b2 = "fd,d"  # 合法
    b3 = ",fd,d"  # 不合法

    # input10的测试例子
    d1 = "c x=8;"
    judge_string = s0
    # judge_string = input("请输入你要判断的字符串：")
    judge_string = judge_string + "$"
    rt = predict_analyse(judge_string, notendcharlist[0], predict_tbl)



