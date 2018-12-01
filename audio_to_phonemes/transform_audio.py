import os
import sys
from pocketsphinx import AudioFile, get_model_path, get_data_path


def get_phonemes_from_file(file_path):
    """
    :param file_path: audio file (must be raw 16khz 16bit)
    :return: a list of phrases
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
        #'lm': os.path.join(model_path, 'en-us.lm.bin'),
        #'dict': os.path.join(model_path, 'cmudict-en-us.dict'),
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


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
            phrases = get_phonemes_from_file(sys.argv[1])
            for phrase in phrases:
                print(phrase)
