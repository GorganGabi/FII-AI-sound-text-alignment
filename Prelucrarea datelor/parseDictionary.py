import os


def parse_dictionary(path):
    try:
        if not os.path.exists(path):
            raise IOError

        dct = dict()
        file = open(path)
        for line in file:
            line = line.rstrip('\n')
            tokens = line.split(" ", 1)
            tokens[1] = tokens[1].replace(" ", "", 1)
            if dct.get(tokens[1]) is None:
                dct[tokens[1]] = [tokens[0]]
            else:
                dct[tokens[1]].append(tokens[0])
        return dct

    except IOError as e1:
        print(type(e1), e1)
        print("Could not read file " + path)
    except Exception as e2:
        print(type(e2), e2)