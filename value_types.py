
import enum

# definitions = enum.Enum("definitions", "ANY")
# ANY = definitions.ANY

def typecheck(*arg):
    if len(arg) < 2:
        raise ArgumentError("value types typecheck requires 2 arguments or more.")
    types = arg[:-1]
    value = arg[-1]
    for t in types:
        if typecheck_single(t, value):
            return value
    raise TypeError("--Value Types-- value " + str(value) + ", did not match any of types " + str(types))

def typecheck_single(example, value):
    if example == None: # match anything
        return value
    
    if isinstance(example, str):
        return isinstance(value, str)
    if isinstance(example, int):
        return isinstance(value, int)
    if isinstance(example, float):
        return isinstance(value, float)
    if isinstance(example, complex):
        return isinstance(value, complex)
    
    if isinstance(example, list) or isinstance(example, tuple):
        if (isinstance(example, list) and not isinstance(value, list) or
            isinstance(example, tuple) and not isinstance(value, tuple)):
            return False
        l = len(example)
        if l == 1:
            t = example[0]
            for x in value:
                if not typecheck_single(t, x):
                    return False
            return True
        elif l != len(value):
            return False
        for i in range(l):
            if not typecheck_single(example[i], value[i]):
                return False
        return True

    if isinstance(example, dict):
        if not isinstance(value, dict):
            return False
        has_default = False
        default = None
        if '' in example:
            has_default = True
            default = example['']
        for k in example:
            if k == '':
                continue
            if not k in value:
                return False
            if not typecheck_single(example[k], value[k]):
                return False
        for k in value:
            if not k in example:
                if has_default:
                    if not typecheck_single(default, value[k]):
                        print('default does not match.')
                        return False
                else:
                    return False
        return True
    if isinstance(example, set):
        if not isinstance(value, set):
            return False
        if len(example) == 0:
            return True
        for x in value:
            has_match = False
            for y in example:
                if typecheck_single(y, x):
                    has_match = True
            if not has_match:
                return False
        return True
        
def test():
    T = typecheck
    T(0, 0)
    T(0, 5)
    T(0, -5)
    T(0.0, 3.14159263)
    T('', 'test')
    T([0,0,0], [1,2,3])
    T((0,0,['','']), (1,2,['a','bcde']))
    T({'': 0}, {'a': 1, 'b':2, 'c': 3})
    T({0,'a'}, {1,2,'asdf'})
    print("Value Types tests finished.")
    
    
if __name__ == "__main__":
    test()
