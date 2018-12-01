import os
import sys
from pocketsphinx import AudioFile, get_model_path, get_data_path


help = """Arguments for console usage:
-h\tShow this
-p <file_path>\tExtract phonemes
-w <file_path>\tExtract words
"""


def get_phonemes_from_file(file_path):
    """
    :param file_path: audio file (must be raw 16khz 16bit)
    :return: a list of phrases made of phonemes
    """

    model_path = get_model_path()
    data_path = get_data_path()

    config = {
        'verbose': False,
        'audio_file': file_path,
        'buffer_size': 2048,
        'no_search': False,
        'full_utt': False,
        'hmm': os.path.join(model_path, 'en-us'),
        'allphone': os.path.join(model_path, 'en-us/en-us-phone.lm.dmp'),
        'beam': 1e-20,
        'pbeam': 1e-20,
        'lw': 2.0
    }

    audio = AudioFile(**config)

    phrases = []

    for phrase in audio:
        phrases.append(str(phrase))

    return phrases


def get_words_from_file(file_path):
    """
    :param file_path: audio file (must be raw 16khz 16bit)
    :return: a list of phrases made of words
    """

    model_path = get_model_path()
    data_path = get_data_path()

    config = {
        'verbose': False,
        'audio_file': file_path,
        'buffer_size': 2048,
        'no_search': False,
        'full_utt': False,
        'hmm': os.path.join(model_path, 'en-us'),
        'lm': os.path.join(model_path, 'en-us.lm.bin'),
        'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    }

    audio = AudioFile(**config)

    phrases = []

    for phrase in audio:
        phrases.append(str(phrase))

    return phrases


if __name__ == "__main__":

    if len(sys.argv) > 1:

        if sys.argv[1] == '-h':
            print(help)
            exit(0)

    if len(sys.argv) > 2:
        f = None

        if sys.argv[1] == '-p':
            f = get_phonemes_from_file
        if sys.argv[1] == '-w':
            f = get_words_from_file

        if f is None:
            exit(0)

        if os.path.exists(sys.argv[2]) and os.path.isfile(sys.argv[2]):
            phrases = f(sys.argv[2])
            for phrase in phrases:
                print(phrase)
        else:
            print("Invalid file.")

        exit(0)

    print("No command given. Use the -h argument to view available commands.")