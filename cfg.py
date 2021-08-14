def spawn(file_name):
	with open(f'{file_name}.ini' , 'w') as file:
		file.write(f'[DEFAULT]\nfilename\t:\t{file_name}\nfiletype\t:\tini')
	
def create(file_Config,dct_Config, cfg_config):
	cfg= tocfg(dct_Config, cfg_config)
	write(file_Config, cfg)


def read(file_Config, cfg_Config):
	cfg_Config.read(file_Config)
	return cfg_Config

def todct(cfg,dct={}):
	for section in cfg.keys():
		dct[section]= dict(cfg[section])
	return dct

def tocfg(dct,cfg):
	cfg.read_dict(dct)
	return dct


def write(file_Config, cfg_Config):
	cfg = cfg_Config
	with open(file_Config, 'w') as configfile:
		cfg.write(configfile)

def main():
	return spawn

if __name__ == '__main__':
	main = main()
	main('test')
