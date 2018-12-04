import pydub
import os

def getFileExtension(inFilePath):
    extension = os.path.splitext(inFilePath)[1][1:]

    return extension

'''
Arguments:
    string inFilePath:
        The given file system absolute path for which the AudioSegment
        shall be returned.
Return:
    AudioSegment object created from the file pointed to by the given
    file-system absolute path, inFilePath.
'''
def getPydubAudioSegment(inFilePath):
    extension = getFileExtension(inFilePath)

    resultAudio = pydub.AudioSegment.from_file(inFilePath, format=extension)

    resultAudio = resultAudio.set_frame_rate(16000)
    resultAudio = resultAudio.set_sample_width(2)

    return resultAudio


'''
Arguments:
    string inFilePath:
        The given file system absolute path for the audio file to be converted.
        Formats accepted natively: wav, raw. With ffmpeg library: mp3, ogg, aif (and others).
    string outFilePath:
        The given file system absolute path for the audio file to be converted. Includes
        extension (which must be '.raw').
'''
def convertFileToRaw(inFilePath, outFilePath):
    if os.path.exists(outFilePath) and os.path.isfile(outFilePath):
        os.remove(outFilePath)


    audio = getPydubAudioSegment(inFilePath)

    audio.export(outFilePath, format="raw")

    #output_file = open(out_filename, "wb")
    #output_file.write(audio._data)
