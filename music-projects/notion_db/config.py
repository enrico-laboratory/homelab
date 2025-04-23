from os import getenv


def set_env_var(env: str, default: str=None):
    env = getenv(env, default)
    if not env:
        raise ValueError(f'{env} must be set')
    return env

NOTION_API_TOKEN = set_env_var('NOTION_API_TOKEN')

