import json
import os

ROOT_DIR = os.path.abspath(os.curdir)

# базовый метод получения конфигурации из файла
def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)


# метод получения конфигурации приложения
def load_app_config():
    base_dir = os.path.join(ROOT_DIR, "appconfig.json")
    return  load_config(base_dir)


# метод получения конкретногьо раздела конфигурации
def get_config_section(section_name: str):
    config_file = load_app_config()
    return  config_file[section_name]