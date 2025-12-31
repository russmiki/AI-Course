class UserMemory:
    def __init__(self):
        self.data = {}

    def update(self, key, value):
        self.data[key] = value

    def has(self, key):
        return key in self.data

    def complete(self):
        return all(k in self.data for k in ["goal", "weight", "height", "age"])
