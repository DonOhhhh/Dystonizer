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
    def __init__(self, idf, var_type, owner, delegation=None):
        self.identifier = idf
        self.type = var_type
        self.owner = owner
        self.delegation = delegation
        self.key_value = None

    def getIdentifier(self):
        return self.identifier

    def getType(self):
        return self.type

    def getOwner(self):
        return self.owner

    def getDelegation(self):
        return self.delegation

    def setOwner(self, _owner):
        self.owner = _owner

    def setDelegation(self, _del):
        self.delegation = _del

    def setKeyValue(self, key_type, key_owner, value_type, value_owner):
        self.key_value = KeyValue(key_type, key_owner, value_type, value_owner)