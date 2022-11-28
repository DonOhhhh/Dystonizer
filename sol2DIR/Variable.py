class KeyValue:
    def __init__(self, key_type, key_owner, value_type, value_owner):
        self.key_type = key_type
        self.key_owner = key_owner
        self.value_type = value_type
        self.value_owner = value_owner

    def getKeyOwner(self):
        return self.key_owner

    def getValueOwner(self):
        return self.value_owner

class Variable:
    def __init__(self, _idf=None, _type=None, _owner=None, _del=None):
        self.identifier = _idf
        self.type = _type
        self.owner = _owner
        self.key_value = None
        self.delegetedFrom = _del
        self.constraint = []

    def getIdentifier(self):
        return self.identifier

    def getType(self):
        return self.type

    def getOwner(self):
        return self.owner

    def getDel(self):
        return self.delegetedFrom

    def setIdentifier(self, _idf):
        self.identifier = _idf

    def setType(self, _type):
        self.type = _type

    def setOwner(self, _owner):
        self.owner = _owner

    def setKeyValue(self, key_type, key_owner, value_type, value_owner):
        self.key_value = KeyValue(key_type, key_owner, value_type, value_owner)

    def setDel(self, _del):
        self.delegetedFrom = _del

    def getConstraint(self):
        res = []
        for V in self.constraint:
            res.append(V.getOwner())
        return sorted(res)

    def appendConstraint(self, V):
        self.constraint.append(V)

    def clearConstraint(self):
        self.constraint = []