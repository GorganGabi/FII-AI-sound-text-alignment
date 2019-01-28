import os
import re
import sys
import time
from subprocess import Popen, PIPE

print("Running Python {}".format(sys.version_info))

from pocketsphinx import AudioFile, get_model_path, get_data_path
from transform_audio_configs import configuration


help = """Arguments for console usage:
-h\tShow this
-p <file_path>\tExtract phonemes
-w <file_path>\tExtract words

Example: transform_audio.py -p sample1.raw -model=it -d
"""


def get_detailed_output(file_path):

    lines = open(file_path).readlines()

    output_begin_index = 0
    output_end_index = 0

    for i in range(0, len(lines)):
        if lines[i].startswith("[SEQUENCE START]"):
            output_begin_index = i + 1
        if lines[i].startswith("[SEQUENCE END]"):
            output_end_index = i

    output = []

    for i in range(output_begin_index, output_end_index):
        if not (lines[i].startswith("INFO") or lines[i].startswith("ERROR") or lines[i].startswith("WARN")):
            line = re.split(r"\s+", lines[i])
            
            output_entry = {'start': float(line[1]) / 100, 'end': float(line[2]) / 100, 'word': line[0].lower()}
            output.append(output_entry)

    return output


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


def get_words_from_file_experimental(file_path, detailed=False, model='en-us', cleanup=False):
    model_path = get_model_path()
    data_path = get_data_path()

    t = int(time.time()) % 1000
    log_name = 'log_messages_{}.log'.format(t)

    command = 'bin\\pocketsphinx_continuous.exe -verbose yes -backtrace yes -hmm "{hmm}" -lm "{lm}" -dict "{dict}" -logfn "{log}" -infile "{file}"'.format(
        hmm=os.path.join(model_path, model),
        lm=os.path.join(model_path, '{m}\\{m}.lm.bin'.format(m=model)),
        dict=os.path.join(model_path, '{m}\\{m}.dict'.format(m=model)),
        log=log_name,
        file=file_path
    )

    process = Popen(command, stdout=PIPE)
    out, err = process.communicate()

    output = get_detailed_output(log_name)

    if cleanup:
        try:
            os.remove(log_name)
        except:
            print("Could not remove junk: {}".format(log_name))

    return output


def get_words_from_file(file_path, detailed=False, model='en-us'):
    """
    :param file_path: audio file (must be raw 16khz 16bit)
    :param detailed: False - (default) return string list; True - list of dicts {"word", "start", "end"}
    :param model: specify language model
    """

    model_path = get_model_path()
    data_path = get_data_path()

    #t = int(time.time()) % 1000
    #os.mkdir('mfclog_{}'.format(t))
    #os.mkdir('rawlog_{}'.format(t))
    #os.mkdir('senlog_{}'.format(t))

    config = {
        'audio_file': file_path,
        'hmm': os.path.join(model_path, model),
        'lm': os.path.join(model_path, '{m}\\{m}.lm.bin'.format(m=model)),
        'dict': os.path.join(model_path, '{m}\\{m}.dict'.format(m=model)),
        #'verbose': True,
        #'logfn': 'log_messages_{}.log'.format(t),
        #'mfclogdir': 'mfclog_{}'.format(t),
        #'rawlogdir': 'rawlog_{}'.format(t),
        #'senlogdir': 'senlog_{}'.format(t),
        #'backtrace': True
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
            f = get_words_from_file_experimental

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