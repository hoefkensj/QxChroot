
#!/usr/bin/python
from bash import *
from clit import *
from configparser import ConfigParser, ExtendedInterpolation
import cfg,sys,argparse



def get_cfg(env_chroot):
	return cfg.todct(
		cfg.read(
			f'chroot_{env_chroot.upper()}.ini',
			ConfigParser(
				interpolation=ExtendedInterpolation(),
				delimiters=':'
				)
			)
		)

def shm(MNT_FS):
	run('test', '-L /dev/shm ')
	run('rm', '/dev/shm')
	run('mkdir', '/dev/shm') 
	mount('shm', '/dev/shm', MNT_FS['shm'])
	run('chmod', '1777 /dev/shm')

def unpack_dct(dct_chrt):
	MNT_FS		= dct_chrt['MNT_FS']
	STORL 		= dct_chrt['STORL']
	STORF 		= dct_chrt['STORF']
	MNT = dct_chrt['MNT']
	dicts={'MNT_FS':MNT_FS,'STORL':STORL,'STORF':STORF,'MNT':MNT}
	root = (STORL['root'], MNT['root'], MNT_FS['f2fs'])
	boot = (STORL['boot'], MNT['boot'], MNT_FS['vfat'])
	proc = (STORF['proc'], MNT['proc'], MNT_FS['proc'])
	sys = (STORF['sys'], MNT['sys'], MNT_FS['sys'])
	dev = (STORF['dev'], MNT['dev'], MNT_FS['dev'])
	settings=(root,boot,proc,sys,dev)
	return settings,dicts


def start(args,dct):
	for i, arg in enumerate(args):
		wnl(f'mounting {args[i][0]} on {args[i][1]}')
		mount(args[i][0], args[i][1], args[i][2])
		
	make_rslave(dct['MNT']['sys'])
	make_rslave(dct['MNT']['dev'])
	shm(dct['MNT_FS'])
	wnl('copieng resolf.conf...')
	run('cp', f'--dereference /etc/resolv.conf {dct["MNT"]["etc"].lower()}')
	wnl('changing directory ...')
	spawn_afterchroot(dct['MNT'])
	#run('cd', dct['MNT']['root'])
	#prepp2()
	run('konsole', f'-e chroot {dct["MNT"]["root"]} /bin/bash')
	return 0

def stop(MNT):
	umount(MNT['proc'])
	umount(MNT['sys'])
	umount(MNT['dev'])
	umount(MNT['boot'])
	umount(MNT['root'])
	return 0

def spawn_afterchroot(MNT):
	with open(f'{MNT["root"]}/.afterchroot.sh','w') as file:
		file.write('#!/bin/bash\n')
	with open(f'{MNT["root"]}/.afterchroot.sh','a') as file:
		file.write('source /etc/profile\n')
		file.write('export PS1="(chroot) ${PS1}"\n')
		#file.write('screen -S chroot\n')
	run('chmod', f'+x {MNT["root"]}/.afterchroot.sh ')


def getargs():
	parser=argparse.ArgumentParser()
	parser.add_argument('cmd', help='[start|stop] chroot for [env]')
	parser.add_argument('env', type=str ,help='[env]')
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	a=getargs()
	sudo()

	tup_settings,cfg_dicts= unpack_dct(get_cfg(a.env))
	dct_fnc = {
			'start': start,
			'stop' : stop
			}
	act = dct_fnc[a.cmd]
	act(tup_settings,cfg_dicts)

	
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
#bash.run('export', 'PS1="(chroot) ${PS1}"')



