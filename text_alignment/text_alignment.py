import argparse
import os
import json
import re
import sys
from unidecode import unidecode
import codecs
import treetaggerwrapper
import strgen
import subprocess

sys.path.insert(0, '..\\audio_to_phonemes')

from transform_audio import get_words_from_file_experimental

TREE_TAGGER_PATH = r"C:\TreeTagger\bin\tree-tagger.exe"
ROMANIAN_PAR_PATH = r"C:\TreeTagger\lib\romanian-utf8.par"


def create_parser():
    parser = argparse.ArgumentParser(description="Parse args for text alignment script.")
    # parser.add_argument('-rec', '--recongnized', help='path to the first file to be aligned')
    parser.add_argument('-rec', '--recording', help='path to the audio file')
    parser.add_argument('-orig', '--original', help='path to the second file to be aligned')
    parser.add_argument('-out', '--output', help='path to the final alignment (result alignment file)')
    parser.add_argument('-m', '--model', help='the model used by the voice recognition model', default='en-us')
    parser.add_argument('-l', '--lemma', help='use lemmas of words in the alignment algorithm', action='store_true')

    return parser


def get_args(parser):
    args = parser.parse_args()
    return [args.recording, args.original, args.output, args.model, args.lemma]


def align(text1, text2, gap_penalty, mismatch_penalty):
    m = len(text1)
    n = len(text2)

    table = []
    for i in range(n + m + 1):
        row = []
        for j in range(n + m + 1):
            row.append(0)
        table.append(row)

    for i in range(n + m + 1):
        table[i][0] = i * gap_penalty
    for j in range(n + m + 1):
        table[0][j] = j * gap_penalty

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j - 1] + mismatch_penalty,
                                  table[i - 1][j] + gap_penalty,
                                  table[i][j - 1] + gap_penalty)

    # reconstructie
    max_length = n + m
    i = m
    j = n
    xpos = max_length
    ypos = max_length
    xans = [-1 for x in range(max_length + 1)]
    yans = [-1 for x in range(max_length + 1)]

    while not (i == 0 or j == 0):
        if text1[i - 1] == text2[j - 1]:
            xans[xpos] = text1[i - 1]
            yans[ypos] = text2[j - 1]
            xpos = xpos - 1
            ypos = ypos - 1
            i = i - 1
            j = j - 1
        elif (table[i - 1][j - 1] + mismatch_penalty) == table[i][j]:
            xans[xpos] = text1[i - 1]
            yans[ypos] = text2[j - 1]
            xpos = xpos - 1
            ypos = ypos - 1
            i = i - 1
            j = j - 1
        elif (table[i - 1][j] + gap_penalty) == table[i][j]:
            xans[xpos] = text1[i - 1]
            yans[ypos] = '_'
            xpos = xpos - 1
            ypos = ypos - 1
            i = i - 1
        elif (table[i][j - 1] + gap_penalty) == table[i][j]:
            xans[xpos] = '_'
            yans[ypos] = text2[j - 1]
            xpos = xpos - 1
            ypos = ypos - 1
            j = j - 1

    while xpos > 0:
        if i > 0:
            i = i - 1
            xans[xpos] = text1[i]
            xpos = xpos - 1
        else:
            xans[xpos] = '_'
            xpos = xpos - 1

    while ypos > 0:
        if j > 0:
            j = j - 1
            yans[ypos] = text2[j]
            ypos = ypos - 1
        else:
            yans[ypos] = '_'
            ypos = ypos - 1

    id = 1
    for i in range(max_length, 0, -1):
        if yans[i] == '_' and xans[i] == '_':
            id = i + 1
            break

    res = list()
    res.append(xans[id:])
    res.append(yans[id:])
    return res


def remove_diacritics(file):
    text = []
    with codecs.open(file, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            text.append(unidecode(line))
    return "".join(text)


def remove_word_diacritics(word):
    diacritics_dict = {'ș': 's', 'ț': 't', 'î': 'i', 'ă': 'a', 'â': 'a'}
    new_word = word
    for diac in diacritics_dict:
        try:
            while diac in word:
                diac_poz = new_word.index(diac)
                new_word = new_word[0:diac_poz] + diacritics_dict[diac] + new_word[diac_poz + 1:]
        except:
            pass
    return new_word


def dict_is_ok(input_dict):
    if "<" in input_dict["word"]:
        return False
    return True


def remove_word_number(input_dict):
    new_dict = input_dict
    if "(" in new_dict["word"]:
        paranthesis_pos = new_dict["word"].index("(")
        new_dict["word"] = new_dict["word"][:paranthesis_pos]

    return new_dict


def get_lists(arguments):
    if arguments.count(None) != 0:
        print("Missing arguments!")
        return []

    if not os.path.exists(arguments[0]):
        print("The path for file1 does not exits!")
        return []

    if not os.path.exists(arguments[1]):
        print("The path for file2 does not exits!")
        return []

    '''
    file1 = open(arguments[0], "r")
    file1_data = json.load(file1)
    file1_data = [remove_word_number(elem) for elem in file1_data if dict_is_ok(elem)]
    word_list1 = [elem["word"] for elem in file1_data]
    '''
    file1_data = get_words_from_file_experimental(arguments[0], detailed=True, model=arguments[3])
    file1_data = [remove_word_number(elem) for elem in file1_data if dict_is_ok(elem)]
    word_list1 = [elem["word"] for elem in file1_data]

    file2 = open(arguments[1], "rb")
    word_list2 = []
    for line in file2:
        line = line.decode()
        line_word_list = [x for x in re.split(",|\s+|\.|;|:|\*+|\n", line) if x]
        word_list2.extend(line_word_list)

    word_list1 = [word.lower() for word in word_list1]
    word_list1 = [remove_word_diacritics(word) for word in word_list1]
    word_list2 = [word.lower() for word in word_list2]
    word_list2 = [remove_word_diacritics(word) for word in word_list2]

    return [word_list1, word_list2, file1_data]


def create_result_dictionary(alignment_res, word_lists, arguments):
    align_list1 = alignment_res[0]
    align_list2 = alignment_res[1]
    dict_list = word_lists[2]

    res_dict_list = []
    nr_blanks1 = 0

    for i in range(len(align_list1)):
        if align_list1[i] == align_list2[i]:
            word_dict = dict()
            word_dict["end"] = dict_list[i - nr_blanks1]["end"]
            word_dict["start"] = dict_list[i - nr_blanks1]["start"]
            word_dict["word"] = align_list1[i - nr_blanks1]
            word_dict["matched"] = 1
            res_dict_list.append(word_dict)
        elif align_list1[i] == "_":
            nr_blanks1 = nr_blanks1 + 1
        else:
            word_dict = dict()
            word_dict["end"] = dict_list[i - nr_blanks1]["end"]
            word_dict["start"] = dict_list[i - nr_blanks1]["start"]
            word_dict["word"] = align_list1[i - nr_blanks1]
            word_dict["matched"] = 0
            res_dict_list.append(word_dict)

    outfile = open(arguments[2], "w")
    outfile.write(json.dumps(res_dict_list))


def get_english_lemmas(orig_list):
    lemma_list = []
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')

    for word in orig_list:
        tag = tagger.tag_text(word)
        tag_object = treetaggerwrapper.make_tags(tag)
        lemma_list.append(tag_object[0].lemma)

    return lemma_list


def get_romanian_lemmas(orig_list):
    lemma_list = []

    random_string = strgen.StringGenerator("[\d\w]{10}").render()
    input_file_name = random_string + ".input"
    output_file_name = random_string + ".output"

    input_file_handle = open(input_file_name, 'w')

    for word in orig_list:
        input_file_handle.write(word + '\n')

    input_file_handle.close()
    subprocess.call([TREE_TAGGER_PATH, "-lemma", ROMANIAN_PAR_PATH, input_file_name, output_file_name])

    output_file_handle = open(output_file_name, 'r')

    i = 0
    for line in output_file_handle:
        lemma = line.split()[1]

        if lemma == '<unknown>':
            lemma_list.append(orig_list[i])
        else:
            lemma_list.append(lemma)

        i = i + 1

    output_file_handle.close()

    os.remove(input_file_name)
    os.remove(output_file_name)

    return lemma_list


def run_simple_align(arguments):
    gap_penalty = -2
    mismatch_penalty = -3
    word_lists = get_lists(arguments)
    # word_lists = [["ana", "șade", "bine", "la", "soare"],["ana", "șade", "la", "umbră"]]

    if word_lists:
        alignment_res = align(word_lists[0], word_lists[1], gap_penalty, mismatch_penalty)
        create_result_dictionary(alignment_res, word_lists, arguments)
        print(alignment_res)


# create_result_dictionary(alignment_res, word_lists, arguments)


def run_lemma_align(arguments):
    gap_penalty = -2
    mismatch_penalty = -3
    word_lists = get_lists(arguments)

    if arguments[3] == "en-us":
        get_lemma_list = lambda list: get_english_lemmas(list)
    else:
        get_lemma_list = lambda list: get_romanian_lemmas(list)

    lemma_list1 = get_lemma_list(word_lists[0])
    lemma_list2 = get_lemma_list(word_lists[1])
    if word_lists:
        alignment_res = align(lemma_list1, lemma_list2, gap_penalty, mismatch_penalty)
        create_result_dictionary(alignment_res, word_lists, arguments)


if __name__ == '__main__':
    parser = create_parser()
    arguments = get_args(parser)

    if not arguments[4]:
        run_simple_align(arguments)
    else:
        run_lemma_align(arguments)
