#!/usr/bin/python

class SymbolTable():
    def __init__(self):
        self._table = {"SP": 0,
                       "LCL": 1,
                       "ARG": 2,
                       "THIS": 3,
                       "THAT": 4,
                       "R0": 0,
                       "R1": 1,
                       "R2": 2,
                       "R3": 3,
                       "R4": 4,
                       "R5": 5,
                       "R6": 6,
                       "R7": 7,
                       "R8": 8,
                       "R9": 9,
                       "R10": 10,
                       "R11": 11,
                       "R12": 12,
                       "R13": 13,
                       "R14": 14,
                       "R15": 15,
                       "SCREEN": 16384,
                       "KEYBOARD": 24576}
        self._values = {}
        self.counter = 16

    def addEntry(self, name, address):
        # self._table[name] = self.counter
        self._values[name] = address
        #self.counter += 1

    def addEntryVar(self, name):
        self._table[name] = self.counter
        self.counter += 1

    def contains(self, name):
        return name in self._table or name in self._values

    def getAddress(self, name):
        if name in self._table:
            return self._table.get(name, None)
        return self._values.get(name, None)
