#!/usr/bin/python3
import bash, cfg, clit
import sys,argparse,os
from configparser import ConfigParser, ExtendedInterpolation
from bash import *

# def run(a,**k):
# 	binbash=f'/usr/bin/bash'
# 	thisproc=subprocess.Popen(a , stdout=subprocess.PIPE, universal_newlines=True)
# 	return thisproc

def root(helper='sudo',trys=0):
	euid = os.geteuid
	if euid() != 0:
		print("Script not started as root. Running sudo..")
		args = [helper, sys.executable] + sys.argv + [os.environ]
		# the next line replaces the currently-running process with the sudo
		os.execlpe(helper, *args)
	else: return euid
	root(trys=(trys-1)) if trys else sys.exit("couldn't get root")


def shm(shm):
	run('test -L /dev/shm')
	run('sudo -S rm /dev/shm')
	run('mkdir /dev/shm')
	mount(f"shm /dev/shm {shm}")
	run('chmod 1777 /dev/shm')

def unpack_dct(Config):
	MNT_FS		= dct_Config['OPTIONS']
	STORL 		= dct_Config['DEVICE']
	STORF 		= dct_Config['SPECIAL']
	MNT 		= dct_Config['REROOT']
	root = (STORL['root'], MNT['root'], MNT_FS['f2fs'])
	boot = (STORL['boot'], MNT['boot'], MNT_FS['vfat'])
	proc = (STORF['proc'], MNT['proc'], MNT_FS['proc'])
	sys = (STORF['sys'], MNT['sys'], MNT_FS['sys'])
	dev = (STORF['dev'], MNT['dev'], MNT_FS['dev'])
	mkrssys= ('', MNT['sys'],'--make-rslave')
	mkrsdev= ('', MNT['dev'],'--make-rslave')
	shm = MNT_FS['shm']
	etc= MNT['etc']
	settings=(root,boot,proc,sys,dev,mkrssys,mkrsdev,shm,etc)
	return settings


def start(seqs):

	for seq in seqs:
		wnl(f'mount {seqs[seq]}')
		mount(args=seqs[seq])
	#$shm(args['shm'])
	#$shm(args['shm'])
	wnl('copieng resolf.conf...')
	
	run( f'cp -vf --dereference /etc/resolv.conf /os/arch/etc')
	wnl('changing directory ...')
	#spawn_afterchroot(dct['MNT'])
	#run( f'{args[0][1]}')
	#prepp2()

	return 0

def stop(MNT):
	umount(MNT['proc'])
	umount(MNT['sys'])
	umount(MNT['dev'])
	umount(MNT['boot'])
	umount(MNT['root'])
	return 0


def addseqsection(cfg):

	dct= {
		'ROOT' 	: 	'${OPTIONS:f2fs}	${DEVICE:root}	${REROOT:root}',
		'BOOT' 	: 	'${OPTIONS:vfat}	${DEVICE:boot}	${REROOT:boot}',
		'PROC' 	: 	'${OPTIONS:proc}	${SPECIAL:proc}	${REROOT:proc}',
		'SYS' 	:	'${OPTIONS:sys}	${SPECIAL:sys}	${REROOT:sys}',
		'DEV' 	:	'${OPTIONS:dev}	${SPECIAL:dev}	${REROOT:dev}',
		'MKSSYS':	'--make-rslave	${REROOT:sys}',
			'MKSDEV': '--make-rslave	${REROOT: dev}'
			}
	for key in dct.keys():
		cfg['SEQUENCES'][key] = dct[key]
	return cfg

def spawn_afterchroot(MNT):
	with open(f'{MNT["root"]}/.afterchroot.sh','w') as file:
		file.write('#!/bin/bash\n')
	with open(f'{MNT["root"]}/.afterchroot.sh','a') as file:
		file.write('source /etc/profile\n')
		file.write('export PS1="(chroot) ${PS1}"\n')
		#file.write('screen -S chroot\n')


# hhrun(' f'chmod +x {MNT["root"]}/.afterchroot.sh ')

def home():
	path = f'{"/".join(os.path.realpath(__file__).split("/")[0:-1])}/'
	print(path)
	return path


def getargs(): #get arguments from commandline
	parser=argparse.ArgumentParser()
	parser.add_argument('cmd', help='[start|stop] chroot for [env]')
	parser.add_argument('env', type=str ,help='[env]')
	args = parser.parse_args()
	return args


def main():
	root()
	ReRoot_Home=home()
	a=getargs()

	inifile = f'{ReRoot_Home}/Rootes/{a.env.upper()}.ini' #construct ini file path from commandline env var and location of the script
	config = cfg.get(inifile)
	#config = addseqsection(config)
	dict= cfg.to_dct(config)
	seqs = dict['SEQUENCES']

	
	
	dct_fnc = {
			'start': start,
			'stop' : stop
			}
	act = dct_fnc[a.cmd]
	#
	act(seqs)
	run( f'konsole -e chroot /os/{a.env} /bin/bash')

if __name__ == '__main__':
	main()
	
	

	
	#if args.cmd=='stop'else

	
	

	
	

	
	#mounted = is_mount(path.lower())
	#if mounted:




#
# print('Press s or n to continue:')
#
# with keyboard.Events() as events:
# 	# Block for as much as possible
# 	event = events.get(1e6)
# 	if event.key == keyboard.KeyCode.from_char('s'):
# 		print("YES")
#
#
#
#
#
		


	
	
#bash.run('chroot','/mnt/gentoo /bin/bash')
#bash.run('source','/etc/profile')
#bash.run('export PS1="(chroot) ${PS1}"')



