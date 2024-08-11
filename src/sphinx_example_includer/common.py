import logging


def get_logger(name=None):
    if name:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARN)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARN)
    logger.addHandler(ch)
    return logger


def write_above_or_end(file_path, target, content_to_write):
    # Read the file contents
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the target exists in the file
    target_index = None
    for i, line in enumerate(lines):
        if target in line:
            target_index = i
            break

    # If target is found, insert content above it
    if target_index is not None:
        lines.insert(target_index, content_to_write + '\n')
    else:
        # If target is not found, append content at the end
        lines.append(content_to_write + '\n')

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)


