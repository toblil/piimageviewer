import os
import sys
import time
import traceback
from getkey import getkey

clear = lambda: os.system('clear')
DIR_BASE = '/home/pi/Pictures'
contains_dirs = False
os.chdir(DIR_BASE)
while(1):
	clear()
	print(" KATALOG: " + os.getcwd())
	keytodirname = {}
	count = 0
	row_count = 0
	print("")
	line = ""
	dirs = os.listdir('.')
	dirs.sort()
	for dirname in dirs:
		count += 1
		keytodirname[str(count)] = dirname
		d = "    %d - %s" % (count, dirname)
		line += d
		if row_count < 0:
			row_count += 1
		else:
			print(line)
			row_count = 0
			line = ""
	if len(line) > 0:
		print(line)
	print('')
	if len(os.getcwd()) > len(DIR_BASE):
		print("    ESC - TILLBAKA")
	print("    0 - VISA ALLA")
	print("    s - VISA ALLA SLUMPADE")
	print("    Q - STANG AV")
	print("")
	#print("    SKRIV SIFFRA OCH ENTER: ")
	#p = sys.stdin.readline()
	q=chr(0x0)
	p=getkey()
	p = p.strip()
	try:
		row = int(p, 10)
		if(row == 1 and count > 9):
			sys.stdout.write("FORTSATT SKRIVA ELLER ENTER: " + str(row))
			sys.stdout.flush()
			q=getkey()
			q=q.strip()
			try:
				ord(q)
				sys.stdout.write(q)
				sys.stdout.flush()
			except:
				q = chr(0x0)
	except:
		pass
	feh_command = "feh -r -F <RANDOMIZE> --sort dirname --draw-filename --auto-rotate <DIRECTORY>"
	error = False
	randomize = False
	contains_dirs = False
	esc_pressed = False
	if(p=="*" or p=="'"):
		sys.exit(0)
	if(p=="Q"):
		os.system('sudo shutdown now')
	else:
		try:
			if(p=="0"):
				replace_with = "."
			elif(p=="s"):
				replace_with = "."
				randomize = True
			elif(ord(p)==27): #ESC
				esc_pressed = True
				if len(os.getcwd()) > len(DIR_BASE):
					os.chdir('..')
			elif((ord(p))>=0x30 and (ord(p)) <= 0x39):
				try:
					if((ord(q))>=0x30 and (ord(q)) <= 0x39):
						temp = 10*(ord(p) - 0x30)
						temp = temp + ord(q) - 0x30
						key = str(temp)
						replace_with = keytodirname[key]
					else:
						replace_with = keytodirname[p]
					os.chdir(replace_with)
					#print("Testing dir: " + os.getcwd())
					contains_dirs = False
					for dirname in os.listdir('.'):
						filename_to_test = os.getcwd() + '/' + dirname 
						#print("Testing filename: " + filename_to_test)
						if os.path.isdir(filename_to_test):
							contains_dirs = True
					if not contains_dirs:
						os.chdir('..')
				except:
					print("FEL...")
					print(traceback.format_exc())
					time.sleep(0.5)
					error = True
			else:
				print("FEL...")
				print(traceback.format_exc())
				time.sleep(0.5)
				error = True
		except:
			print("FEL...")
			print(traceback.format_exc())
			time.sleep(0.5)
			error = True

	if not error and not contains_dirs and not esc_pressed:
		command = feh_command.replace('<DIRECTORY>', '"' + replace_with + '"')
		if randomize:
			command = command.replace('<RANDOMIZE>', '-zD 2.0')
			command = command.replace('--sort dirname ', '')
		else:
			command = command.replace('<RANDOMIZE>', '')
		print("")
		print("Running command: " + command)
		time.sleep(2)
		os.system(command)

