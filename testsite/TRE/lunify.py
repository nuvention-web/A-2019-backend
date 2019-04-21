import numbers

Symbol = str    # A Lisp Symbol is implemented as a Python str

def isVariable(x):
    """
    True if x is a pattern variable
    :param x:
    :return:
    """
    if isinstance(x, Symbol) and x[0] == '?':
        return True
    return False

def unify(a, b, bindings = {}):
    """
    Unify <a> with <b>, returning a new set of bindings if successful, None represents :fail.
    :param a:
    :param b:
    :param bindings:
    :return:
    """
    if bindings == None:
        return None
    elif a == b:
        return bindings
    elif isVariable(a):
        return unifyVariable(a, b, bindings)
    elif isVariable(b):
        return unifyVariable(b, a, bindings)
    elif (not (isinstance(a, list))) or (not (isinstance(b, list))):
        return None
    else:
        if len(a) != len(b):
            return None
        elif len(a) == 1:
            return unify(a[0], b[0], bindings)
        else:
            return unify(a[1:], b[1:], unify(a[0], b[0], bindings))

def unifyVariable(var, exp, bindings):
    """
    Binds variable with value
    :param var:
    :param exp:
    :param bindings:
    :return:
    """
    binding = None
    if var in bindings:
        binding = bindings[var]

    if binding != None:
        return unify(binding, exp, bindings)
    elif freeInVar(var, exp, bindings):
        bindings[var] = exp
        return bindings
    else:
        return None

def freeInVar(var, exp, bindings):
    """
    Returns [] if <var> occurs in <exp>, assuming <bindings>
    :param var:
    :param exp:
    :param bindings:
    :return:
    """
    if isinstance(exp, numbers.Number) or len(exp) == 0:
        return True
    elif var == exp:
        return False
    elif isVariable(exp):
        if exp in bindings:
            return freeInVar(var, bindings[exp], bindings)
        else:
            return True
    elif not isinstance(exp, list):
        return True
    elif freeInVar(var, exp[0], bindings):
        if len(exp) > 1:
            return freeInVar(var, exp[1:], bindings)
        else:
            return True
    else:
        return None

if __name__ == '__main__':

    # Test case #1 - expects None (Fail)
    pat = [['plays-piano', '?a'], ['plays-harp', '?b']]
    obj = [['plays-piano', 'sam'], ['plays-harp', 'sam']]
    print(unify(pat, obj))
    """
    # Test case #2 - expects {'?x': ['a', 'b']}
    pat = '?x'
    obj = ['a', 'b']
    print(unify(pat, obj))
    

    #pat = ['?y', '?x']
    #obj = ['a', 'b']
    #print(unify(pat, obj))

    print(Symbol(0))
    print(isVariable(0))
    """


    a1 = ('a', 'b', '?x')
    print(any(isVariable(a) for a in a1))