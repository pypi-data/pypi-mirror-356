import logging
import logging.config
import sys
import os


def get_logger(name):
    config = None

    if not getattr(get_logger, "configured", False):
        setattr(get_logger, "configured", True)
        package_root = os.path.dirname(os.path.dirname(__file__))  # Adjust as needed to reach package root
        toml_path = os.path.join(package_root, "pyproject.toml")
        try:
            with open(toml_path, "rb") as f:
                if sys.version_info >= (3, 11):
                    import tomllib
                else:
                    import tomli as tomllib
                config = tomllib.load(f).get("tool", {}).get("logging", {})
        except FileNotFoundError:
            pass

    if config:
        # NOTE: due to a bug in the logging library (?), handlers and formatters can't reliably be set through
        # dictConfig(). We set them manually now.

        console_handler = logging.StreamHandler(sys.stdout)
        format_dict = config.pop("formatters", {}).get("formatter", {})
        if format_dict:
            formatter = logging.Formatter(format_dict.get("format"))
            if "default_time_format" in format_dict:
                formatter.default_time_format = format_dict["default_time_format"]
            console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)

        logging.config.dictConfig(config)

    return logging.getLogger(name)
