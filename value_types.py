
import enum

definitions = enum.Enum("definitions", "ANY")
ANY = definitions.ANY

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
    print("Value Types tests finished.")
    
    
if __name__ == "__main__":
    test()
