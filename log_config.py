import logging, os

level = os.getenv("LOG_LEVEL")

if level is None or level == "DEBUG":
    level = logging.DEBUG
elif level == "INFO":
    level = logging.INFO
elif level == "WARNING":
    level = logging.WARNING
elif level == "ERROR":
    level = logging.ERROR
else:
    raise ValueError(f"Unkown Log Level : {level}")
