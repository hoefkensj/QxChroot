from configparser import ConfigParser,ExtendedInterpolation
import dct,os



def new():
	cfg = ConfigParser(interpolation=ExtendedInterpolation(), delimiters=':')  # create empty config
	cfg.optionxform = lambda option: option
	return cfg
	
def create(file,config):
	cfg= tocfg(dct_Config, config)
	write(file,config)
def get_rrhome():
	path = f'{"/".join(os.path.realpath(__file__).split("/")[0:-1])}/'
	print(path)
	return path
	

def read_from(file,config):
	config.read(file)
	return config

def to_dct(cfg,dct={}):
	for section in cfg.keys():
		dct[section]= dict(cfg[section])
	return dct

def to_cfg(dct,cfg):
	cfg.read_dict(dct)
	return dct


def get(src):
	cfg=new()
	inifile=f'{get_rrhome()}/Rootes/{src.upper()}.ini'
	cfg = read_from(inifile, cfg)
	return cfg

def write(filename,cfg):
	with open(filename, 'w') as file:
		cfg.write(file)
		
		
if __name__ == '__main__':
	main = main()
	main('test')
