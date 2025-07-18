"""Module preference.py"""
import logging

import pandas as pd


class Preference:
    """
    Sets up the labels in focus
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__preference: list = arguments.get('preference')
        self.__rename: dict = arguments.get('rename')

    def __call__(self) -> pd.DataFrame:
        """

        :return:
            identifier: This will be the code of the selected name/label
            name:
            label:
        """

        # A data frame consisting of the labels of interest
        frame = pd.DataFrame.from_records(data=list(enumerate(self.__preference)), columns=['identifier', 'name'])

        # An additional field of alternative labels names
        frame['label'] = frame['name']
        frame['label'] = frame['label'].replace(to_replace=self.__rename).values
        logging.info(frame)

        return frame
