#!/usr/bin/python

import sys
from parser import Parser
from code import Code
from symboltable import SymbolTable


def symbol_to_16bit(symbol):
    num = int(symbol)
    return "{0:016b}".format(num)


def main():
    _file = sys.argv[1]
    file_name = _file.split('.')[-2:-1]
    # print(file_name)
    file_name = file_name[0].split('/')[-1]
    output_file_name = "./results/" + file_name + ".hack"
    # print(args)
    result = []
    symboltable = SymbolTable()
    parsedpre = Parser(_file)
    parsedpre.advance()
    while parsedpre.currentCommand:
        if parsedpre.commandType() == "L_COMMAND":
            if not symboltable.contains(parsedpre.symbol()):
                symboltable.addEntry(parsedpre.symbol(),
                                     parsedpre.getCurrentLine())
        parsedpre.advance()

    # print(symboltable._values)
    # print(symboltable)

    parsed = Parser(_file)
    code = Code()
    parsed.advance()
    while parsed.currentCommand:
        if parsed.commandType() == "A_COMMAND":
            if symboltable.contains(parsed.symbol()):
                # print(parsed.symbol())
                # print(symboltable.getAddress(parsed.symbol()))
                result.append(symbol_to_16bit(
                    symboltable.getAddress(parsed.symbol())))
            else:
                intvalue = -1
                try:
                    intvalue = int(parsed.symbol())
                except:
                    intvalue = -1
                if intvalue >= 0:
                    result.append(symbol_to_16bit(intvalue))
                else:
                    # It is a new variable
                    symboltable.addEntryVar(parsed.symbol())
                    result.append(symbol_to_16bit(
                        symboltable.getAddress(parsed.symbol())))
        elif parsed.commandType() == "C_COMMAND":
            result.append("111" + code.comp(parsed.comp()) +
                          code.dest(parsed.dest()) + code.jump(parsed.jump()))
        parsed.advance()

    with open(output_file_name, "w") as f:
        for line in result:
            f.write(line + "\n")
        # print(parsed.currentCommand)
        # print(parsed.commandType())
        # print(parsed.symbol())
        # print(parsed.comp())
        # print(parsed.dest())
        # print(parsed.jump())
        # parsed.advance()
        # print("-------------------")


def bintest():
    print(symbol_to_16bit(25000))


if __name__ == "__main__":
    main()
