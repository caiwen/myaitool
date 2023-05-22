"""
工具类，获取配置信息
"""
import configparser
import approot


class ModConfig:

    def __init__(self):
        # 配置文件目录
        self.file = '/conf/config.ini'

    # 获取配置
    def getConfig(self, section, name, defaultValue=''):
        try:
            conf = configparser.ConfigParser()
            config_path = approot.get_root() + self.file
            conf.read(config_path, encoding='UTF-8')
            name = conf.get(section, name)
            return name
        except Exception as e:
            print(repr(e))
            return defaultValue


if __name__ == '__main__':
    print(ModConfig().getConfig('caigou', 'dbhost', '111'))
