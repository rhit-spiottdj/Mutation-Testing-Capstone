from enum import Enum

class NodeType(Enum):
    ADD = 1
    ADDASSIGN = 2
    SUBTRACT = 3
    SUBTRACTASSIGN = 4
    MULTIPLY = 5
    MULTIPLYASSIGN = 6
    DIVIDE = 7
    DIVIDEASSIGN = 8
    MODULO = 9
    MODULOASSIGN = 10
    BITAND = 11
    BITOR = 12
    POWER = 13
    LESSTHAN = 14
    GREATERTHAN = 15
    EQUAL = 16
    NOTEQUAL = 17
    LESSTHANEQUAL = 18
    GREATERTHANEQUAL = 19
    CLASS = 20
    METHOD = 21
    VARIABLE = 22
    ASSIGN = 23
    VALUE = 24

NodeType = Enum('NodeType', [('ADD', 1), ('ADDASSIGN', 2), ('SUBTRACT', 3), ('SUBTRACTASSIGN', 4), ('MULTIPLY', 5), ('MULIPLYASSIGN', 6), 
                            ('DIVIDE', 7), ('DIVIDEASSIGN', 8), ('MODULO', 9), ('MODULOASSIGN', 10),  ('BITAND', 11), ('BITOR', 12), ('POWER', 13), 
                            ('LESSTHAN', 14), ('GREATERTHAN', 15), ('EQUAL', 16), ('NOTEQUAL', 17), ('LESSTHANEQUAL', 18), ('GREATERTHANEQUAL', 19), 
                            ('CLASS', 20), ('METHOD', 21), ('VARIABLE', 22), ('ASSIGN', 23), ('VALUE', 24)])