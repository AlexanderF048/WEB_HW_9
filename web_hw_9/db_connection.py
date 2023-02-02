from pathlib import Path
from configparser import ConfigParser
from mongoengine import connect

path_to_config = Path(__file__).parent.parent.joinpath('config.ini')
print(f'Path to config.ini:::{path_to_config}')
db_configurations = ConfigParser()
db_configurations.read(path_to_config)

db_username = db_configurations.get('DB_DEV', 'username')
db_password = db_configurations.get('DB_DEV', 'password')
db_domain = db_configurations.get('DB_DEV', 'db_domain')
db_name = db_configurations.get('DB_DEV', 'db_name')

db = connect(host=f'mongodb+srv://{db_username}:{db_password}@{db_domain}.{db_name}'
                        f'.mongodb.net/?retryWrites=true&w=majority', ssl=True)






