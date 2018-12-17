import os
import re

def domain (tokens):
    return tokens[0]

def image (tokens):
    return tokens[1]


whitespaceRX = re.compile('[( )\t]+')
def normalizeLine(line):
    line = line.rstrip('\n')
    line = line.strip(' ')

    # replace all whitespaces with a single space
    line = whitespaceRX.sub(' ', line)

    return line


def parseDictionaryExplicit(path, domain, image):
    try:
        if not os.path.exists(path):
            raise IOError

        dct = dict()
        file = open(path, 'r', encoding = 'utf-8')


        for line in file:
            line = normalizeLine (line)

            tokens = line.split(" ", 1)


            key = domain(tokens)
            value = image(tokens)

            if dct.get(key) is None:
                dct[key] = [value]
            else:
                dct[key].append(value)

        return dct

    except IOError as e1:
        print(type(e1), e1)
        print("Could not read file " + path)

    except Exception as e2:
        print(type(e2), e2)


def parse_dictionary (path):
    return parseDictionaryExplicit(path, domain, image)

def parse_dictionary_reverse (path):
    return parseDictionaryExplicit(path, image, domain)

