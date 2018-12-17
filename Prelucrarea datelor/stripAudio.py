import os
import sox
import sys

def getFileExtension(inFilePath):
    extension = os.path.splitext(inFilePath)[1][1:]

    return extension

'''
Arguments:
    string inFilePath:
        The given file system absolute path for the audio file to be converted.
    string outFilePath:
        The given file system absolute path for the audio file to be converted. Includes
        extension (which must be '.raw').
'''


def convertFileToRaw(inFilePath, outFilePath):
    try:
        tfm = sox.Transformer();


        fileType = getFileExtension(outFilePath)

        tfm.set_output_format(file_type = fileType, rate = 16000, bits = 16, channels = 1)

        tfm.build(inFilePath, outFilePath)

    except Exception as e:
        print(e)
        return


convertFileToRaw(sys.argv[1], sys.argv[2])
