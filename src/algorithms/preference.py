import pandas as pd


class Preference:

    def __init__(self, arguments: dict):

        self.__preference: list = arguments.get('preference')
        self.__rename: dict = arguments.get('rename')


    def __call__(self):

        # A data frame consisting of the labels of interest
        frame = pd.DataFrame.from_records(data=list(enumerate(self.__preference)), columns=['identifier', 'name'])

        # An additional field of alternative labels names
        frame['label'] = frame['name']
        frame['label'] = frame['label'].replace(to_replace=self.__rename).values

        return frame
