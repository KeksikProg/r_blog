from datetime import datetime
from os.path import splitext


def get_timestamp_path(instance, filename):
    """Generate new filename"""

    return f'{datetime.now().timestamp()}{splitext(filename)[1]}'
