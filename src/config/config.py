import configparser

"""
Needed to load config.cfg , where contains user settings 
"""
def load_config(path="config/config.cfg"):
    config = configparser.ConfigParser()
    config.read(path)
    return config