"""Module preference.py"""
import logging

import pandas as pd

import config
import src.functions.streams


class Preference:
    """
    Sets up the labels in focus
    """

    def __init__(self, arguments: dict, bucket: str):
        """

        :param arguments:
        :param bucket:
        """

        self.__arguments = arguments
        self.__bucket = bucket

        # Configurations
        self.__configurations = config.Config()

        # For writing
        self.__streams = src.functions.streams.Streams()

    def __persist(self, frame: pd.DataFrame):
        """

        :param frame:
        :return:
        """

        fields = ['label', 'category', 'group']
        path = 's3://' + self.__bucket + '/' + self.__configurations.destination_tags + '/tags.csv'

        blob = frame.copy()[fields]
        blob.rename(columns={'label': 'tag'}, inplace=True)

        message = self.__streams.write(blob=blob, path=path)
        logging.info(message)

    def __call__(self) -> pd.DataFrame:
        """

        :return:
            identifier: This will be the code of the selected name/label
            name:
            label:
            category:
            group:
        """

        __preference: list = self.__arguments.get('preference')
        __rename: dict = self.__arguments.get('rename')
        __category: dict = self.__arguments.get('category')
        __group: dict = self.__arguments.get('group')

        # A data frame consisting of the labels of interest
        frame = pd.DataFrame.from_records(data=list(enumerate(__preference)), columns=['identifier', 'name'])

        # An additional field of alternative labels names
        frame['label'] = frame['name']
        frame['label'] = frame['label'].replace(to_replace=__rename).values

        # Extra
        frame = frame.assign(
            category=frame['name'].map(__category), group=frame['name'].map(__group))

        # Persist
        self.__persist(frame=frame)

        logging.info(frame)

        return frame
