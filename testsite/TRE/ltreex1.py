from TRE.dds import *

_attributes_ = ['plays-piano', 'plays-harp', 'smooth-talker', 'likes-gambling', 'likes-animals']
_objects_ = ['groucho', 'harpo', 'chico']

_attributes_ = ['jacket', 'pants']
_objects_ = ['red', 'black', 'green']

def makeAttributeChoiceSets(attributes, objects):
    """
    Each attribute is assumed to apply to exactly one of the objects
    :param attributes:
    :param objects:
    :return:
    """
    choiceSets = []
    for attribute in attributes:
        attributeSet = []
        for object in objects:
            attributeSet.append({attribute : object})
        choiceSets.append(attributeSet)
    return choiceSets

def ex1 (debugging = False):
    inLtre(createLtre(title="Ex1", debugging = debugging))
    forms = ['(rassert! (:not (plays-piano plays-harp)))',
             '(rassert! (:not (plays-piano smooth-talker)))',
             '(rassert! (:not (plays-harp smooth-talker)))',
             '(rassert! (:not (likes-money likes-gambling)))',
             '(rassert! (:not (likes-gambling likes-animals)))',
             '(rassert! (:not (smooth-talker likes-gambling)))',
             '(rassert! (same-entity likes-animals plays-harp))',
             '(rassert! (:not (likes-animals groucho)))',
             '(rassert! (:not (smooth-talker harpo)))',
             '(rassert! (plays-piano chico))',
             '(rule ((:not (?attribute1 ?attribute2)) (?attribute1 ?obj) (?attribute2 ?obj)) (rassert! (:not (:and (:not (?attribute1 ?attribute2)) (?attribute1 ?obj) (?attribute2 ?obj)))))']

    forms = [
        '(rassert! (plays-piano sally))',
        '(rassert! (plays-harp sally))',
        '(rule ((plays-piano ?a) (plays-harp ?b)) (when (eql ?a ?b) (rassert! (:not (:and (plays-piano ?a) (plays-harp ?b))))))']

    #runForms(myglobal._ltre_, forms)


    ### These rules and facts are the finally ones!!!
    forms = [
        '(rule ((plays-piano ?a) (plays-harp ?b)) (when (eql ?a ?b) (rassert! (:not ((plays-piano ?a) (plays-harp ?b))))))',
        '(rule ((plays-piano ?a) (smooth-talker ?b)) (when (eql ?a ?b) (rassert! (:not ((plays-piano ?a) (smooth-talker ?b))))))',
        '(rule ((plays-harp ?a) (smooth-talker ?b)) (when (eql ?a ?b) (rassert! (:not ((plays-harp ?a) (smooth-talker ?b))))))',
        '(rule ((likes-money ?a) (likes-gambling ?b)) (when (eql ?a ?b) (rassert! (:not ((likes-money ?a) (likes-gambling ?b))))))',
        '(rule ((likes-gambling ?a) (likes-animals ?b)) (when (eql ?a ?b) (rassert! (:not ((likes-gambling ?a) (likes-animals ?b))))))',
        '(rule ((smooth-talker ?a) (likes-gambling ?b)) (when (eql ?a ?b) (rassert! (:not ((smooth-talker ?a) (likes-gambling ?b))))))',
        '(rassert! (same-entity likes-animals plays-harp))',
        '(rassert! (:not (likes-animals groucho)))',
        '(rassert! (:not (smooth-talker harpo)))',
        '(rassert! (plays-piano chico))',
        '(rule ((same-entity ?a1 ?a2) (?a1 ?obj)) (rassert! (:implies ((same-entity ?a1 ?a2) (?a1 ?obj)) (?a2 ?obj))))',
        '(rassert! (likes-animals chico))',
    ]

    forms = [
        '(rassert! (:not ((jacket red) (pants green))))',
        '(rassert! (:not ((jacket green) (pants red))))'
    ]

    runForms(myglobal._ltre_, forms)

    # ddSearch & making Choice Sets
    choiceSets = makeAttributeChoiceSets(_attributes_, _objects_)
    #print(choiceSets)

    myglobal.num = 0
    myglobal.ans = {}
    ddSearch(choiceSets)
    return myglobal.ans

    # ============ Test for get not dbclass facts
    #dbclass = getDbClass('plays-piano', myglobal._ltre_)
    #for data in dbclass.notFacts:
    #    print(data)


def repl(prompt='ltre.py> '):
    """
    A prompt-read-eval-print loop.
    :param prompt:
    :return:
    """
    while True:
        val = input(prompt)
        if val == 'ex1()':
            ex1()
        elif val == 'ex1(True)':
            ex1(True)
        elif val == 'showRules()':
            showRules()
        elif val == 'showData()':
            showData()



if __name__ == '__main__':

    print(makeAttributeChoiceSets(attributes=_attributes_, objects=_objects_))

    ex1()

    #print('======== Show Rules ========')
    #showRules()
    #print('======== Show Facts ========')
    #showData()

    #repl()
