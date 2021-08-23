# DEFINITIONS
# Supersu run chk_mnt is_mount umount mount
import subprocess
import shlex,os,sys

def sudo():
	euid = os.geteuid()
	if euid != 0:
		print("Script not started as root. Running sudo..")
		args = ['sudo', sys.executable] + sys.argv + [os.environ]
		# the next line replaces the currently-running process with the sudo
		os.execlpe('sudo', *args)
	print('Running. Your euid is', euid)



def run(cmd, args=''):
	args = f' {cmd} {args}'
	su = 'sudo'
	bashline = []  + shlex.split(args)
	allput = ['stdout:\n']
	process = subprocess.Popen(bashline, stdout=subprocess.PIPE, universal_newlines=True)
	ret = {'RETURN_CODE' : '','STDOUT': ''}
	while True:
		output = process.stdout.readline()
		#wrl(output.strip())
		allput.append(output.strip())
		# Do something else
		return_code = process.poll()
		if return_code is not None:
			ret['RETURN_CODE']= return_code
			#wrl(f'RETURN CODE:{return_code}')
			# Process has finished, read rest of the output
			for output in process.stdout.readlines():
				#wrl(output.strip())
				allput.append(output.strip())
			break
	ret['STDOUT']= allput
	return ret

def chk_mnt(MNT):
	if is_mount(MNT):
		pass
			
def is_mount(path,tgl=''):
	MOUNTS = run('mount')
	for line in MOUNTS['STDOUT']:
		tgl= path in line
		if tgl:	break
		else :continue
	return tgl

def umount(path):
	STAT= run('umount', f'-l {path.lower()}')
	return STAT
		

def mount(file,path,args):
	mounted = is_mount(path.lower())
	if not mounted:
		STAT=run('mount',f'{args} {file} {path.lower()}')
		return STAT

def make_rslave(path):
	status=run('mount', f'--make-rslave {path.lower()}')
	return status

def help():
	return f'Usage: $qxroot.py [start|stop] [$env]'

		
def main(cmd, args=''):
	return  run(cmd, args)
	
	
if __name__ == '__main__':
	pass