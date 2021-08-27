# DEFINITIONS
# Supersu run chk_mnt is_mount umount mount
import subprocess
import shlex, os, sys
from functools import partial

#create a process to be executed with processname = proc
proc= partial(subprocess.Popen, stdin=subprocess.PIPE,stdout=subprocess.PIPE, universal_newlines=True)

#run the program as root :
def root(helper='kdesu',trys=0):
	euid = os.geteuid
	if euid() != 0:
		args = [helper, sys.executable] + sys.argv + [os.environ]
		# the next line replaces the currently-running process with the sudo
		os.execlpe(helper, *args)
	else: return euid
	root(trys=(trys - 1)) if trys else sys.exit("couldn't get root")


#implement the Su not aas root but as switch User!!!
def su(user):
	shell = proc
	user=shell(('su', user))
	return user


def run(a):
	shell = proc
	tpl_a=shlex.split(a)
	out=shell(tpl_a)
	return out.stdout.readlines()
# def sudo():
# 	euid = os.geteuid()
# 	if euid != 0:
# 		print("Script not started as root. Running sudo..")
# 		args = ['sudo', sys.executable] + sys.argv + [os.environ]
# 		# the next line replaces the currently-running process with the sudo
# 		os.execlpe('sudo', *args)
# 	print('Running. Your euid is', euid)
# 	return

# def proc(a,**k):
# 	binbash=f'/usr/bin/bash'
# 	thisproc=subprocess.Popen(a , stdout=subprocess.PIPE, universal_newlines=True)
# 	return thisproc

# def runold(cmd, args=''):
# 	args = f' {cmd} {args}'
# 	su = 'sudo'
# 	bashline = []  + shlex.split(args)
# 	allput = ['stdout:\n']
# 	process = subprocess.Popen(bashline, stdout=subprocess.PIPE, universal_newlines=True)
# 	ret = {'RETURN_CODE' : '','STDOUT': ''}
# 	while True:
# 		output = process.stdout.readline()
# 		#wrl(output.strip())
# 		allput.append(output.strip())
# 		# Do something else
# 		return_code = process.poll()
# 		if return_code is not None:
# 			ret['RETURN_CODE']= return_code
# 			#wrl(f'RETURN CODE:{return_code}')
# 			# Process has finished, read rest of the output
# 			for output in process.stdout.readlines():
# 				#wrl(output.strip())
# 				allput.append(output.strip())
# 			break
# 	ret['STDOUT']= allput
# 	return ret
#
#
# def out(string):
# 	sys.stdout.write(f'{string}')
#
#
#
def is_mount(path,tgl=''):
	MOUNT = run('mountpoint path')
	for line in MOUNT['STDOUT']:
		tgl= path in line
		if tgl:	break
		else :continue
	return tgl

def umount(path):
	STAT= run(f'umount-l {path.lower()}')
	return STAT


def mount(**k):
	if k['file'] is None:
		STAT = run(f"mount {k['args']} {k['path'].lower()}")
	else:
		STAT = run(f"mount {k['args']} {k['file']} {k['path'].lower()}")
	return STAT
#
# def make_rslave(path):
# 	status=run(f'mount --make-rslave {path.lower()}')
# 	return status
#
# def help():
# 	return f'Usage: $qxroot.py [start|stop] [$env]'
def wxl(line):
	sys.stdout.write(f'\t{line}')

def wrl(line):
	sys.stdout.write(f'\r{line}')

def wnl(line):
	sys.stdout.write(f'\n{line}')
#
# def main(cmd, args=''):
# 	return
#
#
if __name__ == '__main__':
	root()
	status = proc
	stat = status('whoami')
	
	print(stat.stdout.readline())