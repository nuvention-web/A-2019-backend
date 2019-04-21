import warnings
from TRE.ldata import *
from TRE.lrules import *
import copy

def solveCryptarithmeticProblem():
    sendMoreMoney = [
        ['column 1 D E Y'],
        ['column 2 N R E'],
        ['column 3 E O N'],
        ['column 4 S M O'],
        ['column 5 :blank :blank M'],
        ['leftmost-column 5']
    ]

    choiceSets = makeLetterChoiceSets(sendMoreMoney)
    return choiceSets

def makeLetterChoiceSets(problem):
    """
    Form a possible choice sets letters
    :param problem:
    :return:
    """
    choiceSets = []

    for letter in set(extractProblemLetters(problem)):
        dict = {}
        letterSet = []
        for i in range(0, 10):
            letterSet.append({letter: i})
        choiceSets.append(letterSet)

    print(choiceSets)
    return choiceSets


def extractProblemLetters(problem):
    """
    Extract all letters inside the problem except ':blank'
    :param problem:
    :return:
    """
    letters = []

    for line in problem:
        for letter in line[0].split()[1:]:
            if letter != ':blank' and letter.isalpha():
                letters.append(letter)

    return letters

# ================= Useless above ============================

global tmpEnv

def ddSearch(choiceSets, level=0, stack=[[]], ltre=[], debugging=False):
    #print('level ==> ', level)
    if choiceSets == None or choiceSets == []:
        print('***********************************************************')
        print('A feasible ddsearch solution is:')
        print('level =', level, ' stack =', stack[level-1])
        myglobal.ans[myglobal.num] = stack[level-1]
        myglobal.num += 1
        return

    choices = choiceSets[0]

    for choice in choices:
        if len(stack) >= level + 1:
            if level == 0:
                stack[level] = []
                stack[level].append(reformatPhrase(choice))
            else:
                stack[level] = copy.deepcopy(stack[level-1])
                stack[level].append(reformatPhrase(choice))
            ltre.append(copy.deepcopy(myglobal._ltre_))
        else:
            stack.append([])
            stack[level] = copy.deepcopy(stack[level-1])
            stack[level].append(reformatPhrase(choice))

            ltre.append(copy.deepcopy(ltre[level-1]))

        # if true, then ddsearch, otherwise, contradition!!!
        if checkContradictionAssumptions(level, stack[level], ltre[level], debugging) == False\
                and withContradictionHandler(level, stack[level], ltre[level], debugging) == False:
            ddSearch(choiceSets[1:], level+1, stack, ltre, debugging)


def withContradictionHandler(level, stack, ltre, debugging=False):
    for assumption in stack:
        tmpEnv = ltre
        #print('assumption => ', assumption)
        #print('tmpEnv => ', tmpEnv)
        assertFact(assumption, tmpEnv)
        runRules(tmpEnv)

        if checkContradictionAssumptions(level, stack, ltre, debugging) == True:
            return True

    return False


def checkContradictionAssumptions(level, stack, ltre, debugging=False):
    #print('level =', level, 'stack =', stack)

    dbclass = getDbClass(':not', ltre)

    flag = False

    for nogoodfacts in dbclass.facts:
        #print('nogoodfact => ', nogoodfacts[1:][0])

        if isinstance(nogoodfacts[1:][0][0], list):
            tmpflag = False
            for nogoodfact in nogoodfacts[1:][0]:
                if nogoodfact not in stack:
                    tmpflag = True
                    break
            if tmpflag == False:
                flag = True
                if debugging:
                    printContradictionInfo(level, stack, nogoodfacts[1:][0])
        else:
            nogoodfact = nogoodfacts[1:][0]
            if nogoodfact in stack:
                flag = True
                if debugging:
                    printContradictionInfo(level, stack, nogoodfact)

        if flag == True:
            break

    return True if flag == True else False


def printContradictionInfo(level, stack, assumption):
    print('=================================================')
    print('Making Contradition!!!!!!')
    print('level = ', level, ' stack = ', stack)
    tmp = [':not']
    tmp.append(assumption)
    print('Assumption:', assumption, ' Facts: ', tmp)


#### Need to be modified!!! Because different phrase has different format!!!!!! ####
def reformatPhrase(choice):
    phrases = []
    for attribute, object in choice.items():
        return parse('('+attribute+' '+object+')')



if __name__ == '__main__':
    #solveCryptarithmeticProblem()

    #choiceSets = solveCryptarithmeticProblem()
    #ddSearch(choiceSets)

    ss = [':not', [['likes-gambling', '?a'], ['likes-animals', '?b']]]
    print(ss[1:][0])

    ss = [':not', ['likes-gambling', '?a']]
    print(ss[1:][0])