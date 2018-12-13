import os
import sys

print("Running Python {}".format(sys.version_info))

from pocketsphinx import AudioFile, get_model_path, get_data_path


help = """Arguments for console usage:
-h\tShow this
-p <file_path>\tExtract phonemes
-w <file_path>\tExtract words

Example: transform_audio.py -p sample1.raw -model=it -d
"""


def get_phonemes_from_file(file_path, detailed=False, model='en-us'):
    """
    :param file_path: path to audio file (must be raw 16khz 16bit)
    :param detailed: False - (default) return only phonemes; True - return tuples (phoneme, start_frame, end_frame)
    :param model: specify language model
    :return: a list of phrases made of phonemes/tuples
    """

    model_path = get_model_path()
    data_path = get_data_path()

    config = {
        'verbose': False,
        'audio_file': file_path,
        'buffer_size': 2048,
        'no_search': False,
        'full_utt': False,
        'hmm': os.path.join(model_path, model),
        'allphone': os.path.join(model_path, 'phone.lm.dmp'),
        'beam': 1e-20,
        'pbeam': 1e-20,
        'lw': 2.0
    }

    audio = AudioFile(**config)

    phrases = []

    for phrase in audio:
        phrases.append(phrase.segments(detailed=detailed))

    if detailed:

        detailed_phrases = []

        for phrase in phrases:

            detailed_phrase = []

            for p in phrase:
                d = (p[0], p[2], p[3])
                detailed_phrase.append(d)
            detailed_phrases.append(detailed_phrase)

        return detailed_phrases

    return phrases


def get_words_from_file(file_path, detailed=False, model='en-us'):
    """
    :param file_path: audio file (must be raw 16khz 16bit)
    :param detailed: False - (default) return only phonemes; True - return tuples (phoneme, start_frame, end_frame)
    :param model: specify language model
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
        'hmm': os.path.join(model_path, model),
        'lm': os.path.join(model_path, '{}.lm.bin'.format(model)),
        'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    }

    audio = AudioFile(**config)

    phrases = []

    for phrase in audio:
        phrases.append(phrase.segments(detailed=detailed))

    if detailed:

        detailed_phrases = []

        for phrase in phrases:

            detailed_phrase = []

            for p in phrase:
                d = (p[0], p[2], p[3])
                detailed_phrase.append(d)
            detailed_phrases.append(detailed_phrase)

        return detailed_phrases

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

        model='en-us'
        for arg in sys.argv:
            if arg.startswith('-model='):
                model = arg.split('=')[1]

        detailed=False
        if '-d' in sys.argv:
            detailed=True

        if os.path.exists(sys.argv[2]) and os.path.isfile(sys.argv[2]):
            phrases = f(sys.argv[2], detailed=detailed, model=model)
            for phrase in phrases:
                print(phrase)
        else:
            print("Invalid file.")

        exit(0)

    print("No command given. Use the -h argument to view available commands.")