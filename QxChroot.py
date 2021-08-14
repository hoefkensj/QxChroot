
#!/usr/bin/python
from bash import *
from clit import *
from configparser import ConfigParser, ExtendedInterpolation
import cfg,sys



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
	MNT 		= dct_chrt['MNT']
	return MNT_FS,STORL,STORF,MNT
	
def start(STORF,STORL,MNT,MNT_FS):
	mount(STORL['root'],MNT['root'],MNT_FS['f2fs'])
	mount(STORL['boot'], MNT['boot'], MNT_FS['vfat'])
	mount(STORF['proc'], MNT['proc'], MNT_FS['proc'])
	mount(STORF['sys'], MNT['sys'], MNT_FS['sys'])
	mount(STORF['dev'], MNT['dev'], MNT_FS['dev'])
	make_rslave(MNT['sys'])
	make_rslave(MNT['dev'])
	shm(MNT_FS)
	wnl('copieng resolf.conf...')
	run('cp', f'--dereference /etc/resolv.conf {MNT["etc"].lower()}')
	wnl('changing directory ...')
	spawn_afterchroot(MNT)
	#run('cd', MNT['root'])
	#prepp2()
	run('chroot',f'{MNT["root"]} /bin/bash -c /.afterchroot.sh')
	



def stop(MNT):
	umount(MNT['proc'])
	umount(MNT['sys'])
	umount(MNT['dev'])
	umount(MNT['boot'])
	umount(MNT['root'])

def status(MNT):
	chk_mnt(MNT['root'])
	
def spawn_afterchroot(MNT):
	with open(f'{MNT["root"]}/.afterchroot.sh','w') as file:
		file.write('#!/bin/bash\n')
	with open(f'{MNT["root"]}/.afterchroot.sh','a') as file:
		file.write('source /etc/profile\n')
		file.write('export PS1="(chroot) ${PS1}"\n')
		file.write('screen -S chroot\n')
	run('chmod', f'+x {MNT["root"]}/.afterchroot.sh ')

def main(chrenv,act='start'):
	
	supersu(f'QUICK CHROOT: {chrenv}')
	MNT_FS, STORL, STORF, MNT = unpack_dct(get_cfg(chrenv))
	if act=='start':
		start(STORF, STORL, MNT, MNT_FS)
	elif act == 'stop':
		stop(STORF,STORL,MNT)

	


	


if __name__ == '__main__':
	main('gentoo', 'start')

	
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



