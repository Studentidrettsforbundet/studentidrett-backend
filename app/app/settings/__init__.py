# flake8: noqa
from .base import *


env_name = os.getenv("ENV_NAME", "local")

if env_name == "production":
    from .production import *
elif env_name == "staging":
    from .development import *
else:
    from .local import *
