'''2. Закодируйте любую строку по алгоритму Хаффмана.'''

from collections import Counter,OrderedDict

class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right


def fill_dict(tree, d,ch=''):
        if type(tree.left) is Node:
            fill_dict(tree.left,d, ch+'0')
        else:
            d[tree.left] = ch+'0'

        if type(tree.right) is Node:
            fill_dict(tree.right,d, ch + '1')
        else:
            d[tree.right] = ch + '1'
        return d

def build_tree(st):
    rate = [(key, value) for key, value in OrderedDict(sorted(Counter(st).items(), key=lambda t: t[1])).items()]
    while len(rate) > 1:
        kl, vl = rate.pop()
        kr, vr = rate.pop()
        sum = vl + vr
        node = (Node(kl, kr), sum)
        rate.append(node)
        rate = [(key, value) for key, value in (sorted(rate, key=lambda t: t[1]))]

    tree, s = rate.pop()
    return tree

st = input('Введите строку: ')

d = fill_dict(build_tree(st),{})
code_st = ''.join([d[s] for s in st])
print(code_st.encode('ASCII'))



