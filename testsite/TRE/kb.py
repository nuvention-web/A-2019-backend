import operator

global facts

class ColorsDbClass(object):

    def __init__(self, fact=[], popularity=None):
        self.fact = fact
        self.popularity = popularity


## General rules about colors
facts = [
    {'fact': [':not', ['red', 'green']]},
    {'fact':['black', '*'], 'popularity': 0.80},
    {'fact': ['white', '*'], 'popularity': 0.95},
    {'fact': ['gray', 'white'], 'popularity': 0.93}
]

# if has weather, we can use implies => to infer about the suitable color in specific season

notLst = []
x = []

for fact in facts:
    if fact['fact'][0] == ':not':
        notLst.append(fact['fact'][1:][0])
    else:
        if 'popularity' in fact:
            p1 = ColorsDbClass(fact = fact['fact'], popularity=fact['popularity'])
        else:
            p1 = ColorsDbClass(fact = fact['fact'])
        x.append(p1)

#print('facts => ', x)
#print('notfacts => ', notLst)

sorted_x = sorted(x, key=operator.attrgetter('popularity'), reverse=True)
#print('sort_ed x => ', sorted_x)

for fact in sorted_x:
    p1 = fact
    #print('fact => ', p1.fact)
    #print('popularity => ', p1.popularity)
    #print('===============')


def createKB():
    notLst = []
    x = []

    for fact in facts:
        if fact['fact'][0] == ':not':
            notLst.append(fact['fact'][1:][0])
        else:
            if 'popularity' in fact:
                p1 = ColorsDbClass(fact=fact['fact'], popularity=fact['popularity'])
            else:
                p1 = ColorsDbClass(fact=fact['fact'])
            x.append(p1)

    sorted_x = sorted(x, key=operator.attrgetter('popularity'), reverse=True)

    kb_facts = {"color_popularity_sorted": sorted_x, "color_nogood_facts": notLst}
    return kb_facts