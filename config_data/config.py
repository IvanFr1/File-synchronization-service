from dotenv import dotenv_values


config_data = dotenv_values()


token_api = config_data.get('TOKEN')
local_path = config_data.get('LOCAL_PATH')
remove_path = config_data.get('REMOVE_PATH')
interval = config_data.get('INTERVAL')
log_path = config_data.get('LOG_FILE')
