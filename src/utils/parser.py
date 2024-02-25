import configparser

ini_path = './config.ini'

class ConfigManager:
    def __init__(self, config_file_path):
        self.config = configparser.ConfigParser()
        self.config_file_path = config_file_path
        self.config.read(config_file_path)
        
    def get_config_dict(self):
        all_config_dict = {}
        
        for section in self.config.sections():
            section_dict = {}
            
            for key, value in self.config[section].items():
                section_dict[key] = value
                
            all_config_dict[section] = section_dict
            
        return all_config_dict
        
config_mng = ConfigManager(ini_path)
