
import enum

definitions = enum.Enum("definitions", "ANY")
ANY = definitions.ANY
OPTIONAL_PROPERTY_PREFIX = "$"
DEFAULT_VALUE_KEY = ""

def typecheck(*arg):
    if len(arg) < 2:
        return
    if len(arg) == 2:
        check_result = typecheck_single(arg[0], arg[1])
        if check_result == True:
            return arg[1]
        else:
            raise TypeError("For value: " + str(arg[0]) + "\n  " + str(check_result[0]) + ". type: " + str(check_result[1]) + ", value: " + str(check_result[2]) + ";")

    types = arg[:-1]
    value = arg[-1]
    check_errors = []
    check_types = []
    check_value = None
    for t in types:
        check_result = typecheck_single(t, value)
        if check_result == True:
            return value
        check_errors.append(check_result[0])
        check_types.append(check_result[1])
        check_value = check_result[2]
    raise TypeError("\n  types: " + str(types) + "\n  value: " + str(value) + "\n  errors: " + str(check_errors) )

# returns True | (error_string, type, value)
def typecheck_single(example, value, type_path = ""):
    if example == None: # match anything
        return True
    example_type = type(example)
    
    def err_msg(s, x=example, y=value):
        return ("At path " + type_path + ": " + s if len(type_path) else s, x, y)

    if isinstance(example, str):
        return True if isinstance(value, str) else err_msg("Not a string")
    if isinstance(example, int):
        return True if isinstance(value, int) else err_msg("Not an int")
    if isinstance(example, float):
        return True if isinstance(value, float) else err_msg("Not a float")
    if isinstance(example, complex):
        return True if isinstance(value, complex) else err_msg("Not a complex value")
    
    # tuple
    if isinstance(example, tuple):
        if not isinstance(value, tuple):
            return err_msg("Not a tuple")
        if len(value) != len(example):
            return err_msg("Tuple wrong length")
        for i in range(len(example)):
            check_result = typecheck_single(example[i], value[i], type_path + "[" + str(i) + "]")
            if check_result != True:
                return check_result
        return True

    # list
    if isinstance(example, list):
        if not isinstance(value, list):
            return err_msg("Not a list")
        if len(example) == 1:
            for i in range(len(value)):
                x = value[i]
                check_result = typecheck_single(example[0], x, type_path + "[" + str(i) + "]")
                if check_result != True:
                    return check_result
            return True
        elif len(example) != len(value):
            return err_msg("List wrong length")
        else:
            for i in range(len(example)):
                t = example[i]
                x = value[i]
                check_result = typecheck_single(t, x, type_path + "[" + str(i) + "]")
                if check_result != True:
                    return check_result
        return True
    
    # set
    if isinstance(example, set):
        if not isinstance(value, set):
            return err_msg("Not a set")
            # if len(example) > 1:
            #     return err_msg("Set type example should have at most 1 value.")
        for x in value:
            has_match = False
            for entry in example:
                check_result = typecheck_single(entry, x, type_path + "{}")
                if check_result == True:
                    has_match = True
                    break
            if not has_match:
                return err_msg("No matching set example entry.")
        return True
    
    # dictionaries
    if isinstance(example, dict):
        if not isinstance(value, dict):
            return err_msg("Not a dict")
        has_default = False
        default_type = None
        for k in example:
            if k == DEFAULT_VALUE_KEY:
                has_default = True
                default_type = example[k]
        variant_matches = {}
        for k in value:
            new_type_path = type_path + "['" + str(k) + "']"
            prefix_key = OPTIONAL_PROPERTY_PREFIX + k
            has_variant = False
            variant_match = False
            while prefix_key in example:
                has_variant = True
                check_result = typecheck_single(example[prefix_key], value[k], new_type_path)
                if check_result == True:
                    variant_match = True
                prefix_key = OPTIONAL_PROPERTY_PREFIX + prefix_key
            if variant_match:
                continue
            if not k in example:
                if has_variant: #variant_match must be false to get here.
                    return err_msg("Property did not match any variant '" + str(k) + "'")
                elif has_default:
                    check_result = typecheck_single(default_type, value[k], new_type_path)
                    if check_result != True:
                        return check_result
                else:
                    return err_msg("Unknown property '" + str(k) + "'")
            else:
                check_result = typecheck_single(example[k], value[k], new_type_path)
                if check_result != True:
                    return check_result
        for k in example:
            if k == '':
                continue
            if not k in value:
                pre_len = len(OPTIONAL_PROPERTY_PREFIX)
                if len(k) < pre_len or k[:pre_len] != OPTIONAL_PROPERTY_PREFIX:
                    return err_msg("Missing property '" + str(k) + "'")
        return True
#TODO sets

def expectTypeError(code, test_name=None):
    code = "T(" + code + ")"
    try:
        T = typecheck
        eval(code)
    except TypeError:
        return
    if test_name == None:
        test_name = code
    raise TypeError("Expected type error for test: '" + test_name + "'")


def test():
    T = typecheck
    TE = expectTypeError
    T(0, 5)
    T(5, 0)
    T(0.0, 5.0)
    T(-5, 0)
    T(0, -5)
    TE(" 0.0, 0 ")
    TE(" 0, 99.0 ")
    TE(" '', 0 ")
    TE(" 0, '' ")
    TE(" 0.0, int(0.0)")
    TE("0, 99.0")
    TE(" '', [0,0,[0],0], [1,2,[3.0], 4]")
    T((0,0,0), (1,2,3))
    T((), ())
    T({'',0}, {'a', 'b', 'c', 1, 2, 3})
    TE("{'',0}, {'a', 'b', 'c', 1, 2, 3.0}")
    T({'': ('',''),}, {'test': ('a', 'b')})
    TE("{'': ('',''), '$test': (1, 2)}, {'test': ('a', 'b')}")
    T({'': ('',''), '$test': (1, 2)}, {})
    TE("(0), (99.0)")
    # T()
    
    
if __name__ == "__main__":
    test()
    print("Tests finished.")
