import sox


'''
Arguments:
    string inFilePath:
        The given file system absolute path for the audio file to be converted.
    string outFilePath:
        The given file system absolute path for the audio file to be converted. Includes
        extension (which must be '.raw').
'''
def convertFileToRaw(inFilePath, outFilePath):
    tfm = sox.Transformer();
    tfm.set_output_format(file_type='raw', rate=16000, bits=16, channels=2)
    tfm.build(inFilePath, outFilePath)
