from environs import Env

env = Env()

env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')

DB_DRIVER = env.str('DB_DRIVER')
DB_USERNAME = env.str('DB_USERNAME')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_NAME = env.str('DB_NAME')

CHAT_ID = env.str('CHAT_ID')

ADMINS_ID = 5295136531

