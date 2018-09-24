from os import popen

def command(instr):
    return popen(instr).read()
