import sys
import string
import re
import os
def safeVariable(input):
    variable = input.strip(' \t\n\r,"').replace(" ", "")
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', variable)
    variable = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()
    return re.sub(r"[^\w\d]", "_", variable)

def safeword(input):
    variable = input.strip(' \t\n\r,')
    replacement = "\$"
    if re.search(r'^(")', variable):
        replacement = '"' + replacement
    return re.sub(r'^(")?\$', replacement, variable)

def parse(inputfile, outputfile, parentprefix):
    line = inputfile.readline()
    if "}" in line and '{' not in line:
        return False
    elif "{" in line and '}' not in line:
        splitparts = string.split(line, ":", 1)
        variable = safeVariable(splitparts[0])
        parentprefix += variable + "_"
        condition = True
        while condition:
            condition = parse(inputfile, outputfile, parentprefix)
        return True
    elif "[" in line and "]" not in line:
        splitparts = string.split(line, ":", 1)
        variable = safeVariable(splitparts[0])
        line = inputfile.readline()
        outputfile.write(parentprefix + variable + "=[" + safeword(line))
        line = inputfile.readline()
        while "]" not in line:
            outputfile.write("," + safeword(line))
            line = inputfile.readline()
        outputfile.write("]\n")
        return True
    elif ":" in line:
        splitparts = string.split(line, ":", 1)
        variable = parentprefix + safeVariable(splitparts[0])
        towrite = "{}={}".format(variable, safeword(splitparts[1]))
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


def processFile(configfile):
    outfile = ".env"
    if ".json" in configfile:
        configFilePrefix = string.split(configfile, "/")
        length= len(configFilePrefix)-1
        configPrefix = string.split(configFilePrefix[length], ".json")
        outputPath = configFilePrefix[0]
        for x in range(1, length):
            outputPath += "/" + configFilePrefix[x]
        outfile = outputPath + "/.env." + configPrefix[0]
        try:
            in_file = open(configfile, 'r')
            out_file = open(outfile, 'w')
            condition = True
            in_file.readline()
            while condition:
                condition = parse(in_file, out_file, "")
        finally:
            in_file.close()
            out_file.close()
            print "Finished with " + outfile



inputFile = sys.argv[1]

if os.path.isdir(inputFile):
    '''Loop through all of the files'''
    for f in os.listdir(inputFile):
        processFile(inputFile + "/" + f)
else:
    processFile(inputFile)