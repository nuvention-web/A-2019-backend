from TRE import myglobal
from TRE.lrules import *

class Ltre(object):

    def __init__(self, title=None, dbclassTable={},
                 debugging=False, queue=[],
                 rule_counter=0, rules_run=0):
        self.title = title
        self.dbclassTable = dbclassTable
        self.debugging = debugging
        self.queue = queue
        self.rule_counter = rule_counter
        self.rules_run = rules_run


def inLtre(ltre):
    """
    Set the default ltre to a new value.
    :param ltre:
    :return:
    """
    myglobal._ltre_ = ltre


def createLtre(title, debugging=False):
    """
    :param title:
    :param debugging:
    :return: create a logic-based Tiny Rule Engine
    """
    return Ltre(title=title, dbclassTable={}, debugging=debugging)


def runForms(ltre, forms):
    for form in forms:
        eval(parse(form))
        runRules(ltre)


"""
if __name__ == "__main__":
    inTre(createTre("Ex1"))
    print(myglobal._tre_.title)
"""
