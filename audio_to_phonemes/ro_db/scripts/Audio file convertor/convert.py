import os
import subprocess

path = os.path.dirname(__file__)
loc_program = os.path.join(path, "sox", "sox.exe")
out = os.path.join(path, 'output')
in_p = os.path.join(path, 'input')

if not ( os.path.exists(out) and os.path.exists(in_p) and os.path.exists( os.path.join(path, "sox") ) ):
	if not os.path.exists(in_p):
		os.mkdir("input")
	if not os.path.exists(out):
		os.mkdir("output")
	if not os.path.exists(os.path.join(path, "sox")):
		os.mkdir("sox")

for root, dirs, files in os.walk(in_p):
	for i in files:
		if i.split('.')[-1] in ['wav', 'flac']:
			in_path = os.path.join(in_p, i)
			out_path = os.path.join(out, (os.path.splitext(i)[0] + '.wav'))
			command = r'"{}" "{}" -b 16 "{}" channels 1 rate 16k'.format(loc_program, in_path, out_path)
			command = command.replace('\\', '/')
			#print(command + '\n')
			subprocess.call(command, shell=True)

