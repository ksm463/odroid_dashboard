import configparser

class ConfigManager:
    def __init__(self, config_file_path):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str  # 옵션 이름을 대소문자 그대로 유지
        self.config_file_path = config_file_path
        self.config.read(config_file_path)  # 구성 파일 읽기

        # 섹션과 키에 대한 타입 매핑
        self.type_map = {
            'DB': {
                'DB_PATH': str,
                'DB_NAME': str,
            },
            'LOGS': {
                'LOG_FILE_PATH': str,
                'LOG_FILE_NAME': str,
                'LOG_LEVEL': str,
            },
            'DASH': {
                'MAX_LENGTH': int,
                'DASH_INTERVAL': int,
            }
        }

    def get_config_dict(self):
        all_config_dict = {}

        for section in self.config.sections():
            section_dict = {}

            # 각 섹션의 키-값 쌍에 대해 루프 실행
            for key, value in self.config[section].items():
                if key in self.type_map.get(section, {}):
                    value_type = self.type_map[section][key]
                    section_dict[key] = value_type(value)  # 타입 변환
                else:
                    section_dict[key] = value  # 타입 변환이 필요 없는 값

            all_config_dict[section] = section_dict

        return all_config_dict
