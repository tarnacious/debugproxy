from flask.config import Config
import os
import concurrent_log_handler

def read_config() -> Config:
    config = Config("")
    env_settings_file = os.environ.get('DEBUGPROXY_SETTING_FILE',
                                       './config/default_settings.py')
    config.from_pyfile(env_settings_file)

    # update the config with any values found in the environment
    for key in config.keys():
        env_value = os.environ.get(key)
        if env_value:
            config[key] = env_value

    return config
