#!/usr/bin/python
from collections import deque


class Parser:
    def __init__(self, filename):
        result_content = deque()
        with open(filename, 'r') as f:
            content = f.readlines()
            for line in content:
                line = str(line).strip()
                if len(line) > 0 and not line.startswith("//"):
                    result_line = line
                    if result_line.find("//") > 0:
                        result_line = str(result_line.split("//")[0]).strip()
                    result_content.append(result_line)
        self.body = result_content
        self.hasMoreComannds = True if len(self.body) > 0 else False
        self._currentLine = 0
        self.currentCommand = None

    def advance(self):
        if self.hasMoreComannds == True:
            if len(self.body) == 1:
                self.hasMoreComannds = False
            self.currentCommand = self.body.popleft()
            if self.commandType() in ["A_COMMAND", "C_COMMAND"]:
                self._currentLine += 1
        else:
            self.currentCommand = None

    def getCurrentLine(self):
        return self._currentLine if self._currentLine >= 0 else 0

    def commandType(self):
        if self.currentCommand:
            if self.currentCommand[0] == "@":
                return "A_COMMAND"
            elif self.currentCommand[0] == "(":
                return "L_COMMAND"
            else:
                return "C_COMMAND"
        return None

    def symbol(self):
        if self.commandType():
            if self.commandType() == "A_COMMAND":
                return self.currentCommand[1:]
            elif self.commandType() == "L_COMMAND":
                return self.currentCommand[1:-1]
        return None

    def dest(self):
        if self.commandType() and self.commandType() == "C_COMMAND":
            if self.currentCommand.find("=") > 0:
                return self.currentCommand[0:self.currentCommand.find('=')]
            else:
                return None
            # if self.currentCommand.find(";") > 0:
            #     dest = self.currentCommand[0:self.currentCommand.find(";")]
            #     return dest if dest != "0" else None
        return None

    def comp(self):
        if self.commandType() and self.commandType() == "C_COMMAND":
            jump_pos = self.currentCommand.find(";")
            dest_pos = self.currentCommand.find("=")
            dest_pos = dest_pos + 1 if dest_pos > 0 else 0
            if jump_pos > 0:
                if dest_pos > 0:
                    return self.currentCommand[dest_pos:jump_pos]
                else:
                    return self.currentCommand[0:jump_pos]
            else:
                return self.currentCommand[dest_pos:]
        return None

    def jump(self):
        if self.commandType() and self.commandType() == "C_COMMAND":
            if self.currentCommand.find(";") > 0:
                return self.currentCommand[self.currentCommand.find(";") + 1:]
        return None

        # if len(self.body) > 0:
        #   line = self.body.popleft()
        # else:

        # with open(output_file_name, "w") as f:
        #     for line in result_content:
        #         f.write(line + "\n")
