
import enum

definitions = enum.Enum("definitions", "ANY")
ANY = definitions.ANY

def typecheck(*arg):
    if len(arg) == 2:
        return typecheck_single(arg[0], arg[1])
    types = arg[:-1]
    value = arg[-1]
    for t in types:
        t = arg[i]
        try:
            return typecheck_single(example, value)
        except:
            pass
    raise TypeError("value_types value:" + str(value) + " types: " + types)

def typecheck_single(example, value):
    if example == None: # match anything
        return value
    example_type = type(example)
    t = type(value)
    
    if example_type is str:
        return t is str
    if example_type is int:
        return isinstance(t, int)
    if example_type is long:
        return isinstance(t, long)
    if example_type is float:
        return isinstance(t, float)
    if example_type is complex:
        return is_instance(t, complex)
    
    if example_type is list:
        if not is_instance(t, list):
            return False
        
     
    
def test():
    pass
    
    
if __name__ == "__main__":
    test()