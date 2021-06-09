#!/usr/bin/python

import sys
from parser import Parser
from code import Code
from symboltable import SymbolTable


def symbol_to_16bit(symbol):
    """
    """
    num = int(symbol)
    return "{0:016b}".format(num)


def main():
    """
    Main function. Expect a relative path to the source file. Example /sources/Add.asm
    """
    _file = sys.argv[1]
    file_name = _file.split('.')[-2:-1]
    # Find file name
    file_name = file_name[0].split('/')[-1]
    # Build output path
    output_file_name = "./results/" + file_name + ".hack"
    # Stores the line of the result
    result = []
    # Symbol table reference
    symboltable = SymbolTable()
    # Parser for 1st pass
    parsedpre = Parser(_file)
    parsedpre.advance()
    # 1st Pass, build label references
    while parsedpre.currentCommand:
        if parsedpre.commandType() == "L_COMMAND":
            if not symboltable.contains(parsedpre.symbol()):
                symboltable.addEntry(parsedpre.symbol(),
                                     parsedpre.getCurrentLine())
        parsedpre.advance()
    # Parser for second pass
    parsed = Parser(_file)
    # Code interpreter
    code = Code()
    parsed.advance()
    # 2nd Pass, build result, add variables if necessary
    while parsed.currentCommand:
        if parsed.commandType() == "A_COMMAND":
            if symboltable.contains(parsed.symbol()):
                # Reference exists
                result.append(symbol_to_16bit(
                    symboltable.getAddress(parsed.symbol())))
            else:
                # Reference does not exist
                # Try int conversion
                intvalue = -1
                try:
                    intvalue = int(parsed.symbol())
                except:
                    intvalue = -1
                if intvalue >= 0:
                    # It is an int reference
                    result.append(symbol_to_16bit(intvalue))
                else:
                    # It is a new variable
                    symboltable.addEntryVar(parsed.symbol())
                    result.append(symbol_to_16bit(
                        symboltable.getAddress(parsed.symbol())))
        elif parsed.commandType() == "C_COMMAND":
            # Built binary sequence
            result.append("111" + code.comp(parsed.comp()) +
                          code.dest(parsed.dest()) + code.jump(parsed.jump()))
        parsed.advance()

    # Write output file
    with open(output_file_name, "w") as f:
        for line in result:
            f.write(line + "\n")


def bintest():
    """
    Not relevant
    """
    print(symbol_to_16bit(25000))


if __name__ == "__main__":
    # Example:
    # python main.py /sources/Add.asm
    # result in /results/Add.hack
    main()
