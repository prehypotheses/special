"""config.py"""
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        -----------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>
        """

        # Directories
        self.data_ = os.path.join(os.getcwd(), 'data')
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')

        # Keys, etc
        self.s3_parameters_key = 's3_parameters.yaml'
        self.arguments_key = 'special/arguments.json'

        # Prefixes
        self.source = 'data/raw'
        self.destination = 'data/special'
