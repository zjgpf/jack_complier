FIELD = 'field'
STATIC = 'static'
ARG = 'argument'
LOCAL = 'local'

def find(table, name):
    for _kind in table:
        for i,_obj in enumerate(table[_kind]):
            if _obj['name'] == name:
                return {'kind':_kind,'index':i,'type':_obj['type']}
    return None

class SymbolTable:

    def __init__(self):
        self.table_class = {FIELD:[],STATIC:[]}
        self.table_subroutine = {ARG:[],LOCAL:[]}

    '''
    Starts a new subroutine scope(i.e., reset subroutine's symbol table)
    '''
    def startSubroutine(self):
        self.table_subroutine = {ARG:[],LOCAL:[]}

    '''
    Defines a new identifier of given name, type, and kind, and assigns it a running index.
    STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.
    '''
    def define(self, _name, _type, _kind):
        if _kind in [ARG, LOCAL]:
            self.table_subroutine[_kind] += [{'name':_name,'type':_type}]
        elif _kind in [FIELD, STATIC]:
            self.table_class[_kind] += [{'name':_name,'type':_type}]
        else:
            raise Expection(f"Unexpected kind ${_kind}")
        

    '''
    Returns the number of variables of the given kind already defined in current scope.
    '''
    def varCount(self, _kind):
        if _kind in [ARG, LOCAL]:
            return len(self.table_subroutine[_kind])
        elif _kind in [FIELD, STATIC]:
            return len(self.table_class[_kind])
        else:
            raise Expection(f"Unexpected kind ${_kind}")

    '''
    Returns the kind of named identifier in the current scope. If the identifier is unknown in the current scope, returns None
    '''
    def kindOf(self, _name):
        ret = find(self.table_subroutine, _name)
        if not ret:
            ret = find(self.table_class, _name)
        if not ret: return None
        else: return ret._kind

    def typeOf(self, _name):
        ret = find(self.table_subroutine, _name)
        if not ret:
            ret = find(self.table_class, _name)
        if not ret: return None
        else: return ret._type

    def indexOf(self, _name):
        ret = find(self.table_subroutine, _name)
        if not ret:
            ret = find(self.table_class, _name)
        if not ret: return None
        else: return ret._index
