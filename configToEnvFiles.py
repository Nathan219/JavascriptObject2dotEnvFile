import sys
import string
def parse(inputfile, outputfile, parentprefix):
    line = inputfile.readline()
    if "}" in line and '{' not in line:
        return False
    elif "{" in line and '}' not in line:
        splitparts = string.split(line, ":", 1)
        variable = splitparts[0].upper().strip(' \t\n\r,"')
        parentprefix += variable + "_"
        condition = True
        while condition:
            condition = parse(inputfile, outputfile, parentprefix)
        return True
    elif "[" in line and "]" not in line:
        splitparts = string.split(line, ":", 1)
        variable = splitparts[0].upper().strip(' \t\n\r,"')
        condition = True
        outputfile.write(parentprefix + variable + "=[")
        while condition:
            condition = parseSquareBracket(inputfile, outputfile)
        outputfile.write("]\n")
        return True
    elif ":" in line:
        splitparts = string.split(line, ":", 1)
        variable = parentprefix + splitparts[0].upper().strip(' \t\n\r,"')
        towrite = "{}={}".format(variable, splitparts[1].strip(' \t\n\r,'))
        print(towrite)
        outputfile.write(towrite + "\n")
        return True
    elif line == "":
        return False
    elif "]" in line:
        outputfile.write("]" + "\n")
        return True
    else:
        return True

def parseSquareBracket(inputfile, outputfile):
    line = inputfile.readline()
    if "]" in line:
        return False
    else:
        output = line.strip(' \t\n\r')
        outputfile.write(output)
        return True

Configfile = sys.argv[1]
Outfile = ".env"
if ".json" in Configfile:
    configFilePrefix = string.split(Configfile, "/")
    length= len(configFilePrefix)-1
    configPrefix = string.split(configFilePrefix[length], ".json")
    Outfile = ".env." + configPrefix[0]

try:
    in_file = open(Configfile, 'r')
    out_file = open(Outfile, 'w')
    condition = True
    in_file.readline()
    while condition:
        condition = parse(in_file, out_file, "")



finally:
    in_file.close()
    out_file.close()


