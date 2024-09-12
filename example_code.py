def add(x: int, y: int) -> int:
    return x + y


def multiply_with_five(value: int) -> int:
    return value * 5


def save_arguments_with_yaml(argument_dict: dict, save_path: str) -> bool:
    import yaml, logging

    success = False
    try:
        with open(save_path) as f:
            yaml.safe_dump(argument_dict, f)

        success = True
    except Exception as e:
        logging.error(e)

    return success


def transfer_arguments(pipeline_argument):
    pass
