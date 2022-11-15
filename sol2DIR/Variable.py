class Variable:
    def __init__(self, ID, var_type, owner):
        self.identifier = ID
        self.type = var_type
        self.owner = owner
        self.delegation = owner

    def getIdentifier(self):
        return self.identifier

    def getType(self):
        return self.type

    def getOwner(self):
        return self.owner

    def getDelegation(self):
        return self.delegation

    def setDelegation(self, owner, delegated):
        if self.owner == owner:
            self.delegation = delegated
