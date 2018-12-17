import os
import sys

print("Running Python {}".format(sys.version_info))

from pocketsphinx import AudioFile, get_model_path, get_data_path
from transform_audio_configs import configuration


help = """Arguments for console usage:
-h\tShow this
-p <file_path>\tExtract phonemes
-w <file_path>\tExtract words

Example: transform_audio.py -p sample1.raw -model=it -d
"""


def get_phonemes_from_file(file_path, detailed=False, model='en-us'):
    """
    :param file_path: path to audio file (must be raw 16khz 16bit)
    :param detailed: False - (default) return string list; True - list of dicts {"word", "start", "end"}
    :param model: specify language model
    """

    model_path = get_model_path()
    data_path = get_data_path()

    config = {
        'audio_file': file_path,
        'hmm': os.path.join(model_path, model),
        'allphone': os.path.join(model_path, 'phone.lm.dmp'),
    }

    for param in configuration['default_phonemes']:
        config[param] = configuration['default_phonemes'][param]

    if model in configuration:
        for param in configuration[model]:
            config[param] = configuration[model][param]

    audio = AudioFile(**config)

    phrases = []

    if detailed:

        for phrase in audio:
            phrases.append(phrase.segments(detailed=detailed))

        out_list = []

        for phrase in phrases:

            for p in phrase:
                out_list.append({"phoneme": p[0], "start": p[2]/100.00, "end": p[3]/100.00})

        return out_list

    for phrase in audio:
        phrases.append(str(phrase))

    return phrases


def get_words_from_file(file_path, detailed=False, model='en-us'):
    """
    :param file_path: audio file (must be raw 16khz 16bit)
    :param detailed: False - (default) return string list; True - list of dicts {"word", "start", "end"}
    :param model: specify language model
    """

    model_path = get_model_path()
    data_path = get_data_path()

    config = {
        'audio_file': file_path,
        'hmm': os.path.join(model_path, model),
        'lm': os.path.join(model_path, '{m}\\{m}.lm.bin'.format(m=model)),
        'dict': os.path.join(model_path, '{m}\\{m}.dict'.format(m=model))
    }

    for param in configuration['default_words']:
        config[param] = configuration['default_words'][param]

    if model in configuration:
        for param in configuration[model]:
            config[param] = configuration[model][param]

    audio = AudioFile(**config)

    phrases = []

    if detailed:

        for phrase in audio:
            phrases.append(phrase.segments(detailed=detailed))

        out_list = []

        for phrase in phrases:

            for p in phrase:

                out_list.append({"word": p[0], "start": p[2]/100.00, "end": p[3]/100.00})

        return out_list

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