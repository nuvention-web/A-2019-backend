from TRE import myglobal
from TRE.ltinter import *
import TRE.lrules as rules
from TRE.lunify import *
import warnings

Symbol = str    # A Lisp Symbol is implemented as a Python str
myglobal._lenv_ = None

class DbClass(object):

    def __init__(self, name=None, ltre=None, facts=[], rules=[], notFacts=[]):
        self.name = name
        self.ltre = ltre
        self.facts = facts
        self.rules = rules
        self.notFacts = notFacts

def showData():
    """
    Print out whole facts
    :return: counter
    """
    counter = 0
    for key,dbclass in myglobal._ltre_.dbclassTable.items():
        for datum in dbclass.facts:
            counter += 1
            print("Fact #", counter, "=>", datum)
    return counter

def getDbClass(fact, ltre, flag=0):
    if fact == None:
        warnings.warn("nil can't be a dbclass!")
    elif isinstance(fact, list) and (not isinstance(fact[0], list)) and flag == 0:
        return getDbClass(fact[0], ltre, flag)
    elif len(fact) > 1 and isinstance(fact[0], list):
        tmpLst = []
        flag = 1    # means need to construct tuple used as dbclass name
        # assume that only will appear secondary level list
        for lst in fact:
            tmpLst.append(lst[0])
        return getDbClass(tuple(tmpLst), ltre, flag)
    else:
        dbclass = ltre.dbclassTable[fact] if fact in ltre.dbclassTable else None
        if dbclass != None:
            return dbclass
        else:
            dbclass = DbClass(name=fact, ltre=ltre, facts=[], rules=[], notFacts=[])
            ltre.dbclassTable[fact] = dbclass
            return dbclass

def getCandidates(pattern, ltre=None):
    """
    Retrieve all facts from the dbclass of a given pattern
    :param pattern:
    :param ltre:
    :return:
    """
    #print('pattern => ', pattern)
    #print('getDbclass => ', getDbClass(pattern, ltre).name)

    if ltre == None:
        ltre = myglobal._ltre_

    dbclass = getDbClass(pattern, ltre)

    facts = []
    if isinstance(dbclass.name, tuple):
        idx = 0
        for item in dbclass.name:
            facts.append([])

        for item in dbclass.name:
            # if it starts with '?', then retrieve all the facts,
            # because we don't know which one to match
            if isVariable(item):
                for key, dbclass in ltre.dbclassTable.items():
                    for datum in dbclass.facts:
                        facts[idx].append(datum)

            else:
                for fact in getDbClass(item, ltre).facts:
                    facts[idx].append(fact)
            idx += 1

        return facts
    else:
        return getDbClass(pattern, ltre).facts

# Installing new facts
def assertFact(fact, ltre=None):
    if ltre == None:
        ltre = myglobal._ltre_

    #print('assertFact fact = ', fact)

    #### Store the False facts explicitly (like false node)
    if fact[0] == ':not':
        if insertNoGoodFact(fact[1:][0], ltre) == True:
            rules.tryRules(fact, ltre)

    if insertFact(fact, ltre) == True:     # When it isn't already there
        rules.tryRules(fact, ltre)               # run the rules on it

def insertFact(fact, ltre):
    """
    Insert a single fact into the database
    :param fact:
    :param ltre:
    :return:
    """
    dbclass = getDbClass(fact, ltre)
    if fact not in dbclass.facts:
        if ltre.debugging:
            print(ltre, 'Inserting',fact,'into database.')
        dbclass.facts.append(fact)
        return True
    return False

def insertNoGoodFact(nogoodfact, ltre):
    """
    Insert a single not fact into the database
    :param nogoodfact:
    :param ltre:
    :return:
    """
    dbclass = getDbClass(nogoodfact, ltre)
    if nogoodfact not in dbclass.notFacts:
        if ltre.debugging:
            print(ltre, 'Inserting',nogoodfact,'into database.')
        dbclass.notFacts.append(nogoodfact)
        return True
    return False

if __name__ == '__main__':
    a = [1,3,4]
    b = [[1,2,3], [1,3,4]]
    print(a in b)