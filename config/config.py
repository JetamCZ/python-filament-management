from environs import Env

env = Env()
env.read_env()

db_name = env.str("DB_FILE")

