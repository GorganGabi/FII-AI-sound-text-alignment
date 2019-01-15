"""
The code in this script was used for the generation of the fileids and transcription files
needed for training the model. Due to the very specific arrangement of the folders, this
script is not meant to be used in a general manner, as it was used to accomodate parsing
the data from the SWARA corpus (https://speech.utcluj.ro/swarasc/).
"""


import os

fileids_train = open("/etc/ro_db_train.fileids", 'a')
fileids_test = open("/etc/ro_db_test.fileids", 'a')
transcript_train = open("/etc/ro_db_train.transcription", 'a')
transcript_test = open("/etc/ro_db_test.transcription", 'a')

import os


#fileids generation

"""
for dir in os.listdir("/"):

	for i in os.listdir(dir + "/train/):
		fileids_train.write(dir + "/train/" + i.split('.')[0])
		
	for i in os.listdir(dir + "/test/):
		fileids_test.write(dir + "TIM/train/" + i.split('.')[0])
"""


#transcription generation

for dir in os.listdir("/"):

	transcript_txt = ""
	for i in range(0, os.listdir(dir)):
		transcript_txt += open(dir + "/rnd" + i).read()
	
	open("transcript.txt", 'w').write(transcript_txt)

	transcript = open("transcript.txt").readlines()

	ts_train = ""
	ts_test = ""
	
	for i in range(0, len(os.listdir(dir + "/train/")):
		transcript[i] = "<s> " + transcript[i][5:-2] + " </s> " + "(" + new[i][0:-1] + ")\n"
		ts_train += transcript[i]

	for i in range(len(os.listdir(dir + "/train/"), len(transcript)):
		transcript[i] = "<s> " + transcript[i][5:-2] + " </s> " + "(" + new[i][0:-1] + ")\n"
		ts_train += transcript[i]

		
transcript_train.write(ts_train)
transcript_test.write(ts_test)


#check for discrepancy between transcript and audio files

"""
for i in os.listdir("train"):
    audio += i + '\n'

yesAudio_noTranscripts = []
noAudio_yesTranscripts = []

for i in range(0, 500):
    if str(i) not in audio and str(i) in transcripts:
        noAudio_yesTranscripts.append(i)
    if str(i) not in transcripts and str(i) in audio:
        yesAudio_noTranscripts.append(i)

print("In audio, not in transcripts:" + str(yesAudio_noTranscripts))
print("Not in audio, in transcripts: " + str(noAudio_yesTranscripts))
"""