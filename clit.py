from pynput import keyboard
from sys import stdout

def wxl(line):
	stdout.write(f'\t{line}')

def wrl(line):
	stdout.write(f'\r{line}')

def wnl(line):
	stdout.write(f'\n{line}')


def tkit(state):
	dctTXT = {
			'tgln':'[ ]',
			'tgly':'[X]',
			'strYN': '[Y]|n'
	}
	if state:
		return dctTXT['tgly']
	elif state == 'YN':
		return dctTXT['strYN']
	else:
		return dctTXT['tgln']
	


def ask(Q):
	wnl(f'{Q}:') #write new line : Q
	if kbl('YyNn') in 'Yy' :
		return True
	else:
		return False

def kbl(chars='azAZ09', defkey="y"):
	if chars == 'azAZ09':
		chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	
	while True:
		with keyboard.Events() as events:
			event = events.get(1e6)
			if 'Press' in str(event):
				keyp = str(event.key).strip("''")
				if keyp in chars:
					char = str(event.key).strip("''")
					return char
				elif 'enter' in keyp:
					return defkey
			else:
				stdout.write(f'')

def libLine(*args,**kwargs):
	path=kwargs['path']
	act = args
	wnl(f'{tkit(is_mount(path.lower()))}\t{path.lower()}')

